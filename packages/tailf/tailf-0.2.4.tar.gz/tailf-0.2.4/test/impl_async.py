import asyncio
import functools
import tailf
import tempfile


def nose_async(async_function):
    @functools.wraps(async_function)
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        try:
            coro = async_function(*args, **kwargs)
            loop.run_until_complete(coro)
        finally:
            loop.close()

    return wrapper


async def fill_file(f, strings):
    with f:
        for i, s in enumerate(strings):
            if i != 0:
                await asyncio.sleep(0.1)
            f.write(s)
            f.flush()


@nose_async
async def test_concurrent():
    with tempfile.NamedTemporaryFile("w+b") as f:
        asyncio.get_event_loop().create_task(fill_file(f, [b"alpha", b"beta"]))
        with tailf.Tail(f.name) as tail:
            event = await tail.wait_event()
            assert event == b"alpha"
            event = await tail.wait_event()
            assert event == b"beta"


@nose_async
async def test_asyncfor():
    with tempfile.NamedTemporaryFile("w+b") as f:
        data = [b"alpha", b"beta"]
        asyncio.get_event_loop().create_task(fill_file(f, data))
        index = 0
        with tailf.Tail(f.name) as tail:
            async for event in tail:
                assert event == data[index]
                index += 1
                if index >= len(data):
                    break
