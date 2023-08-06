from .utilities import *
from .supports import ReadablePathHandler, PathHandler, ChannelListener, ActiveSubscriberPathHandler
from rejson import Path
import logging
import queue

logger = logging.getLogger("reem")


class Writer:
    """Responsible for setting data inside Redis

    The Writer class is an internal class that is used for all data sent to Redis (not including pub/sub messages).
    Each key that will have nested data below requires a new instantiation of Writer

    Attributes:
        top_key_name (str): The name of the Redis key under which JSON data will be stored. To Redis,
            this will become a ReJSON key name. It is also used to generate the Redis key name that ``ship``'s use to
            store non JSON data.
        interface (RedisInterface): Defines the connection to Redis this writer will use
    """
    def __init__(self, top_key_name, interface):
        self.interface = interface
        self.top_key_name = top_key_name
        self.metadata_key_name = "{}{}metadata".format(self.top_key_name, SEPARATOR_CHARACTER)
        self.metadata = None
        self.__initialize_metadata()
        self.sp_to_label = self.metadata["special_paths"]
        self.pipeline = self.interface.client.pipeline()
        self.do_metadata_update = True

    def __initialize_metadata(self):
        """ Pull metadata for this key from Redis or set a default

        Returns:
            None
        """
        try:
            pulled = self.interface.client.jsonget(self.metadata_key_name, ".")
            if pulled is not None:
                self.metadata = pulled
                return
        except TypeError:
            pass
        self.metadata = {"special_paths": {}, "required_labels": self.interface.shipper_labels}

    def send_to_redis(self, set_path, set_value):
        """ Execute equivalent of ``JSON.SET self.top_key_name <set_path> <set_value>``

        From the user's perspective, it executes ``JSON.SET self.top_key_name <set_path> <set_value>``
        except that ``set_value`` can be json-incompatible. This is the only public
        method of this class. It determines what non-serializable types are inside set_value, stores the
        serializable data as a JSON, and stores the non-serializable data using ``self.interface``'s ships

        Args:
            set_path (str): path underneath JSON key to set
            set_value: value to set

        Returns:
            None

        """
        logger.info("SET {} {} = {}".format(self.top_key_name, set_path, type(set_value)))
        self.__process_metadata(set_path, set_value)
        logger.debug("SET {} {} Metadata: {}".format(self.top_key_name, set_path, self.metadata))
        self.__publish_non_serializables(set_path, set_value)
        logger.debug("SET {} {} Non-Serializables Pipelined".format(self.top_key_name, set_path))
        self.__publish_serializables(set_path, set_value)
        logger.debug("SET {} {} Serializables Pipelined".format(self.top_key_name, set_path))
        self.pipeline.execute()
        logger.debug("SET {} {} Pipeline Executed".format(self.top_key_name, set_path))

    def __process_metadata(self, set_path, set_value):
        """ Handle metadata updates

        Given the path and value the user would like to set, check if there are non-serializable data types and update
        metadata locally and in Redis. Happens without pipeline

        Args:
            set_path (str): path underneath JSON key to set
            set_value: value to set

        Returns:
            None

        """
        if not self.do_metadata_update:
            return

        overridden_paths = set()
        for existing_path in self.sp_to_label.keys():
            if existing_path.startswith(set_path):
                overridden_paths.add(existing_path)
        [self.sp_to_label.pop(op) for op in overridden_paths]

        special_paths = get_special_paths(set_path, set_value, self.sp_to_label, self.interface.label_to_shipper)
        dels, adds = overridden_paths - special_paths, special_paths - overridden_paths
        for set_path, label in special_paths:
            self.sp_to_label[set_path] = label

        if len(adds) > 0 or len(dels) > 0:
            self.pipeline.jsonset(self.metadata_key_name, ".", self.metadata)
            channel, message = "__keyspace@0__:{}".format(self.metadata_key_name), "set"
            self.pipeline.publish(channel, message)  # Homemade key-space notification for metadata updates

    def __publish_non_serializables(self, set_path, set_value):
        """Publish JSON incompatible data to Redis

        Given a set, publish the non-serializable components to redis, given that metadata has been updated already

        Args:
            set_path (str): path underneath JSON key to set
            set_value: value to set

        Returns:
            None
        """

        overridden_paths, suffixes = filter_paths_by_prefix(self.sp_to_label.keys(), set_path)
        for full_path, suffix in zip(overridden_paths, suffixes):
            logger.debug("Suffix = {}".format(suffix))
            update_value = extract_object(set_value, path_to_key_sequence(suffix))
            special_path_redis_key_name = "{}{}".format(self.top_key_name, full_path)
            logger.debug("SET {} {} Non-serializable update {} = {}".format(
                self.top_key_name, set_path, special_path_redis_key_name, type(update_value))
            )
            self.interface.label_to_shipper[self.sp_to_label[full_path]].write(
                key=special_path_redis_key_name,
                value=update_value,
                client=self.pipeline
            )

    def __publish_serializables(self, set_path, set_value):
        """ Publish the serializable portion of ``set_value

        Take out the non-serializable part of set_value and publish it at set_path

        Args:
            set_path (str): path underneath JSON key to set
            set_value: value to set

        Returns: None

        """
        if type(set_value) is dict:
            intrusive_paths, suffixes = filter_paths_by_prefix(self.sp_to_label.keys(), set_path)
            excised_copy = copy_dictionary_without_paths(set_value, [path_to_key_sequence(s) for s in suffixes])
            self.pipeline.jsonset(self.top_key_name, set_path, excised_copy)
            logger.debug("SET {} {} Serializable update {} = {}".format(self.top_key_name, set_path, set_path, excised_copy))
        elif set_path not in self.sp_to_label:
            self.pipeline.jsonset(self.top_key_name, set_path, set_value)
            logger.debug("SET {} {} Serializable update {} = {}".format(self.top_key_name, set_path, set_path, set_value))


