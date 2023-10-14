
import asyncio
import websockets
import time

cnt: int = 0

async def hello_world(name: str):
    global cnt
    for i in range(10):
        print(f"{name}: {cnt}")
        cnt += 1
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(hello_world("hwf"))
    asyncio.get_event_loop().run_until_complete(hello_world("jkl"))