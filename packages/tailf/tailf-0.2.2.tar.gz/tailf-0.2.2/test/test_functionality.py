import os.path
import tailf
import tempfile


def test_nonexistent_file():
    with tempfile.TemporaryDirectory() as dirname:
        filename = os.path.join(dirname, "nonexistent.txt")
        with tailf.Tail(filename) as tail:
            events = list(iter(tail))
            assert len(events) == 0, "no events are expected"

            with open(filename, "wb") as f:
                events = list(iter(tail))
                assert len(events) == 0, "no events are expected"

                f.write(b"alpha")
                f.flush()
                events = list(iter(tail))
                assert b"".join(events) == b"alpha", "new data is expected"

                events = list(iter(tail))
                assert len(events) == 0, "no events are expected"


def test_preexisting_file():
    with tempfile.NamedTemporaryFile("w+b") as f:
        f.write(b"alpha")
        f.flush()
        with tailf.Tail(f.name) as tail:
            events = list(iter(tail))
            assert b"".join(events) == b"alpha", "pre-existing data is expected"

            events = list(iter(tail))
            assert len(events) == 0, "no events are expected"

            f.write(b"beta")
            f.flush()

            events = list(iter(tail))
            assert b"".join(events) == b"beta", "new data is expected"

            events = list(iter(tail))
            assert len(events) == 0, "no events are expected"


def test_truncate():
    with tempfile.NamedTemporaryFile("w+b") as f:
        with tailf.Tail(f.name) as tail:
            f.write(b"alpha")
            f.flush()
            list(iter(tail))  # skip "alpha"

            f.truncate(0)
            events = list(iter(tail))
            assert tailf.Truncated in events, "tailf.Truncated event is expected"
            assert all(
                not isinstance(event, (str, bytes)) for event in events
            ), "no data events are expected"

            f.seek(0)
            f.write(b"beta")
            f.flush()
            events = list(iter(tail))
            assert b"".join(events) == b"beta", "new data is expected"
