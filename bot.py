import os
from gigachat import GigaChatAsyncClient
from dotenv import load_dotenv
from telegram.ext import Application, MessageHandler, filters as f


async def llm_handler(update, context):
    try:
        user_id = update.message.from_user.id
        user_message = update.message.text
        if "users" not in context.user_data:
            context.user_data["users"] = {}
        if user_id not in context.user_data["users"]:
            context.user_data["users"][user_id] = []
        history = context.user_data["users"][user_id]
        history.append(f"Пользователь: {user_message}")
        if len(history) > 6:
            history = history[-6:]
            context.user_data["users"][user_id] = history

        await update.message.reply_chat_action("typing")

        history_text = "\n".join(history)
        prompt = f"""
Ты добрый друг. История разговора:
{history_text}
Отвечай кратко и по-дружески.
"""

        async with GigaChatAsyncClient(
            credentials=os.getenv("key"),
            scope="GIGACHAT_API_CORP",
            verify_ssl_certs=False,
        ) as giga:
            response = await giga.achat(prompt)

        answer = response.choices[0].message.content

        history.append(f"Бот: {answer}")

        if len(answer) > 4000:
            answer = answer[:4000] + "..."

        await update.message.reply_text(answer)

    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)}")


def main():
    load_dotenv()
    app = Application.builder().token(os.getenv("tgkey")).build()
    app.add_handler(MessageHandler(f.TEXT, llm_handler))
    print("Бот запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
