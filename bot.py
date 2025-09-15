# Main bot script
import os
import sys
import openai
import telegram
from telegram.ext import Updater, MessageHandler, Filters

# --- Configuration and Validation ---
# Get API keys from environment variables
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Check if the keys are present and exit if not
if not TELEGRAM_TOKEN:
    print("Error: The TELEGRAM_TOKEN environment variable is not set.")
    sys.exit(1)

if not OPENAI_API_KEY:
    print("Error: The OPENAI_API_KEY environment variable is not set.")
    sys.exit(1)

# Set up OpenAI API key
openai.api_key = OPENAI_API_KEY
# ------------------------------------


def get_gpt_response(prompt):
    """
    Get response from OpenAI GPT model.
    """
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Placeholder for GPT-5
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error getting response from OpenAI: {e}"

def reply_to_message(update, context):
    """
    Reply to user's message with a GPT-generated response.
    """
    user_message = update.message.text
    gpt_response = get_gpt_response(user_message)
    update.message.reply_text(gpt_response)

def main():
    """
    Main function to start the bot.
    """
    print("Starting bot...")
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_to_message))

    updater.start_polling()
    print("Bot is running.")
    updater.idle()

if __name__ == '__main__':
    main()
