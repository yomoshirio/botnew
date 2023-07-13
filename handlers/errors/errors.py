from aiogram.utils.exceptions import MessageNotModified, MessageToDeleteNotFound, InvalidQueryID, \
    ChatNotFound, BadRequest, MessageToEditNotFound, BotBlocked, TelegramAPIError, MessageCantBeDeleted, \
        RetryAfter
from loader import vip



#@vip.errors_handler()
async def errors_handler(update, exception):
    if isinstance(exception, MessageNotModified):
        return True
    
    if isinstance(exception, BadRequest):
        return True

    if isinstance(exception, MessageToEditNotFound):
        return True
    
    if isinstance(exception, BotBlocked):
        return True

    if isinstance(exception, ChatNotFound):
        return True

    if isinstance(exception, MessageCantBeDeleted):
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        return True

    if isinstance(exception, InvalidQueryID):
        return True

    if isinstance(exception, RetryAfter):
        return True

    if isinstance(exception, TelegramAPIError):
        return True
