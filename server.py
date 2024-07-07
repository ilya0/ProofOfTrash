import yaml
import openai
import asyncio

import async_question_to_answer
import async_socket_to_chat
import async_answer_to_socket
from fastapi import WebSocket
from termcolor import colored
from async_queue import AsyncQueue

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
config = yaml.safe_load(open("config.yaml"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

openai.api_key = config["gpt"]["api_key"]

@app.websocket("/chat/")
async def chat_client(websocket: WebSocket):
    print("In", colored("/accept_client", "light_cyan"))

    question_queue = AsyncQueue()
    response_queue = AsyncQueue()

    async_answer_to_socket_promise = async_answer_to_socket.loop(response_queue, websocket)
    async_question_to_answer_chat_promise = async_question_to_answer.loop(question_queue, response_queue, config["gpt"])
    socket_to_chat_promise = async_socket_to_chat.loop(websocket, question_queue, response_queue)

    await asyncio.gather(
        async_answer_to_socket_promise,
        socket_to_chat_promise,
        async_question_to_answer_chat_promise,
    )