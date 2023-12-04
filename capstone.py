import asyncio
from aiogram.types import (Message, ReplyKeyboardMarkup, 
                           ReplyKeyboardRemove, KeyboardButton, 
                           InlineKeyboardButton, InlineKeyboardMarkup,
                           CallbackQuery)
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart
from aiogram import Dispatcher, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

dp = Dispatcher()

loggedInUsers = set()
registeredUsers = set()

class BookingStates(StatesGroup):
    done = State()
    onroute = State()
    source = State()
    destination = State()


class RegisterState(StatesGroup):
    fullname = State()
    phone = State()
    role = State()

    

    

@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    
    builder = InlineKeyboardBuilder()
    builder.button(text="Login \U0001F511", callback_data="login")
    builder.button(text="Register \U0001F4CB", callback_data="register")
    builder.button(text="Book Ride \U0001F697", callback_data="book")
    builder.button(text="History \U0001F4D6", callback_data="history")
    builder.button(text="Rate \U00002B50", callback_data="rate")
    
    builder.adjust(2, 2)
    mainMenu = builder.as_markup()
    
    await message.answer("Hello , How can i help you today ?", reply_markup=mainMenu)
    
@dp.callback_query()
async def menuHandler(call: CallbackQuery, state: FSMContext):
    
    match call.data:
        case "register":
            await state.set_state(RegisterState.fullname)
            await call.message.answer("Hello What is Your name ? ")
        case "login":
            await call.message.answer("logged in successfully")
        case "history":
            await call.message.answer("This Your history")
        case "book":
            await call.message.answer("what is your current location ? ")
        case "rate":
            
            await call.message.answer("")
    call.answer()  

@dp.callback_query()
async def handle_login( call: CallbackQuery):
    if call.data == "login":
        await call.message.answer("logged in successfuly")
    call.answer()


@dp.message(RegisterState.fullname)
async def registerPhone(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await state.set_state(RegisterState.role)
    
    sharePhone = ReplyKeyboardMarkup(
        keyboard= [[
            KeyboardButton(text="Share Phone \U0001F4DE", callback_data="sharephone", request_contact = True)
    
        ]],
        resize_keyboard=True
    )

    
    await message.answer("click the button below to share your phone number? ", reply_markup=sharePhone)


@dp.message(RegisterState.role)
async def registerRole(message: Message, state:  FSMContext):
    await state.update_data()
    await state.set_state(None)
    await message.answer(f"Hello there your phone number is {message.contact.phone_number}", reply_markup=ReplyKeyboardRemove())

@dp.message(Command("login"))
async def loginHandler(message: Message, state: FSMContext):
    pass


@dp.message(Command("bookride"))
async def rideBookingHandler(message: Message, state: FSMContext):
    pass




    





async def main():
    bot = Bot(token='6739333948:AAEk1TQtCQUmb-ry6ouSKA6-73uKGmOXX84')

    await dp.start_polling(bot)
    


if __name__ == "__main__":
    
    asyncio.run(main())
    