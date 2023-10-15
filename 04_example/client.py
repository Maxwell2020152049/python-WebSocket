
import asyncio
import websockets
import json

from user import User


async def hello_world():
    uri = "ws://localhost:9002"
    async with websockets.connect(uri) as websocket:
        while True:
            # 输入想问候的名字
            username = input("What's your name? ")
            password = input("What's your password? ")
            email = input("What's your email? ")

            user = User(username=username, password=password, email=email)

            # 将该名字发送给服务器
            await websocket.send(json.dumps(user.dict()))

            # 接受服务器传来的名字
            greeting =  await websocket.recv()
            print(f"> {greeting}")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(hello_world())