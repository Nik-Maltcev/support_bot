# Main bot script
import os
import sys
import openai
from openai import AsyncOpenAI
from telegram.ext import Application, filters, MessageHandler

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

# --- Client and Persona Initialization ---
# Initialize the async OpenAI client
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# Define the persona for the AI model
SYSTEM_PROMPT = (
    "You are a helpful and polite technical support specialist for the company Data Trace. "
    "Your name is Jules. Answer questions clearly and concisely. "
    "You are powered by a GPT model, as GPT-5 is not yet publicly available."
)
# ------------------------------------

async def get_gpt_response(user_prompt):
    """
    Get a response from the OpenAI Chat Completion API using the defined persona.
    """
    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",  # Using a powerful model suitable for chat
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=300  # Increased max_tokens for more detailed support answers
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error getting response from OpenAI: {e}")
        return "I apologize, but I'm currently having trouble connecting to the AI service. Please try again in a moment."

async def reply_to_message(update, context):
    """
    Handle incoming text messages and reply with a GPT-generated response.
    """
    user_message = update.message.text
    gpt_response = await get_gpt_response(user_message)
    await update.message.reply_text(gpt_response)

def main():
    """
    Main function to set up and run the bot.
    """
    print("Starting bot...")

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add a handler for all text messages that are not commands.
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_to_message))

    # Run the bot until the user presses Ctrl-C
    print("Bot is running. Press Ctrl-C to stop.")
    application.run_polling()


if __name__ == '__main__':
    main()
