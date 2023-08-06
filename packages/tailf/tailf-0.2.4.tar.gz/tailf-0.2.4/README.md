tailf
=====

`tail -f` functionality for your python code. Track file appends and
truncations.

Python3.5+ is supported. Asynchronous API is available for Python3.6+.

Examples
--------

```sh
pip install tailf
```

```python
import tailf
import time

with tailf.Tail(filename) as tail:
    while True:
        for event in tail:
            if isinstance(event, bytes):
                print(event.decode("utf-8"), end='')
            elif event is tailf.Truncated:
                print("File was truncated")
            else:
                assert False, "unreachable" # currently. more events may be introduced later
        time.sleep(0.01) # save CPU cycles
```

```python
# async is supported starting from python3.6
# this example requires python3.7 though
import asyncio
import tailf

async def main():
    with tailf.Tail(filename) as tail:
        while True:
            event = await tail.wait_event()
            if isinstance(event, bytes):
                print(event.decode("utf-8"), end='')
            elif event is tailf.Truncated:
                print("File was truncated")
            else:
                assert False, "unreachable" # currently. more events may be introduced later

asyncio.run(main())
```

Limitations
-----------

* Truncation detection is unreliable in general. It is primarily tracked by
  file size decrease, which sometimes can be unreliable. In cases when a file
  grows large and is truncated seldom, this is sufficient.

* Asynchronous tracking is done at timer events (0.01 seconds currently).
  Inotify support could solve this issue on linux. Feel free to suggest other
  solutions.

