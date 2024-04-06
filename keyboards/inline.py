from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime
import pytz
from filters.CallBackDataFilter import DateCallBack

timezone = pytz.timezone('Europe/Moscow')

days = [31, 29 if (lambda year: year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def periodButtons() -> InlineKeyboardMarkup:
    nowMonth = datetime.now(timezone).month
    nowDay = datetime.now(timezone).day
    startDay = 1
    endDay = 14
    firstDate = [startDay, endDay, nowMonth]
    secondDate = [endDay + 1, days[nowMonth], nowMonth]
    if nowDay < 15:
        firstDate = [endDay + 1, days[nowMonth - 1], nowMonth - 1]
        secondDate = [startDay, endDay, nowMonth]
    firstBtn = InlineKeyboardButton(text=f"{firstDate[0]}.{firstDate[-1]}-{firstDate[1]}.{firstDate[-1]}", callback_data=DateCallBack(startDay=firstDate[0], endDay=firstDate[1], month=firstDate[-1]).pack())
    secondBtn = InlineKeyboardButton(text=f"{secondDate[0]}.{secondDate[-1]}-{secondDate[1]}.{secondDate[-1]}", callback_data=DateCallBack(startDay=secondDate[0], endDay=secondDate[1], month=secondDate[-1]).pack())
    markup = InlineKeyboardBuilder()
    markup.add(firstBtn)
    markup.add(secondBtn)
    return markup.as_markup()


