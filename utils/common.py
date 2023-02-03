import asyncio
import json
from pathlib import Path

def JsonReader(path: Path):
    with open(path.absolute(), 'r', encoding='utf-8') as fp:
        return json.load(fp)

def GetAsyncRes(function):
    loop = asyncio.get_event_loop()
    get_future = asyncio.ensure_future(function)
    loop.run_until_complete(get_future)
    return get_future.result()