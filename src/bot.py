import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from translator import translator

class PyTelTranslate:
    def __init__(self):
        load_dotenv()
        self.bot = telebot.TeleBot(token=os.getenv("BOT_TOKEN"), parse_mode="markdown")

        # Temporary user data: user_id -> {"text": "..."}
        self.user_data = {}

        # Supported languages
        self.languages = {
            "en": "English",
            "fa": "Persian",
            "fr": "French",
            "de": "German",
            "es": "Spanish",
            "ar": "Arabic",
            "ru": "Russian",
            "tr": "Turkish",
            "it": "Italian",
            "zh": "Chinese",
            "ja": "Japanese",
        }

        self.setup_handler()

    def setup_handler(self):
        self.bot.message_handler(commands=["start", "help"])(self.send_welcome)
        self.bot.message_handler(func=lambda m: True)(self.handle_message)
        self.bot.callback_query_handler(func=lambda call: True)(self.handle_callback)

    def send_welcome(self, message):
        self.bot.reply_to(
            message,
            "👋 Welcome to PyTel-Translate Bot!\n\n"
            "Send me any text and I will translate it for you."
        )

    def handle_message(self, message):
        user_id = message.from_user.id
        text = message.text.strip()

        # Save the text temporarily
        self.user_data[user_id] = {"text": text}

        # Build inline keyboard for target languages
        markup = InlineKeyboardMarkup(row_width=3)
        buttons = [
            InlineKeyboardButton(text=name, callback_data=f"{user_id}:{code}")
            for code, name in self.languages.items()
        ]
        markup.add(*buttons)

        self.bot.reply_to(
            message,
            "🌐 Choose the target language:",
            reply_markup=markup
        )

    def handle_callback(self, call):
        user_id = call.from_user.id
        data = call.data

        # Make sure the button belongs to the same user
        if not data.startswith(f"{user_id}:"):
            self.bot.answer_callback_query(call.id, "This option is not for you ❌")
            return

        _, target = data.split(":")
        original_text = self.user_data[user_id]["text"]

        translated = translator(original_text, target)

        self.bot.send_message(
            user_id,
            f"✅ Translated to {self.languages[target]}:\n\n{translated}"
        )

        # Clear user state
        self.user_data.pop(user_id, None)

    def run(self):
        print("🤖 Bot is running...")
        self.bot.infinity_polling(allowed_updates=["message", "callback_query"], restart_on_change=True)


if __name__ == "__main__":
    bot = PyTelTranslate()
    bot.run()
