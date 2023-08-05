import logging
import json
import random
from weakref import WeakValueDictionary
from .transport import create_transport
from .bucket import BucketType, Bucket
from aioriak.resolver import default_resolver
from riak.util import bytes_to_str, str_to_bytes
from aioriak.datatypes import TYPES


logger = logging.getLogger('aioriak.client')


def default_encoder(obj):
    '''
    Default encoder for JSON datatypes, which returns UTF-8 encoded
    json instead of the default bloated backslash u XXXX escaped ASCII strings.
    '''
    if isinstance(obj, bytes):
        return json.dumps(bytes_to_str(obj),
                          ensure_ascii=False).encode("utf-8")
    else:
        return json.dumps(obj, ensure_ascii=False).encode("utf-8")


def binary_json_encoder(obj):
    '''
    Default encoder for JSON datatypes, which returns UTF-8 encoded
    json instead of the default bloated backslash u XXXX escaped ASCII strings.
    '''
    if isinstance(obj, bytes):
        return json.dumps(bytes_to_str(obj),
                          ensure_ascii=False).encode("utf-8")
    else:
        return json.dumps(obj, ensure_ascii=False).encode("utf-8")


def binary_json_decoder(obj):
    '''
    Default decoder from JSON datatypes.
    '''
    return json.loads(bytes_to_str(obj))


def binary_encoder_decoder(obj):
    '''
    Assumes value is already in binary format, so passes unchanged.
    '''
    return obj


