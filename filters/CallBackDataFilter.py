from aiogram.filters.callback_data import CallbackData

class DateCallBack(CallbackData, prefix="date"):
    startDay: int
    endDay: int
    month: int