class Reader:
    """Responsible for getting data from Redis

    The Reader class is an internal class that is used for all read from Redis (not including pub/sub messages).
    Each key that will have nested data below requires a new instantiation of Reader

    Attributes:
        top_key_name (str): The name of the Redis key under which JSON data is stored
        interface (RedisInterface): Defines the connection to Redis this reader will use
    """
    def __init__(self, top_key_name, interface):
        self.interface = interface
        self.top_key_name = top_key_name
        self.metadata = {"special_paths": {}, "required_labels": self.interface.shipper_labels}
        self.sp_to_label = self.metadata["special_paths"]
        self.pipeline = self.interface.client.pipeline()
        self.pipeline_no_decode = self.interface.client_no_decode.pipeline()
        self.metadata_key_name = "{}{}metadata".format(self.top_key_name, SEPARATOR_CHARACTER)
        self.interface.metadata_listener.add_listener(self.metadata_key_name, self)
        self.pull_metadata = True
        # Will need to update metadata on first read regardless so the simple initialization we have here is sufficient

    def read_from_redis(self, read_path):
        """ Read specified path from Redis

        This is the only public method of the Reader class. It will retrieve the data stored at a specified path
        from Redis. At a high level, it reads data stored with ReJSON and inserts non-JSON compatible data
        at appropriate paths using the metadata associated with this key.

        Args:
            read_path (str): path the user wants to read

        Returns: data stored at value in Redis

        """

        self.interface.INTERFACE_LOCK.acquire(timeout=1)
        logger.info("GET {} {} pull_metadata = {}".format(self.top_key_name, read_path, self.pull_metadata))
        self.update_metadata()
        logger.debug("GET {} {} Using Metadata: {}".format(self.top_key_name, read_path, self.metadata))
        if read_path in self.sp_to_label:
            ret_val = self.pull_special_path(read_path)
        else:
            self.queue_reads(read_path)
            logger.debug("GET {} {} Reads Queued".format(self.top_key_name, read_path))
            ret_val = self.build_dictionary(read_path)
            logger.debug("GET {} {} Dictionary Built".format(self.top_key_name, read_path))
        self.interface.INTERFACE_LOCK.release()
        return ret_val

    def update_metadata(self):
        """ Update the local copy of metadata if a relevant path has been updated.

        The metadata listener is a redis client subscribed to key-space notifications. If a relevant path is updated,
        this Reader's ``pull_metadata`` flag will be turned on. If ``pull_metadata`` is ``True``, then the reader
        will fetch metadata from the Redis server.

        Returns: None

        """
        self.interface.metadata_listener.flush()
        if self.pull_metadata:
            try:
                pulled = self.interface.client.jsonget(self.metadata_key_name, ".")
                if pulled is not None:
                    self.metadata = pulled
            except TypeError:  # No Metadata online
                return
            self.sp_to_label = self.metadata["special_paths"]
        self.pull_metadata = False

    def queue_reads(self, read_path):
        """ Queue reads in a pipeline

        Queue all redis queries necessary to read data at path into the appropriate redis pipeline.
        First, queue decoded pipeline with the ReJSON query
        Next, queue all the special path reads with the non-decoded pipeline and ships

        Args:
            read_path: path user wants to read

        Returns: None
        """
        self.pipeline.jsonget(self.top_key_name, read_path)
        special_paths, suffixes = filter_paths_by_prefix(self.sp_to_label.keys(), read_path)
        for p in special_paths:
            special_path_redis_key_name = "{}{}".format(self.top_key_name, p)
            logger.debug("type(sp to label) = {}, type(p) = {}".format(type(self.sp_to_label), type(p)))
            ship = self.interface.label_to_shipper[self.sp_to_label[p]]
            ship.read(special_path_redis_key_name, self.pipeline_no_decode)

    def build_dictionary(self, read_path):
        """ Execute pipelines and consolidate data into a dictionary

        Args:
            read_path: path user wants to read

        Returns: The data stored at ``read_path`` in Redis
        """

        return_val = self.pipeline.execute()[0]
        logger.debug("GET {} {} Serializable Pipeline Executed".format(self.top_key_name, read_path))
        responses = self.pipeline_no_decode.execute()
        special_paths, suffixes = filter_paths_by_prefix(self.sp_to_label.keys(), read_path)
        logger.debug("special_path = {}, suffixes = {}".format(special_paths, suffixes))
        for i, (sp, suffix) in enumerate(zip(special_paths, suffixes)):
            value = self.interface.label_to_shipper[self.sp_to_label[sp]].interpret_read(responses[i: i + 1])
            insert_into_dictionary(return_val, path_to_key_sequence(suffix), value)
            logger.debug("GET {} {} Nonserializable Pipeline Inserted {} = {}"
                         .format(self.top_key_name, read_path, sp, type(value))
                         )
        logger.debug("GET {} {} Dictionary Built".format(self.top_key_name, read_path))
        return return_val

    def pull_special_path(self, read_path):
        """ Directly pull a non-JSON path

        If the user specified path is not in JSON, this will retrieve the data directly without going through ReJSON.

        Args:
            read_path: path user wants to read

        Returns:

        """
        shipper = self.interface.label_to_shipper[self.sp_to_label[read_path]]
        special_name = "{}{}".format(self.top_key_name, read_path)
        shipper.read(special_name, self.pipeline_no_decode)
        responses = self.pipeline_no_decode.execute()
        return shipper.interpret_read(responses)


