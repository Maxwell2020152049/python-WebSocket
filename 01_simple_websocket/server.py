
import asyncio
import websockets

async def hello_world(websocket):
    while True:
        # 等待客户端发送名字
        name = await websocket.recv()
        print(f"< {name}")

        greeting = f"Hello, {name}"

        # 向客户端发送问候语
        await websocket.send(greeting)

if __name__ == "__main__":
    start_server = websockets.serve(hello_world, "localhost", 7890)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()