from aiogram import Bot, types
from aiogram import Dispatcher
from aiogram.filters import CommandStart, Command

import asyncio
# Create a bot instance
bot = Bot(token='6811357981:AAGHzQN0b5hdnGZXy8hx7bkt99sN-Q7hLSU')
dp = Dispatcher()

# Handler for the "/start" command
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    # Create a custom keyboard with the "Share Contact" button
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    share_contact_button = types.KeyboardButton(text="Share Contact", request_contact=True)
    keyboard.add(share_contact_button)

    # Send a message with the custom keyboard
    await message.reply("Please share your phone number:", reply_markup=keyboard)

# Handler for receiving the shared contact
@dp.message()
async def contact_handler(message: types.Message):
    # Access the shared contact information
    contact = message.contact
    phone_number = contact.phone_number

    # Process the phone number or perform any desired actions
    await message.reply(f"Thank you for sharing your phone number: {phone_number}")

# Start the bot


async def main():
    bot = Bot(token='6811357981:AAGHzQN0b5hdnGZXy8hx7bkt99sN-Q7hLSU')

    await dp.start_polling(bot)
    


if __name__ == "__main__":
    
    asyncio.run(main())
    