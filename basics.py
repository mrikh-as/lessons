import os
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from dotenv import load_dotenv


class Handler:
    def __init__(self):
        self.llm = GigaChat(
            credentials=os.getenv("key"),
            scope="GIGACHAT_API_CORP",
            verify_ssl_certs=False,
        )

    def do(self, string: str):
        print(string)


handler = Handler()
handler.do("кто ты воин")

handler.llm

var1 = "hello"
var2 = 4
deposit0 = []
deposit0.append("hello")
deposit1 = [
    "hi",
    3,
    GigaChat(
        credentials=os.getenv("key"),
        scope="GIGACHAT_API_CORP",
        verify_ssl_certs=False,
    ),
]
variable = deposit1[1]
for var3 in deposit1:
    print(type(var3))
deposit1.append("hello")


deposit2 = {
    "key1": "hi",
    "ke2": 3,
    "key3": GigaChat(
        credentials=os.getenv("key"),
        scope="GIGACHAT_API_CORP",
        verify_ssl_certs=False,
    ),
}
variable = deposit2["key1"]
for k, v in deposit2.items():
    print(f"Ключ:{k}, а тип значения: {type(v)}")
