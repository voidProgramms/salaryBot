from aiogram import types, Router, F, Bot
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.state import StatesGroup, State
import os
import json
import pytz
from datetime import datetime
from filters.chatTypeFilter import ChatTypeFilter
from keyboards.reply import markup
from keyboards.inline import periodButtons
from typing import Any

months = ["Января", "Февраля", "Марта", "Апреля", "Мая", "Июня", "Июля", "Августа", "Сентября", "Октября", "Декабря"]
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'salary.json')
timezone = pytz.timezone('Europe/Moscow')

class SalaryState(StatesGroup):
    day = State()


main_router = Router()
main_router.message.filter(ChatTypeFilter(['private', 'superuser']))


@main_router.message(StateFilter('*'), CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет ты в боте для подсчета твоей зп)\n",reply_markup=markup)

@main_router.message(F.text.lower() == "новый день")
async def newDay(message: Message, state: FSMContext):
    await message.answer("Какая сегодня выручка?")
    await state.set_state(SalaryState.day)

@main_router.message(SalaryState.day)
async def addMoney(message: Message, state: FSMContext):
    salary = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        salary: dict[int, dict[int, dict[int, int]]] = json.load(file)
        nowMonth: int = datetime.now(timezone).month
        nowDay: int = datetime.now(timezone).day
        try:
            revenue: int = int(message.text)
            userID:int = message.from_user.id
            if userID in salary.keys():
                if nowMonth in salary[userID].keys():
                    salary[userID][nowMonth][nowDay] = revenue
                else:
                    salary[userID][nowMonth] = {nowDay: revenue}
            else:
                salary[userID] = {
                    nowMonth: {
                        nowDay: revenue
                    }
                }
                await message.answer(f"Успешно сохранено: {message.text}Р на {nowDay} {months[nowMonth + 1]}", reply_markup=markup)
            await state.clear()
        except Exception as e:
            await message.answer("Введено не число(\nПовторите еще раз)")
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(salary, file, indent=4)
    
@main_router.message(F.text.lower() == "зп")
async def getPeriod(message: Message):
    await message.answer("Выберите период", reply_markup=periodButtons())

@main_router.callback_query(F.data.contains("date"))
async def getSalary(query: CallbackQuery):
    start, end, month = query.data.split(':')[1:]
    salary: list[str] = list()
    revenue: int = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        data: dict[int, dict[int, dict[int, int]]] = json.load(file)
        monthSalary: dict[int, dict[int, int]] = data[str(query.from_user.id)][month]
        for key in monthSalary.keys():
            if int(start) <= int(key) <= int(end):
                salary.append(f"{key} {months[int(month)]}: {monthSalary[key]}")
                revenue += monthSalary[key]
        shifts = len(salary)
        payForShifts = 2200 * shifts
        payForRevenue = revenue*0.05
        salary.append(f"Количество смен: {shifts} = 2200 * {shifts} = {payForShifts}")
        salary.append(f"5% от {revenue} = {payForRevenue}")
        salary.append(f"Итого: {payForShifts + payForRevenue}")
        await query.message.answer("\n".join(salary))

