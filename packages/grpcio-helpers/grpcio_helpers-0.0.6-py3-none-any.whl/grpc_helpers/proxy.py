from asyncio import Event, get_event_loop
from base64 import b64encode, b64decode
from math import ceil
from struct import pack, unpack

import grpc
from quart import Quart, request

UNCOMPRESSED = 0x00
COMPRESSED = 0x01

MESSAGE = 0x00
TRAILERS = 0x80


def serializer(message_length, is_trailer=False):
    compressed_flag = (TRAILERS if is_trailer else MESSAGE) | UNCOMPRESSED
    output = bytes([compressed_flag]) + pack('I', message_length)

    buffer = bytearray()
    while True:
        buffer += yield output
        cutoff = len(buffer) - len(buffer) % 3
        part, buffer = buffer[:cutoff], buffer[cutoff:]
        output = b64encode(part)


def deserializer(input=0):
    buffer = bytearray(input)
    while len(buffer) < 5:
        buffer += yield bytes()

    compressed_flag, message_length, buffer = buffer[0], buffer[1:5], buffer[5:]
    message_length = unpack('I', message_length)[0]
    base64_length = ceil(message_length * 4/3)
    if compressed_flag == COMPRESSED:
        raise NotImplementedError

    read_length, decoded_length = len(buffer), 0
    while read_length < base64_length:
        cutoff = len(buffer) - len(buffer) % 4
        part, buffer = buffer[:cutoff], buffer[cutoff:]
        decoded_length += len(part)

        input = yield b64decode(part)
        if input:
            read_length += len(input)
            buffer += input

    yield b64decode(buffer)


def proxy(grpc_server):
    app = Quart('replace_me')
    channel = grpc.insecure_channel(grpc_server)

    @app.route('/<service>/<method>', methods=['POST'])
    async def proxy(service, method):
        deserializer_ = deserializer()
        deserializer_.send(None)
        request_message = b''.join([deserializer_.send(data) async for data in request.body])
        future = channel.unary_unary(f'/{service}/{method}').future(request_message)

        loop = get_event_loop()
        done = Event()
        future.add_done_callback(lambda _: loop.call_soon_threadsafe(done.set))
        await done.wait()

        exception = future.exception()
        response_message = future.result()

        async def response():
            serializer_ = serializer(len(response_message))
            yield serializer_.send(None)
            yield serializer_.send(response_message)
        return response(), 200, {}

    return app
