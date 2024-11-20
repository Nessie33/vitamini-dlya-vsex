from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio


api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup()
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kb.add(button)
kb.add(button2)
kb.add(button3)

start_menu = InlineKeyboardMarkup()
now = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
now2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
start_menu.add(now)
start_menu.add(now2)

new_menu = InlineKeyboardMarkup()
new = InlineKeyboardButton(text='Product1', callback_data='product_buying')
new2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
new3 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
new4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
new_menu.add(new)
new_menu.add(new2)
new_menu.add(new3)
new_menu.add(new4)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start_message(message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text=['Рассчитать'])
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=start_menu)


@dp.message_handler(text=['Купить'])
async def buy_products(message):
    await get_buying_list(message)


async def get_buying_list(message):
    products = [
        {'name': 'Product1', 'discription': 'описание 1', 'price': 100, 'image': 'img1.png'},
        {'name': 'Product2', 'discription': 'описание 2', 'price': 200, 'image': 'img2.png'},
        {'name': 'Product3', 'discription': 'описание 3', 'price': 300, 'image': 'img3.png'},
        {'name': 'Product4', 'discription': 'описание 4', 'price': 400, 'image': 'img4.png'}
    ]
    for number in products:
        await message.answer(f'Название: {number["name"]} | Описание: {number["discription"]} | Цена: {number["price"]} * 100')
        await message.answer_photo(photo=open(number["image"], 'rb'))
    await message.answer('Выберите продукт для покупки:', reply_markup=new_menu)


@dp.callback_query_handler(text=['product_buying'])
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.callback_query_handler(text=['formulas'])
async def get_formulas(call):
    formula_message = (
        "Формула Миффлина-Сан Жеора:\n"
        "Для женщин: BMR = 10 * вес(кг) + 6.25 * рост(см) - 5 * возраст(лет) - 161"
    )
    await call.message.answer(formula_message)


@dp.callback_query_handler(text=['calories'])
async def set_age(call):
    await UserState.age.set()
    await call.message.answer('Введите свой возраст:')


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await UserState.growth.set()
    await message.answer('Введите свой рост:')


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await UserState.weight.set()
    await message.answer('Введите свой вес:')


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data.get('age'))
    growth = int(data.get('growth'))
    weight = int(data.get('weight'))
    calories = 10 * weight + 6.25 * growth - 5 * age - 161
    await message.answer(f'Ваша норма калорий: {calories:.2f} ккал.')
    await state.finish()


@dp.message_handler()
async def all_message(message):
    print('Введите команду /start, чтобы начать общение.')
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