class KeyValueStore:
    """Dictionary Like object used for get/set paradigm

    The ``KeyValueStore`` object is one that users will frequently use. It keeps ``Reader`` and ``Writer`` objects
    for each key that the user read or written to. It does not actually handle the getting and setting of data
    but produces ``ReadablePathHandler`` objects that assist with path construction and call the reader and
    writer's write and read methods.

    Attributes:
        interface (RedisInterface): Defines the connection to Redis this reader will use
    """
    def __init__(self, interface):
        self.interface = interface
        self.entries = {}
        self.track_schema = True

    def __setitem__(self, key, value):
        """ Only used for setting key on first level of KVS. i.e. KVS["top_key"] = value. Otherwise see __getitem__

        Args:
            key (str): "dictionary" key. It becomes a top-level Redis key
            value: value to store

        Returns: None

        """

        assert check_valid_key_name(key), "Invalid Key: {}".format(key)
        if type(value) != dict:
            value = {"{}ROOT{}".format(ROOT_VALUE_SEQUENCE, ROOT_VALUE_SEQUENCE): value}
        self.__ensure_key_existence(key)
        writer, reader = self.entries[key]
        writer.send_to_redis(Path.rootPath(), value)

    def __getitem__(self, item):
        """Used to retrieve ReadablePathHandler object for handling path construction when setting/getting Redis

        Args:
            item (str): "dictionary" key. It must be a top-level Redis key

        Returns:

        """

        assert check_valid_key_name(item), "Invalid Key: {}".format(item)
        logger.debug("KVS GET {}".format(item))
        self.__ensure_key_existence(item)
        writer, reader = self.entries[item]
        return ReadablePathHandler(writer=writer, reader=reader, initial_path=Path.rootPath())

    def __ensure_key_existence(self, key):
        """ Ensure that the requested key has a reader and writer associated with it.

        Returns: None

        """

        assert check_valid_key_name(key), "Invalid Key: {}".format(key)
        if key not in self.entries:
            self.entries[key] = (Writer(key, self.interface), Reader(key, self.interface))
            self.entries[key][0].do_metadata_update = self.track_schema

    def track_schema_changes(self, set_value, keys=None):
        """ Performance optimization for skipping schema update checks

        Stop checking for schema updates when setting data. Use ONLY if your data's schema is static
        and you are really trying to eek out every bit of optimization.

        Args:
            set_value (bool): True/False indicating if the keys' schema should be tracked
            keys (List[str]): List of keys to track. If None, all present and future keys are tracked
            according to ``set_value``

        Returns: None

        """

        if keys is None:
            keys = self.entries.keys()
            self.track_schema = set_value
        for k in keys:
            self.entries[k][0].do_metadata_update = set_value