class RiakClient:
    '''
    The ``RiakClient`` object holds information necessary to connect
    to Riak. Requests can be made to Riak directly through the client
    or by using the methods on related objects.
    '''
    def __init__(self, host='localhost', port=8087, loop=None):
        if isinstance(host, (list, tuple, set)):
            self._host = random.choice(host)
        else:
            self._host = host
        self._port = port
        self._loop = loop
        self._bucket_types = WeakValueDictionary()
        self._buckets = WeakValueDictionary()
        self._resolver = None
        self._decoders = {'application/json': binary_json_decoder,
                          'text/json': binary_json_decoder,
                          'text/plain': bytes_to_str,
                          'binary/octet-stream': binary_encoder_decoder}
        self._encoders = {'application/json': binary_json_encoder,
                          'text/json': binary_json_encoder,
                          'text/plain': str_to_bytes,
                          'binary/octet-stream': binary_encoder_decoder}
        self._closed = False

    def __del__(self):
        self.close()

    def get_decoder(self, content_type):
        '''
        Get the decoding function for the provided content type.

        :param content_type: the requested media type
        :type content_type: str
        :rtype: function
        '''
        return self._decoders.get(content_type)

    def get_encoder(self, content_type):
        '''
        Get the encoding function for the provided content type.

        :param content_type: the requested media type
        :type content_type: str
        :rtype: function
        '''
        return self._encoders.get(content_type)

    def set_encoder(self, content_type, encoder):
        '''
        Set the encoding function for the provided content type.

        :param content_type: the requested media type
        :type content_type: str
        :param encoder: an encoding function, takes a single object
            argument and returns encoded data
        :type encoder: function
        '''
        self._encoders[content_type] = encoder

    def set_decoder(self, content_type, decoder):
        '''
        Set the decoding function for the provided content type.

        :param content_type: the requested media type
        :type content_type: str
        :param decoder: a decoding function, takes encoded data and
            returns a Python type
        :type decoder: function
        '''
        self._decoders[content_type] = decoder

    def _get_resolver(self):
        return self._resolver or default_resolver

    def _set_resolver(self, value):
        if value is None or callable(value):
            self._resolver = value
        else:
            raise TypeError('resolver is not a function')

    resolver = property(_get_resolver, _set_resolver,
                        doc='''The sibling-resolution function for this client.
                        Defaults to :func:`aioriak.resolver.default_resolver`.
                        ''')

    def close(self):
        if not self._closed:
            self._closed = True
            self._transport.close()

    async def _create_transport(self):
        self._transport = await create_transport(
            self._host, self._port, self._loop)

    @classmethod
    async def create(cls, host='localhost', port=8087, loop=None):
        '''
        Return initialized instance of RiakClient since
        RiakClient.__init__() can't be async.

        :Example:

        .. code-block:: python

            import asyncio
            from aioriak import RiakClient
            loop = asyncio.get_event_loop()
            async def go():
                client = await RiakClient.create('localhost', 8087, loop)
            loop.run_until_complete(go())

        :param host: Hostname or ip address of Riak instance
        :type host: str, list, tuple
        :param port: Port of riak instance
        :type port: int
        :param loop: asyncio event loop
        :rtype: :class:`~aioriak.client.RiakClient`
        '''
        client = cls(host, port, loop)
        await client._create_transport()
        return client

    async def fetch_datatype(self, bucket, key):
        '''
        Fetches the value of a Riak Datatype.

        :param bucket: the bucket of the datatype, which must belong to a
            :class:`~aioriak.bucket.BucketType`
        :type bucket: :class:`~aioriak.bucket.Bucket`
        :param key: the key of the datatype
        :type key: string
        :rtype: :class:`~aioriak.datatypes.Datatype`
        '''
        dtype, value, context = await self._fetch_datatype(bucket, key)

        return TYPES[dtype](bucket=bucket, key=key, value=value,
                            context=context)

    async def _fetch_datatype(self, bucket, key):
        '''
        _fetch_datatype(bucket, key)

        Fetches the value of a Riak Datatype as raw data. This is used
        internally to update already reified Datatype objects. Use the
        public version to fetch a reified type.

        :param bucket: the bucket of the datatype, which must belong to a
            :class:`~aioriak.BucketType`
        :type bucket: RiakBucket
        :param key: the key of the datatype
        :type key: string, None
        :rtype: tuple of type, value and context
        '''
        return await self._transport.fetch_datatype(bucket, key)

    async def ping(self):
        '''
        Check if the Riak server for this ``RiakClient`` instance is alive.

        :rtype: boolean
        '''
        return await self._transport.ping()

    is_alive = ping

    async def get_client_id(self):
        '''
        Get client ID for this RiakClient instance

        :rtype: bytes
        '''
        return await self._transport.get_client_id()

    async def set_client_id(self, id):
        '''
        Set Client ID for this RiakClient instance'
        '''
        return await self._transport.set_client_id(id)

    async def get_buckets(self, bucket_type=None):
        '''
        Get the list of buckets as :class:`Bucket
        <aioriak.bucket.Bucket>` instances.

        .. warning:: Do not use this in production, as it requires
            traversing through all keys stored in a cluster.

        :param bucket_type: the optional containing bucket type
        :type bucket_type: :class:`~aioriak.bucket.BucketType`
        :rtype: list of :class:`Bucket <aioriak.bucket.Bucket>`
            instances
        '''
        if bucket_type:
            maker = bucket_type.bucket
        else:
            maker = self.bucket

        return [maker(name.decode())
                for name in await self._transport.get_buckets(
                    bucket_type=bucket_type)]

    def bucket_type(self, name):
        '''
        Gets the bucket-type by the specified name. Bucket-types do
        not always exist (unlike buckets), but this will always return
        a :class:`BucketType <aioriak.bucket.BucketType>` object.

        :param name: the bucket name
        :type name: str
        :rtype: :class:`BucketType <aioriak.bucket.BucketType>`
        '''
        if not isinstance(name, str):
            raise TypeError('Bucket name must be a string')

        btype = self._bucket_types.get(name)
        if not btype:
            btype = BucketType(self, name)
            self._bucket_types[name] = btype
        return btype

    def bucket(self, name, bucket_type='default'):
        '''
        Get the bucket by the specified name. Since buckets always exist,
        this will always return a
        :class:`Bucket <aioriak.bucket.Bucket>`.
        If you are using a bucket that is contained in a bucket type, it is
        preferable to access it from the bucket type object::

            # Preferred:
            client.bucket_type("foo").bucket("bar")
            # Equivalent, but not preferred:
            client.bucket("bar", bucket_type="foo")

        :param name: the bucket name
        :type name: str
        :param bucket_type: the parent bucket-type
        :type bucket_type: :class:`BucketType <aioriak.bucket.BucketType>`
            or str
        :rtype: :class:`Bucket <aioriak.bucket.Bucket>`
        '''
        if not isinstance(name, str):
            raise TypeError('Bucket name must be a string')

        if isinstance(bucket_type, str):
            bucket_type = self.bucket_type(bucket_type)
        elif not isinstance(bucket_type, BucketType):
            raise TypeError('bucket_type must be a string '
                            'or aioriak.bucket.BucketType')

        bucket = self._buckets.get((bucket_type, name))
        if not bucket:
            bucket = Bucket(self, name, bucket_type)
            self._buckets[(bucket_type, name)] = bucket
        return bucket

    async def get_bucket_type_props(self, bucket_type):
        '''
        Fetches properties for the given bucket-type.

        :param bucket_type: the bucket-type whose properties will be fetched
        :type bucket_type: BucketType
        :rtype: dict
        '''
        return await self._transport.get_bucket_type_props(bucket_type)

    async def set_bucket_type_props(self, bucket_type, props):
        '''
        Sets properties for the given bucket-type.

        :param bucket_type: the bucket-type whose properties will be set
        :type bucket_type: BucketType
        :param props: the properties to set
        :type props: dict
        '''
        return await self._transport.set_bucket_type_props(bucket_type, props)

    async def get_bucket_props(self, bucket):
        '''
        Fetches bucket properties for the given bucket.

        :param bucket: the bucket whose properties will be fetched
        :type bucket: Bucket
        :rtype: dict
        '''
        return await self._transport.get_bucket_props(bucket)

    async def set_bucket_props(self, bucket, props):
        '''
        Sets bucket properties for the given bucket.

        :param bucket: the bucket whose properties will be set
        :type bucket: Bucket
        :param props: the properties to set
        :type props: dict
        '''
        return await self._transport.set_bucket_props(bucket, props)

    async def get_keys(self, bucket):
        '''
        Lists all keys in a bucket.

        .. warning:: Do not use this in production, as it requires
           traversing through all keys stored in a cluster.

        :param bucket: the bucket whose keys are fetched
        :type bucket: Bucket
        :rtype: list
        '''
        return await self._transport.get_keys(bucket)

    async def get(self, robj):
        '''
        Fetches the contents of a Riak object.

        :param robj: the object to fetch
        :type robj: RiakObject
        '''
        if not isinstance(robj.key, str):
            raise TypeError(
                'key must be a string, instead got {0}'.format(repr(robj.key)))

        return await self._transport.get(robj)

    async def put(self, robj, w=None, dw=None, pw=None, return_body=None,
                  if_none_match=None, timeout=None):
        '''
        Stores an object in the Riak cluster.

        :param robj: the object to store
        :type robj: RiakObject
        :param w: the write quorum
        :type w: integer, string, None
        :param dw: the durable write quorum
        :type dw: integer, string, None
        :param pw: the primary write quorum
        :type pw: integer, string, None
        :param return_body: whether to return the resulting object
           after the write
        :type return_body: boolean
        :param if_none_match: whether to fail the write if the object
          exists
        :type if_none_match: boolean
        :param timeout: a timeout value in milliseconds
        :type timeout: int
        '''
        return await self._transport.put(robj, w=w, dw=dw, pw=pw,
                                         return_body=return_body,
                                         if_none_match=if_none_match,
                                         timeout=timeout)

    async def delete(self, robj):
        '''
        Deletes an object from Riak.

        :param robj: the object to delete
        :type robj: RiakObject
        '''
        return await self._transport.delete(robj)

    async def update_datatype(self, datatype, **params):
        '''
        Sends an update to a Riak Datatype to the server.

        :param datatype: the datatype with pending updates
        :type datatype: :class:`~aioriak.datatypes.Datatype`
        :rtype: tuple of datatype, opaque value and opaque context
        '''

        return await self._transport.update_datatype(datatype, **params)

    async def get_index(self, bucket, index, startkey, *args, **kwargs):
        """
        Queries a secondary index, returning matching keys.

        :param bucket: the bucket whose index will be queried
        :type bucket: :class:`~aioriak.bucket.Bucket`
        :param index: the index to query
        :type index: str
        :param startkey: the sole key to query, or beginning of the query range
        :type startkey: str | int
        :param endkey: the end of the query range (optional if equality)
        :type endkey: str | int
        :param return_terms: whether to include the secondary index value
        :type return_terms: bool
        :param max_results: the maximum number of results to return (page size)
        :type max_results: int
        :param continuation: the opaque continuation returned from a
            previous paginated request
        :type continuation: str
        :param timeout: a timeout value in milliseconds, or 'infinity'
        :type timeout: int | str
        :param term_regex: a regular expression used to filter index terms
        :type term_regex: str

        :rtype: list of keys or list of pairs (index_value, key)
        """
        return await self._transport.get_index(bucket, index, startkey, *args,
                                               **kwargs)

    async def mapred(self, inputs, query, timeout=None):
        """
        Executes a MapReduce query.

        Example::
                client = await RiakClient.create()
                result = await client.mapred(
                    {"bucket": ["bucket_type", "bucket"]},
                    [{"map": {
                        "language": "erlang",
                        "module": "mr_example",
                        "function": "get_keys"}])

        :param inputs: the input list/structure
        :type inputs: list[str] | dict
        :param query: the list of query phases
        :type query: list[dict]
        :param timeout: the query timeout
        :type timeout: int | None
        :rtype: mixed
        """
        return await self._transport.mapred(inputs, query, timeout)

    async def stream_mapred(self, inputs, query, timeout=None):
        """
        Streams a MapReduce query as (phase, data) pairs.
        Returns async iterator.

        Example::
                client = await RiakClient.create()
                stream = await client.mapred(
                    {"bucket": ["bucket_type", "bucket"]},
                    [{"map": {
                        "language": "erlang",
                        "module": "mr_example",
                        "function": "get_keys"}])

                async for phase, result in stream:
                    print(phase, result)

        :param inputs: the input list/structure
        :type inputs: list[str] | dict
        :param query: the list of query phases
        :type query: list[dict]
        :param timeout: the query timeout
        :type timeout: integer, None
        :rtype: iterator
        """

        return await self._transport.stream_mapred(inputs, query, timeout)
