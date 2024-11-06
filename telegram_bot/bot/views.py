from rest_framework.views import APIView
from rest_framework.response import Response
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from .models import UserRequest
from .serializers import UserRequestSerializer
import json
import asyncio
import threading
from rest_framework.views import APIView
from rest_framework.response import Response
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)

# Conversation states
CATEGORY, PRODUCT_CODE = range(2)

async def start(update: Update, context) -> int:
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    context.user_data["user_id"] = user_id
    context.user_data["user_name"] = user_name

    reply_keyboard = [['پوشاک', 'دیجیتال', 'خوراکی']]
    await update.message.reply_text(
        f"سلام {user_name}! لطفاً یکی از دسته‌بندی‌های زیر را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return CATEGORY

async def category(update: Update, context) -> int:
    user_choice = update.message.text
    context.user_data["service_category"] = user_choice

    await update.message.reply_text(f"لطفاً کد کالای مورد نظر خود را وارد کنید.")
    return PRODUCT_CODE

async def product_code(update: Update, context) -> int:
    product_code = update.message.text
    context.user_data["product_code"] = product_code

    # Save the data in the Django model
    user_request = UserRequest.objects.create(
        user_id=context.user_data["user_id"],
        user_name=context.user_data["user_name"],
        service_category=context.user_data["service_category"],
        product_code=product_code
    )

    # Serialize and print/save in DRF format
    serializer = UserRequestSerializer(user_request)
    print(serializer.data)

    await update.message.reply_text("درخواست شما با موفقیت ثبت شد. از شما متشکریم!")
    return ConversationHandler.END

async def cancel(update: Update, context) -> int:
    await update.message.reply_text('عملیات لغو شد. خداحافظ!')
    return ConversationHandler.END

# Telegram bot configuration
TOKEN = '7777543551:AAHJYYN3VwfC686y1Ir_aYewX1IzUMOlU68'
application = Application.builder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, category)],
        PRODUCT_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, product_code)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
application.add_handler(conv_handler)

class TelegramBotView(APIView):
    def post(self, request, *args, **kwargs):
        update = Update.de_json(request.data, application.bot)
        application.update_queue.put(update)
        asyncio.run(application.process_update(update))
        return Response({"status": "success"})
