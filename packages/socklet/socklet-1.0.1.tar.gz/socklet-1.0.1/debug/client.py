#!/usr/bin/env python3

import asyncio
import websockets


async def client_loop(uri):
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print(message)

asyncio.get_event_loop().run_until_complete(client_loop('ws://localhost:8765'))
