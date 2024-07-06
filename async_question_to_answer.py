import json
import openai
from termcolor import colored
from async_queue import AsyncQueue
import control_flow_commands as cfc

async def loop(
        questions_queue: AsyncQueue,
        response_queue: AsyncQueue,
        gpt_config,
):
    
    async def call_gpt(messages: list, response_queue):
        response = await openai.ChatCompletion.acreate(
            model=gpt_config["model_type"],
            temperature=gpt_config["temperature"],
            messages=messages,
            #stream=True,
        )
        answer = response.choices[0].message.content
        # async for chunk in response:
        #     for choice in chunk["choices"]:
        #         chunk_message = choice["delta"]
        #         content = chunk_message.get("content", None)
        #         if content:
        #             for character in content:
        #                 sentence.append(character)
        #                 response_queue.enqueue(
        #                     json.dumps({
        #                         "reporter": "output_message",
        #                         "type": "answer",
        #                         "message": character
        #                     })
        #                 )
        # sentence_string = "".join(sentence).strip()
        # sentence_string = sentence_string.replace("\\n", "")
        response_queue.enqueue(
            json.dumps({
                "reporter": "output_message",
                "type": "full",
                "message": answer
            })
        )
        print("Answer:", colored(answer, "light_yellow"))
        return answer

    dialogue = [
        {
            "role": "system",
            "content": gpt_config['prompt'],
        }
    ]
    
    message = await call_gpt(dialogue, response_queue)
    response_queue.enqueue(
        json.dumps({
            "reporter": "output_message",
            "type": "full",
            "message": message
        })
    )

    dialogue.append(
        {
            "role": "assistant",
            "content": message,
        }
    )

    while True:
        data = await questions_queue.dequeue()
        if data == cfc.CFC_CHAT_STARTED:
            response_queue.enqueue(
                json.dumps({
                    "reporter": "output_message",
                    "type": "start_message",
                })
            )
        elif data == cfc.CFC_CHAT_STOPPED:
            response_queue.enqueue(
                json.dumps({
                    "reporter": "output_message",
                    "type": "stop_message",
                })
            )
        elif data:
            dialogue.append({"role": "user", "content": data})
            message = await call_gpt(dialogue, response_queue)
            dialogue.append({
                "role": "assistant",
                "content": message,
            })