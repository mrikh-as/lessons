import os
from gigachat import GigaChat
from dotenv import load_dotenv

load_dotenv()

print("Привет! Это твоя программа.")

while True:
    phrase = input(
        """Введите вопрос. Если хотите завершить работу программы, напишите слово "выход" без кавычек.\n"""
    )
    if phrase.lower() == "выход":
        break

    with GigaChat(
        credentials=os.getenv("key"), scope="GIGACHAT_API_CORP", verify_ssl_certs=False
    ) as giga:
        response = giga.chat(phrase)
    print(response.choices[0].message.content)
