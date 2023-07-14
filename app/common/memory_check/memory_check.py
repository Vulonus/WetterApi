import asyncio
import tracemalloc
from collections import OrderedDict
from datetime import datetime
import gc


def format_frame(frame):
    keys = ["f_code", "f_lineno"]
    return OrderedDict([(k, str(getattr(frame, k))) for k in keys])


def show_coro(coro):
    data = OrderedDict(
        [
            ("txt", str(coro)),
            ("type", str(type(coro))),
            ("done", coro.done()),
            ("cancelled", False),
            ("stack", None),
            ("exception", None),
        ]
    )
    if not coro.done():
        data["stack"] = [format_frame(x) for x in coro.get_stack()]
    else:
        if coro.cancelled():
            data["cancelled"] = True
        else:
            data["exception"] = str(coro.exception())
    return data


async def trace_top20_mallocs(sleep_time=30):
    """
    See https://docs.python.org/ko/3/library/tracemalloc.html
    """
    # has_snap_shot_before = False

    initial_snapshot = (
        tracemalloc.take_snapshot()
    )  # copy.deepcopy(tracemalloc.take_snapshot())
    while True:
        if tracemalloc.is_tracing():
            with open("malloc_logs.txt", "a", encoding="utf-8") as file:
                snapshot = tracemalloc.take_snapshot()
                top_stats = snapshot.compare_to(
                    initial_snapshot, "lineno", cumulative=True
                )  # snapshot.statistics("lineno")
                file.write(f"\n[ TOP 20 ] diff {datetime.now()}\n")
                file.write("Current GC Count: " + str(gc.get_count()) + "\n")
                traces = [str(x) for x in top_stats[:20]]
                for trace in traces:
                    file.write(trace + "\n")
            await asyncio.sleep(sleep_time)


async def show_all_unfinished_coroutine_status(sleep_time=30):
    cnt = 0
    while True:
        await asyncio.sleep(sleep_time)
        tasks = asyncio.all_tasks()
        with open("unfinished_coroutines.txt", "a", encoding="utf-8") as file:
            if len(tasks) != cnt:
                for task in tasks:
                    show_coro(task)
                    # file.write(json.dumps(formatted, indent=2))
                cnt = len(tasks)
            file.write(str(len(tasks)) + "\n")
