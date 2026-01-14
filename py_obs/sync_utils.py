import asyncio
import threading


class _LoopRunner:
    def __init__(self):
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(
            target=self._loop.run_forever,
            daemon=True
        )
        self._thread.start()

    def run(self, coro):
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return future.result()


_loop_runner = _LoopRunner()


def _run(coro):
    return _loop_runner.run(coro)


class SyncProxy:
    def __init__(self, async_obj):
        self._async_obj = async_obj

    def __getattr__(self, name):
        attr = getattr(self._async_obj, name)

        if callable(attr):

            if asyncio.iscoroutinefunction(attr):
                def sync_wrapper(*args, **kwargs):
                    return _run(attr(*args, **kwargs))
                return sync_wrapper

            def method_wrapper(*args, **kwargs):
                result = attr(*args, **kwargs)

                if hasattr(result, "__dict__"):
                    return SyncProxy(result)

                return result

            return method_wrapper

        return attr
