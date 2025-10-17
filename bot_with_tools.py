import os
from gigachat import GigaChatAsyncClient
from dotenv import load_dotenv
from telegram.ext import Application, MessageHandler, filters as f
from tools import llm_with_tools


async def llm_handler(update, context):
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
    answer = llm_with_tools.ask(prompt)

    history.append(f"Бот: {answer}")

    if len(answer) > 4000:
        answer = answer[:4000] + "..."

    await update.message.reply_text(answer)


def main():
    load_dotenv()
    app = Application.builder().token(os.getenv("tgkey")).build()
    app.add_handler(MessageHandler(f.TEXT, llm_handler))
    print("Бот запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
