import asyncio
import gc

import async_timeout

from spruned.application.tools import async_delayed_task
from spruned.builder import cache, headers_reactor, blocks_reactor, jsonrpc_server, repository, p2p_connectionpool


async def main_task(loop):  # pragma: no cover
    from spruned.application.logging_factory import Logger
    loop.create_task(jsonrpc_server.start())
    try:
        Logger.leveldb.debug('Ensuring integrity of the storage, and tracking missing items')
        try:
            await loop_check_integrity(loop)
        except asyncio.TimeoutError:
            Logger.cache.error('There must be an error in storage, 30 seconds to check are too many')
        Logger.leveldb.debug('Checking cache limits')
        try:
            await asyncio.wait_for(asyncio.gather(cache.check()), timeout=30)
        except asyncio.TimeoutError:
            Logger.cache.error('There must be an error in cache, 30 seconds to check are too many')
        headers_reactor.add_on_new_header_callback(blocks_reactor.start)
        headers_reactor.add_on_best_height_hit_volatile_callbacks(blocks_reactor.bootstrap_blocks)
        loop.create_task(headers_reactor.start())
        loop.create_task(p2p_connectionpool.connect())
        loop.create_task(async_delayed_task(cache.lurk(), 600))
        loop.create_task(async_delayed_task(loop_collect_garbage(loop), 300))
    finally:
        pass


async def loop_check_integrity(l):  # pragma: no cover
    """
    this task also prune blocks
    """
    async with async_timeout.timeout(30):
        await repository.ensure_integrity()


async def loop_collect_garbage(l):  # pragma: no cover
    gc.collect()
    l.create_task(async_delayed_task(loop_collect_garbage(l), 300))
