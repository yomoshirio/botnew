from aiogram import Dispatcher

from .filters import IsGroup, IsPrivate, IsAdmin, IsSubscribed, IsBan


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsBan)
    dp.filters_factory.bind(IsSubscribed)
