import asyncio
import sys
from asyncio import get_running_loop
from concurrent.futures import ThreadPoolExecutor
from threading import Event

import grpc
import hypercorn.asyncio
import hypercorn.config

from grpc_helpers.proxy import proxy

_servers = []


def _identities(cls):
    yield cls
    for base in cls.__bases__:
        yield from _identities(base)


def serve(
        *services,
        address='::', port=None,
        credentials=None,
        max_workers=10,
        web=False, web_port=8080,
        block=True):
    executor = ThreadPoolExecutor(max_workers=max_workers)
    grpc_server = grpc.server(executor)

    for service in services:
        for cls in _identities(service.__class__):
            if hasattr(sys.modules[cls.__module__], f'add_{cls.__name__}_to_server'):
                getattr(sys.modules[cls.__module__], f'add_{cls.__name__}_to_server')(service, grpc_server)
                break
        else:
            raise ValueError(f'Class "{service.__class__.__name__}" is not a gRPC service')

    if not port:
        port = 443 if credentials else 80
    if credentials:
        grpc_server.add_secure_port(f'[{address}]:{port}', credentials)
    else:
        grpc_server.add_insecure_port(f'[{address}]:{port}')

    grpc_server.start()
    _servers.append(grpc_server)

    if web:
        app = proxy(f'localhost:{port}')
        config = hypercorn.config.Config()
        config.bind = [f"{address}:{web_port}"]
        web_server = hypercorn.asyncio.serve(app, config)

        loop = get_running_loop()
        if loop:
            return grpc_server, loop.create_task(web_server)
        else:
            asyncio.run(web_server)
    elif block:
        Event().wait()

    return grpc_server
