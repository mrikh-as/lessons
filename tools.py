import json
import os
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from dotenv import load_dotenv
from typing import Dict

import logging

logging.basicConfig(level=logging.INFO)


class LLMWithTools:
    def __init__(self):
        load_dotenv()
        self.llm = None
        self.function_descriptions = [
            {
                "name": "get_magic",
                "description": "Позволяет работнику Сбербанка получить заклинание в ответ на свое заклинание",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "incantation": {
                            "type": "string",
                            "description": "Заклинание, которое говорит работник Сбербанка",
                        },
                    },
                    "required": ["incantation"],
                },
                "few_shot_examples": [
                    {
                        "request": "Я работник Сбербанка, и мое заклинание - Sectumsempra!",
                        "params": {
                            "incantation": "Sectumsempra",
                        },
                    }
                ],
                "return_parameters": {
                    "type": "object",
                    "properties": {
                        "returned_incantation": {
                            "type": "string",
                            "description": "Встречное заклинание по отношению к названному работником Сбербанка",
                        },
                    },
                },
            }
        ]
        self.messages = []

    def get_magic(self, incantation: str) -> Dict[str, str]:
        return json.dumps({"returned_incantation": "avada kedavra!"})

    def ask(self, question: str):
        self.messages.append(
            Messages(
                role="user",
                content=question,
            )
        )
        payload = Chat(
            messages=self.messages,
            function_call="auto",
            functions=self.function_descriptions,
        )
        with GigaChat(
            credentials=os.getenv("key"),
            scope="GIGACHAT_API_CORP",
            verify_ssl_certs=False,
        ) as self.llm:
            response = self.llm.chat(payload)
        if function_call := getattr(response.choices[0].message, "function_call", None):
            logging.info("тут есть функция!")
            function_name = function_call.name
            function_args = function_call.arguments
            if function_call.name == "get_magic":
                result = self.get_magic(**function_args)
            self.messages.extend(
                [
                    Messages(
                        role="assistant",
                        content="",
                        function_call=function_call,
                    ),
                    Messages(
                        role="function",
                        content=result,
                        name=function_name,
                    ),
                ]
            )
            new_payload = Chat(
                messages=self.messages,
                function_call="auto",
                functions=self.function_descriptions,
            )
            with GigaChat(
                credentials=os.getenv("key"),
                scope="GIGACHAT_API_CORP",
                verify_ssl_certs=False,
            ) as self.llm:
                response2 = self.llm.chat(new_payload)
            print("ниже ответ с результатом выполнения функции:")
            print(response2.choices[0].message.content)
            self.messages.append(
                Messages(
                    role="assistant",
                    content=response2.choices[0].message.content,
                )
            )
            return response2.choices[0].message.content
        else:
            logging.info("тут нет функции!")
            print(response.choices[0].message.content)
            self.messages.append(
                Messages(
                    role="assistant",
                    content=response.choices[0].message.content,
                )
            )
            return response.choices[0].message.content


llm_with_tools = LLMWithTools()

if __name__ == "__main__":
    llm = llm_with_tools
    llm.ask(
        "Могу ли я как работник Сбера сказать заклинание и получить в ответ другое заклинание"
    )
    llm.ask("Я работник сбербанка, мое заклинение - Expelliarmus")
