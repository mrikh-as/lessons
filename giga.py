import os
from gigachat import GigaChat
from dotenv import load_dotenv

load_dotenv()
giga = GigaChat(
    credentials=os.getenv("key"), scope="GIGACHAT_API_CORP", verify_ssl_certs=False
)
response = giga.chat("кто убил цезаря")
print(response.choices[0].message.content)
