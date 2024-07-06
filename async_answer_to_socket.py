from fastapi import WebSocket

from termcolor import colored
from async_queue import AsyncQueue

import control_flow_commands as cfc

import starlette.websockets as ws

async def loop(response_queue: AsyncQueue, websocket: WebSocket):
    while True:
        data = await response_queue.dequeue()

        if data == cfc.CFC_CLIENT_DISCONNECTED:
            break
        else:
            print(colored(f"Sending text data: {data}", "yellow"))
            try:
                await websocket.send_text(data)
            except ws.WebSocketDisconnect:
                break