class Publisher(Writer):
    """ Defines Publisher behavior

    The Publisher is identical to the writer but publishes a message when it writes a value.

    """

    def __init__(self, top_key_name, interface):
        super().__init__(top_key_name, interface)
        self.message = "Publish"

    def send_to_redis(self, set_path, set_value):
        """ Publisher equivalent of Writer ``send_to_redis``

        This is an equivalent function to ``Writer``'s ``send_to_redis`` method but also publishes a message
        indicating what channel has been updated.

        Args:
            set_path (str): path underneath JSON key to set
            set_value: value to set

        Returns: None

        """

        logger.info("PUBLISH {} {} = {}".format(self.top_key_name, set_path, type(set_value)))
        logger.debug("PUBLISH {} {} Metadata Update?: {}".format(self.top_key_name, set_path, self.do_metadata_update))
        self.__process_metadata(set_path, set_value)
        logger.debug("PUBLISH {} {} Metadata: {}".format(self.top_key_name, set_path, self.metadata))
        self.__publish_non_serializables(set_path, set_value)
        self.__publish_serializables(set_path, set_value)

        # Addition to Writer class
        if set_path == Path.rootPath():
            set_path = ""
        channel_name = "__pubspace@0__:{}{}".format(self.top_key_name, set_path)
        self.pipeline.publish(channel_name, self.message)

        # Resume Writer Class
        self.pipeline.execute()
        logger.debug("PUBLISH {} {} pipeline executed, published {} to {}".format(
            self.top_key_name, set_path, self.message, channel_name)
        )


