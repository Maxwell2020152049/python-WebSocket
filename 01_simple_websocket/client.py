
import asyncio
import websockets


async def hello_world():
    uri = "ws://localhost:7890"
    async with websockets.connect(uri) as websocket:
        while True:
            # 输入想问候的名字
            name = input("What's your name? ")

            # 将该名字发送给服务器
            await websocket.send(name)

            # 接受服务器传来的名字
            greeting =  await websocket.recv()
            print(f"> {greeting}")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(hello_world())