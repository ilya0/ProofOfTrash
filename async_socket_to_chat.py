import json
from fastapi import WebSocket
from termcolor import colored
from async_queue import AsyncQueue
import starlette.websockets as ws
import control_flow_commands as cfc

async def loop(
    websocket: WebSocket, 
    questions_queue: AsyncQueue,
    respone_queue: AsyncQueue
):

    await websocket.accept()
    while True:
        try:
            message = await websocket.receive_text()

            if message == cfc.CFC_CHAT_STARTED:
                print(colored("Start message", "yellow"), message)
                questions_queue.enqueue(message)
                respone_queue.enqueue(json.dumps({
                    "reporter": "input_message",
                    "type": "start_message",
                    "message": message
                }))
            elif message == cfc.CFC_CHAT_STOPPED:
                print(colored("Stop message", "yellow"), message)
                questions_queue.enqueue(message)
                respone_queue.enqueue(json.dumps({
                    "reporter": "input_message",
                    "type": "stop_message",
                    "message": message
                }))
            else:
                print(colored("Message", "yellow"), message)
                questions_queue.enqueue(message)
                respone_queue.enqueue(json.dumps({
                    "reporter": "input_message",
                    "type": "question",
                    "message": message
                }))
        except ws.WebSocketDisconnect as e:
            print(colored("Socket closed", "yellow"))
            print(colored(str(e), "red"))
            break