class PublishSpace(KeyValueStore):
    """ Convenience class for publishing

    This class keeps track of ``Publisher`` objects for each key the user has published on.

    """
    def __getitem__(self, item):
        """ Identical to ``KeyValueStore`` method of same name but provides non-readable ``PathHandler`` objects

        """
        assert type(item) == str
        self.__ensure_key_existence(item)
        publisher, _ = self.entries[item]
        return PathHandler(writer=publisher, reader=_, initial_path=Path.rootPath())

    def __ensure_key_existence(self, key):
        """ Identical to ``KeyValueStore`` method of same name but does not instantiate a ``Reader`` object
        """

        assert check_valid_key_name(key), "Invalid Key: {}".format(key)
        if key not in self.entries:
            self.entries[key] = (Publisher(key, self.interface), None)
            self.entries[key][0].do_metadata_update = self.track_schema


class RawSubscriber:
    def __init__(self, channel_name, interface, callback_function, kwargs):
        self.listening_channel = '__pubspace@0__:{}'.format(channel_name)
        self.listener = ChannelListener(interface, self.listening_channel, callback_function, kwargs)
        self.listener.setDaemon(True)

    def listen(self):
        self.listener.start()


class SilentSubscriber(Reader):
    """ Silent Subscriber Implementation"""

    def __init__(self, channel, interface):
        super().__init__(channel, interface)
        self.local_copy = {}
        self.passive_subscriber = RawSubscriber(channel + "*", interface, self.update_local_copy, {})
        self.prefix = "__pubspace@0__:{}".format(self.top_key_name)

    def update_local_copy(self, channel, message):
        """ Update the local copy of the data stored under this channel name in redis.

        Args:
            channel: the name of the channel that was published.
            message: message published on that channel

        Returns: None

        """

        logger.info("SILENT_SUBSCRIBER @{} : channel={} message={}".format(self.prefix, channel, message))
        try:
            message = message.decode("utf-8")
        except Exception as e:
            return
        if message != "Publish":
            return

        if channel == self.prefix:
            self.local_copy = self.read_from_redis(Path.rootPath())
            return

        path = channel[len(self.prefix):]
        redis_value = self.read_from_redis(path)
        logger.debug("SILENT_SUBSCRIBER @{} : Read from Redis: {}".format(self.prefix, redis_value))
        insert_into_dictionary(self.local_copy, path_to_key_sequence(path), redis_value)
        logger.debug("SILENT_SUBSCRIBER @{} : Local Copy: {}".format(self.prefix, self.local_copy))

    def listen(self):
        """ Makes this subscriber start listening

        Returns: None

        """
        self.passive_subscriber.listen()

    def value(self):
        """ Get data stored at root

        Where as the reader can do ``server["foo"].read()`` with if server is a ``KeyValueStore``,
        accessing the root value of a subscriber is not as easy. This method retrieves all data stored underneath
        a top level key.

        Returns: all data stored underneath a top level Redis key.

        """
        root_name = "{0}ROOT{0}".format(ROOT_VALUE_SEQUENCE)
        if root_name in self.local_copy:
            return self.local_copy[root_name]
        # Copy dictionary - paths to omit is blank, so we copy everything
        return copy_dictionary_without_paths(self.local_copy, [])

    def __getitem__(self, item):
        """ Implement dictionary API for local copy

        We do not give the user direct access to the dictionary representing the lcoal
        Args:
            item:

        Returns:

        """
        assert type(item) == str, "Key name must be string"
        return ActiveSubscriberPathHandler(None, self, "{}{}".format(Path.rootPath(), item))


class CallbackSubscriber(SilentSubscriber):
    """ Callback Subscriber Implementation"""

    def __init__(self, channel, interface, callback_function, kwargs):
        super().__init__(channel, interface)
        self.queue = queue.Queue()
        self.passive_subscriber = RawSubscriber(channel + "*", interface, self.call_user_function, {})
        self.callback_function = callback_function
        self.kwargs = kwargs

    def call_user_function(self, channel, message):
        """
        Wrapper callback function (wrapping user function) for this class to work with a RawSubscriber object
        Fits required interface for a ChannelSubscriber callback function
        :param channel: channel published to
        :param message: message that was published
        :return: None
        :rtype: None
        """
        self.update_local_copy(channel, message)
        channel_name = channel.split("__pubspace@0__:")[1]
        self.callback_function(data=self.value(), updated_path=channel_name, **self.kwargs)