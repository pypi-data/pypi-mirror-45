#!/usr/bin/env python3

import asyncio
import websockets


async def server_loop(websocket, path):
    while True:
        await asyncio.sleep(1)
        message = 'Hello world.'
        await websocket.send(message)

asyncio.get_event_loop().run_until_complete(websockets.serve(server_loop, 'localhost', 8765))
asyncio.get_event_loop().run_forever()
