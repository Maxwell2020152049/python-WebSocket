import asyncio
import websockets
import webSocketConfig
import json

# 用于保存当前连接到Websocket服务器的所有客户端
connected_clients = dict()

# token值关联存活时间
token_realate_keep_alive_time = dict()

# 清理WebScoket连接
async def cleanWebSocketConnect(token: str):
    # 通过token获取websocket
    webSocketSession = connected_clients.get(token)
    if webSocketSession:
        # 清除存活时间中的token
        del token_realate_keep_alive_time[token]
        # 清除连接
        del connected_clients[token]
        await webSocketSession.close()

# 减少WebSocket存活时间
# async def reducedKeepAliveTime():
#     tokens_to_remove = []
    
#     # 获取websocket存活时间字典
#     for key in token_realate_keep_alive_time.keys():
#         # 通过token修改存活时间
#         aliveTime = token_realate_keep_alive_time[key] - 1
#         token_realate_keep_alive_time[key] = aliveTime
#         print("token:" + key + ",存活时间还有：" + str(aliveTime))
#         if aliveTime == 0:
#             print("websocket存活时间内未获取到心跳，关闭连接,token:" + key)
#             # 清理WebSocket连接
#             await cleanWebSocketConnect(key)

async def reducedKeepAliveTime():
    tokens_to_remove = []
    
    # 逐个检查token
    for key in list(token_realate_keep_alive_time.keys()):
        # 通过token修改存活时间
        aliveTime = token_realate_keep_alive_time[key] - 1
        token_realate_keep_alive_time[key] = aliveTime
        print("token:" + key + ",存活时间还有：" + str(aliveTime))
        
        if aliveTime == 0:
            print("websocket存活时间内未获取到心跳，关闭连接,token:" + key)
            tokens_to_remove.append(key)
            await cleanWebSocketConnect(key)  # 你还可以在这里调用清理方法

    # 从字典中删除条目
    for token in tokens_to_remove:
        token_realate_keep_alive_time.pop(token, None)


# 创建定时任务一秒钟调用一次
async def webSocketSchedulingTask():
    while True:
        await reducedKeepAliveTime()
        await asyncio.sleep(1)

# 单播发送
async def unicastMessage(token: str, message: str):
    try:
        client = connected_clients.get(token)
        if client:
            data = {
                webSocketConfig.TYPE: "data",
                webSocketConfig.DATA: message
            }
            json_data = json.dumps(data)
            await client.send(json_data)
    except Exception as e:
        print('WS单播通信失败，token：' + token + "原因：" + e)
   
# 组播发送
async def multicastMessage(tokens: list, message: str):
    try:
        for token in tokens:
            client = connected_clients.get(token)
            data = {
                webSocketConfig.TYPE: "data",
                webSocketConfig.DATA: message
            }
            json_data = json.dumps(data)
            if client:
                await client.send(json_data)
    except Exception as e:
        print('WS组播通信失败，token：' + token + "原因：" + e)
    
# 广播发送
async def broadcastMessage(message: str):
    try:
        data = {
            webSocketConfig.TYPE: "data",
            webSocketConfig.DATA: message
        }
        json_data = json.dumps(data)
        for client in connected_clients.values():
            await client.send(json_data)
    except Exception as e:
        print('WS广播通信失败，原因：' + e)
    

# 心跳发送
async def heartBeatMessage(token: str):
    # 判断是否存在
    if token in connected_clients.keys():
        client = connected_clients.get(token)
        # 封装json数据
        data = {
            webSocketConfig.TYPE: webSocketConfig.HEART
        }
        json_data = json.dumps(data)
        await client.send(json_data)

# 接收消息
async def receiveMessage(websocket, token, webSocketAddress):
    try:
        async for message in websocket:
            parsed_message = json.loads(message)
            type = parsed_message['type']
            # 心跳发送
            if type == webSocketConfig.HEART:
                await heartBeatMessage(token)
            else:
                data = parsed_message['data']
                # await unicastMessage(token = token, message = "单播消息回复")
                await broadcastMessage(message = token + "说：大家好")
                print("收到data：" + data)
            # 恢复存活时间
            token_realate_keep_alive_time[token] = webSocketConfig.KEEP_ALIVE_TIME
            await websocket.send(f"You said: {parsed_message}")
    except Exception as e:
        print(f"WebSocket接收消息错误, 来源：address: {webSocketAddress} ip: {token}, 错误：{str(e)}")

# 处理websocket连接
async def handler(websocket, path):
    address = websocket.remote_address
    webSocketAddress = f"{address[0]}:{address[1]}"
    token = str(id(websocket))
    connected_clients[token] = websocket
    token_realate_keep_alive_time[token] = webSocketConfig.KEEP_ALIVE_TIME
    try:
        print("websocket:" + str(websocket))
        print(f"WebSocket建立连接 ========> address: {webSocketAddress} token: {token}")
        print(f"WebSocket当前在线人数： {len(connected_clients)}")
        # 开启心跳
        # await websocket.send(token+"我来了")
        # 接收消息
        await receiveMessage(websocket, token, webSocketAddress)
    except Exception as e:
        print(f"WebSocket建立连接错误, 来源：address: {webSocketAddress} ip: {token}, 错误：{str(e)}")
    finally:
        del connected_clients[token]
        del token_realate_keep_alive_time[token]
        print(f"WebSocket断开连接 ========> address: {webSocketAddress} token: {token}")
        print(f"WebSocket当前在线人数： {len(connected_clients)}")

# 创建WebSocket服务器
start_server = websockets.serve(handler, webSocketConfig.HOST, webSocketConfig.PORT)

# 获取当前的事件循环
loop = asyncio.get_event_loop()

# 将WebSocket服务器任务添加到事件循环
loop.run_until_complete(start_server)

# 将定时任务添加到事件循环
asyncio.ensure_future(webSocketSchedulingTask())

print(f"WebSocket server started on ws://{webSocketConfig.HOST}:{webSocketConfig.PORT}")

# 启动事件循环
loop.run_forever()
