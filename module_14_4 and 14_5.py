from fileinput import close

from aiogram import executor, Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import crud_functions as nb
from pyexpat.errors import messages

api = ""
bot = Bot(token=api)

dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup( resize_keyboard=True, one_time_keyboard=True)
botum = KeyboardButton(text='Рассчитать', resize_keyboard="100x100")
botum2 = KeyboardButton(text='Информация', resize_keyboard="100x100")
botum3 = InlineKeyboardButton(text='Купить', callback_data='Купить')
botum4 = InlineKeyboardButton(text='Регистрация', callback_data='Регистрация')
kb.row(botum, botum2, botum3, botum4)

oklaw = InlineKeyboardMarkup()
obot = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
obot1 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')

oklaw.row(obot, obot1)

okl = InlineKeyboardMarkup()
to = InlineKeyboardButton(text='Энергетик Clasic', callback_data="product_buying")
to1 = InlineKeyboardButton(text='Энергетик Granat', callback_data="product_buying")
to2 = InlineKeyboardButton(text='Энергетик Berry and Coconut', callback_data="product_buying")
to3 = InlineKeyboardButton(text='Энергетик Peach', callback_data="product_buying")
okl.row(to, to1, to2, to3)

class UserState(StatesGroup):
     age = State()
     growth = State()
     weight = State()

class RegistrationState(StatesGroup):
    id = State()
    username = State()
    email = State()
    age = State()
    balance = State('1000')

@dp.message_handler(commands=['start'])
async def all_massages(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup=kb)

@dp.message_handler(text='Информация')
async def main_menu(message):
    await message.answer('Язык програмирования: Python')
    await message.answer('Версия aiogram: 2.25.1')
    await message.answer('Автор: S.V.SH.')
    await message.answer('Дата: 19.11.2024', reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=oklaw)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    g = nb.get_all_products()
    k = 1
    for i in range(len(g)):
        y = open(f"{k}.jpg", "rb")
        await message.answer(f'Название: {g[i][1]} | Описание: {g[i][2]} | Цена: {g[i][3]}')
        await message.answer_photo(y)
        k = k+1
    await message.answer("Выберите продукт для покупки", reply_markup=okl)

@dp.callback_query_handler(text='product_buying')
async def get_formulas(call):
    await call.message.answer('Вы успешно приобрели продукт!')


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')

@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(qw=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(qw1=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(qw2=message.text)
    a = await state.get_data()
    i = 10*int(a['qw2']) + 6.25*int(a['qw1']) + 5 - 5*int(a['qw'])
    await message.answer(f"Ваша норма каллорий {i}")
    await state.finish()





@dp.message_handler(text="Регистрация")
async def set_age(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_growth(message, state):
    d = nb.is_included(message.text)
    if d is True:
        await state.update_data(qw = message.text)
        await RegistrationState.email.set()
        await message.answer("Введите свой email:")
    else:
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.email)
async def set_weight(message, state):
    await state.update_data(qw1=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def send_calories(message, state):
    await state.update_data(qw2=message.text)
    a = await state.get_data()
    nb.add_user(f"{a['qw']}", f"{a['qw1']}",f"{a['qw2']}", 10000)
    await message.answer("Регистрация прошла успешно")
    await state.finish()



if __name__=="__main__":
    executor.start_polling(dp, skip_updates=True)
