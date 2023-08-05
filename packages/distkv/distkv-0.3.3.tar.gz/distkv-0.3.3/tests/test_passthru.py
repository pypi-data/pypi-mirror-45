import pytest
import trio
import mock
from time import time

from trio_click.testing import CliRunner
from .mock_serf import stdtest
from .run import run
from distkv.client import ServerError
from distkv.util import PathLongener

import logging

logger = logging.getLogger(__name__)


@pytest.mark.trio
async def test_51_passthru(autojump_clock):
    async with stdtest(args={"init": 123}) as st:
        s, = st.s
        async with st.client() as c:
            recv = []

            async def mon():
                async with c.stream("serfmon", type="foo") as q:
                    async for m in q:
                        assert "data" in m
                        recv.append(m.data)

            await s.spawn(mon)
            await trio.sleep(0.2)
            await c.request("serfsend", type="foo", data=["Hello", 42])
            await c.request("serfsend", type="foo", data=b"duh")
            await trio.sleep(0.5)
        assert recv == [("Hello", 42), b"duh"]
        pass  # closing client
    pass  # closing server


@pytest.mark.trio
async def test_52_passthru_bin(autojump_clock):
    async with stdtest(args={"init": 123}) as st:
        s, = st.s
        async with st.client() as c:
            recv = []

            async def mon():
                async with c.stream("serfmon", type="foo", raw=True) as q:
                    async for m in q:
                        assert not "data" in m
                        recv.append(m.raw)

            await s.spawn(mon)
            await trio.sleep(0.2)
            await c.request("serfsend", type="foo", data=["Hello", 42])
            await c.request("serfsend", type="foo", raw=b"duh")
            await trio.sleep(0.5)
        assert recv == [b"\x92\xa5Hello*", b"duh"]
        pass  # closing client
    pass  # closing server
