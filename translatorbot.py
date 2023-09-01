import logging, os
from aiogram import Bot, Dispatcher, executor, types
from aiogram. dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram. types import InlineKeyboardMarkup, InlineKeyboardButton
from googletrans import Translator
from States import *
translator = Translator()
TOKEN = os.getenv('6574895378:AAGwEkfzaEeKa3_T5rZA3p0NM6szYEnuLjE')
logging.basicConfig(level=logging.INFO)
bot = Bot(token='6574895378:AAGwEkfzaEeKa3_T5rZA3p0NM6szYEnuLjE')
dp = Dispatcher(bot, storage=MemoryStorage())
ADMINS = []


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):
    words_choice = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text='Eng -> Ukr', callback_data='enuk')
    words_choice.add(button)
    button1 = InlineKeyboardButton(text='Ukr -> Eng', callback_data='uken')
    words_choice.add(button1)
    button2 = InlineKeyboardButton(text='Ukr -> Esp', callback_data='ukes')
    words_choice.add(button2)
    button3 = InlineKeyboardButton(text='Esp -> Ukr', callback_data='esuk')
    words_choice.add(button3)
    await message.answer(text='Привіт, Я - бот-перекладач,\n Надішліть повідомлення з текстом котрий хочете перекласти:', reply_markup=words_choice)
    await States.begin.set()


@dp.callback_query_handler(state=States.begin)
async def translation(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'uken':
        await callback_query.answer('Ок')
        await state.finish()
        await States.uken.set()
    elif callback_query.data == 'enuk':
        await callback_query.answer('Ок')
        await state.finish()
        await States.enuk.set()
    elif callback_query.data == 'ukes':
        await callback_query.answer('Ок')
        await state.finish()
        await States.ukes.set()
    elif callback_query.data == 'esuk':
        await callback_query.answer('Ок')
        await state.finish()
        await States.esuk.set()


@dp.message_handler(state=States.uken, content_types=types.ContentTypes.TEXT)
async def name_step(message: types.Message, state: FSMContext):
    await state.finish()
    translated_text = translator.translate(message.text, src='uk', dest='en').text
    await message.answer(translated_text)


@dp.message_handler(state=States.enuk, content_types=types.ContentTypes.TEXT)
async def name_step(message: types.Message, state: FSMContext):
    await state.finish()
    translated_text = translator.translate(message.text, src='en', dest='uk').text
    await message.answer(translated_text)


@dp.message_handler(state=States.ukes, content_types=types.ContentTypes.TEXT)
async def name_step(message: types.Message, state: FSMContext):
    await state.finish()
    translated_text = translator.translate(message.text, src='uk', dest='es').text
    await message.answer(translated_text)


@dp.message_handler(state=States.esuk, content_types=types.ContentTypes.TEXT)
async def name_step(message: types.Message, state: FSMContext):
    await state.finish()
    translated_text = translator.translate(message.text, src='es', dest='uk').text
    await message.answer(translated_text)

if __name__ == '__main__':
    executor.start_polling(dp)
