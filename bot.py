# Main bot script
import os
import sys
from openai import AsyncOpenAI
from telegram.ext import Application, filters, MessageHandler

# --- Configuration and Validation ---
# Get API keys from environment variables
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

# Check if the keys are present and exit if not
if not TELEGRAM_TOKEN:
    print("Error: The TELEGRAM_TOKEN environment variable is not set.")
    sys.exit(1)

if not DEEPSEEK_API_KEY:
    print("Error: The DEEPSEEK_API_KEY environment variable is not set.")
    sys.exit(1)

# --- Client and Persona Initialization ---
# Initialize the async client for DeepSeek
# The OpenAI SDK is used here due to API compatibility
openai_client = AsyncOpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

# Define the persona for the AI model
SYSTEM_PROMPT = (
    "You are a helpful and polite technical support specialist for the company Data Trace. "
    "Your name is Jules. Answer questions clearly and concisely. "
    "You are powered by the DeepSeek AI model."
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
        return "I apologize, but I'm currently having trouble connecting to the AI service. Please try again in a moment."

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
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_to_message))

    print("Bot is running. Press Ctrl-C to stop.")
    application.run_polling()


if __name__ == '__main__':
    main()
