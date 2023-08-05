import pytest
import trio
import mock
from time import time

from trio_click.testing import CliRunner
from .mock_serf import stdtest
from .run import run
from distkv.client import ServerError
import asyncserf
import msgpack
from distkv.util import attrdict

import logging

logger = logging.getLogger(__name__)

N = 20


@pytest.mark.trio
async def test_10_many(autojump_clock):
    """
    This test starts multiple servers at the same time.
    """
    async with stdtest(test_1={"init": 420}, n=N, tocks=1000) as st:
        s = st.s[1]
        async with st.client(1) as ci:
            assert (await ci.request("get_value", path=())).value == 420
            await ci.request("set_value", path=("ping",), value="pong")

        await trio.sleep(1)

        async def s1(i, *, task_status=trio.TASK_STATUS_IGNORED):
            async with st.client(i) as c:
                task_status.started()
                assert (await c.request("get_value", path=())).value == 420
                assert (await c.request("get_value", path=("ping",))).value == "pong"
                await c.request("set_value", path=("foo", i), value=420 + i)

        async with trio.open_nursery() as tg:
            for i in range(1, N):
                await tg.start(s1, i)

        await trio.sleep(1)
        NN = min(N - 1, 3)
        for j in [0] + s._random.sample(range(1, N), NN):
            async with st.client(j) as c:
                for i in s._random.sample(range(1, N), NN):
                    assert (
                        await c.request("get_value", path=("foo", i))
                    ).value == 420 + i

        # await trio.sleep(100)
        pass  # server end


@pytest.mark.trio
@pytest.mark.parametrize("tocky", [-10, -2, -1, 0, 1, 2, 10])
async def test_11_split1(autojump_clock, tocky):
    """
    This test starts multiple servers at the same time.
    """
    n_two = 0

    async with stdtest(test_1={"init": 420}, n=N, tocks=1000) as st:

        async def watch(*, task_status=trio.TASK_STATUS_IGNORED):
            nonlocal n_two
            async with asyncserf.serf_client() as s:
                async with s.stream("user:test.update") as sr:
                    task_status.started()
                    async for r in sr:
                        msg = msgpack.unpackb(
                            r.payload,
                            object_pairs_hook=attrdict,
                            raw=False,
                            use_list=False,
                        )
                        if msg.get("value", "") == "two":
                            n_two += 1

                    i.s()

        await st.tg.start(watch)
        s = st.s[1]
        async with st.client(1) as ci:
            assert (await ci.request("get_value", path=())).value == 420
            await ci.request("set_value", path=("ping",), value="pong")

        async def s1(i, *, task_status=trio.TASK_STATUS_IGNORED):
            async with st.client(i) as c:
                task_status.started()
                assert (await c.request("get_value", path=())).value == 420
                await trio.sleep(5)
                assert (await c.request("get_value", path=("ping",))).value == "pong"
                await c.request("set_value", path=("foo", i), value=420 + i)
                pass  # client end

        async with trio.open_nursery() as tg:
            for i in range(1, N):
                await tg.start(s1, i)

        await trio.sleep(30)
        st.split(N // 2)
        if tocky:
            async with st.client(2 if tocky < 0 else 14) as ci:
                for i in range(abs(tocky)):
                    await ci.request("set_value", path=("one", i), value="two")
        await trio.sleep(30)

        async with st.client(N - 1) as c:
            await c.request("set_value", path=("ping",), value="pongpang")
        await trio.sleep(1)
        async with st.client(0) as c:
            assert (await c.request("get_value", path=("ping",))).value == "pong"
        st.join(N // 2)
        await trio.sleep(20)
        async with st.client(0) as c:
            assert (await c.request("get_value", path=("ping",))).value == "pongpang"
        pass  # server end

    # Now make sure that updates are transmitted once
    assert n_two <= N + 1
