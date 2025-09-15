# Main bot script
import os
import sys
from openai import AsyncOpenAI
from telegram.ext import Application, filters, MessageHandler, CommandHandler

# --- Configuration and Validation ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

if not TELEGRAM_TOKEN:
    print("Error: The TELEGRAM_TOKEN environment variable is not set.")
    sys.exit(1)

if not DEEPSEEK_API_KEY:
    print("Error: The DEEPSEEK_API_KEY environment variable is not set.")
    sys.exit(1)

# --- Client and Persona Initialization ---
openai_client = AsyncOpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

# Russian persona for the AI model
SYSTEM_PROMPT = (
    "Ты — вежливый и полезный специалист технической поддержки компании Data Trace. "
    "Твоё имя — Андрей. Отвечай на вопросы четко и по делу. "
    "Ты работаешь на базе языковой модели DeepSeek."
)
# ------------------------------------

async def get_deepseek_response(user_prompt):
    """
    Get a response from the DeepSeek Chat Completion API using the defined persona.
    """
    try:
        response = await openai_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error getting response from DeepSeek API: {e}")
        return "К сожалению, в данный момент я не могу связаться с сервисом AI. Пожалуйста, попробуйте еще раз через мгновение."

# --- Command and Message Handlers ---

async def start(update, context):
    """Sends a welcome message when the /start command is issued."""
    welcome_message = "Напишите ваш вопрос и наш специалист ответит вам в ближайшее время."
    await update.message.reply_text(welcome_message)

async def reply_to_message(update, context):
    """
    Handle incoming text messages and reply with an AI-generated response.
    """
    user_message = update.message.text
    ai_response = await get_deepseek_response(user_message)
    await update.message.reply_text(ai_response)

def main():
    """
    Main function to set up and run the bot.
    """
    print("Starting bot...")

    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers for the /start command and regular text messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_to_message))

    print("Bot is running. Press Ctrl-C to stop.")
    application.run_polling()


if __name__ == '__main__':
    main()
