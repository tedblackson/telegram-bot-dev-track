import asyncio
import logging
import sys
from os import getenv
from typing import Any, Dict

from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

TOKEN = '6811357981:AAGHzQN0b5hdnGZXy8hx7bkt99sN-Q7hLSU'
form_router = Router()


from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

builder = InlineKeyboardBuilder()


builder.button(text="Yes", callback_data="yes")
builder.button(text = "No", callback_data="no")

builder.adjust(3, 2)

custom_key = builder.as_markup()

class Form(StatesGroup):
    name = State()
    like_bots = State()
    language = State()
    


@form_router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer("Hello, What is Your Name ?", reply_markup=ReplyKeyboardRemove())


@form_router.message(Command("cancel"))
@form_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext):
    cur_state = await state.get_state()
    
    if cur_state is None:
        return
    
    await state.clear()
    await message.answer("Cancelled", reply_markup=ReplyKeyboardRemove())


@form_router.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    
    await state.update_data(name = message.text)
    await state.set_state(Form.like_bots)
    await message.answer(f"Hello {message.text} Nice to meet You!, Do You Like To Write Bots ?", 
        reply_markup= custom_key)

@form_router.message(Form.like_bots, F.text.casefold() == "yes")
async def handle_like_bots(message:Message, state: FSMContext):
    await state.set_state(Form.language)
    await message.answer("Nice, What Programming Language Do You Use To Write Them? ", reply_markup=ReplyKeyboardRemove())


@form_router.message(Form.like_bots, F.text.casefold() == "no")
async def handle_not_like_bots(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Thats Sad :( ", reply_markup= ReplyKeyboardRemove())


@form_router.message(Form.language)
async def handle_language(message: Message):
    
    if message.text.casefold() == "python":
        await message.answer("Thats what I am built with")
    else:
        await message.answer(f"thats wonderful, you like to write bots using {message.text}")



async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    
    dp = Dispatcher()
    dp.include_router(form_router)
    
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())
    
    
    
    




    
    
    
        
    
    
    
    
    
    
    