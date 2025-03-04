from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from urllib.parse import urlparse, parse_qs
import logging
def parse_shopee_url(url: str):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    promotion_id = query_params.get('promotionId', [None])[0]
    signature = query_params.get('signature', [None])[0]
    return promotion_id, signature
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Halo! pemisah id & promotion id telah hadir.\n\n"
        "Kirim URL voucher Shopee ke sini"
    )
async def handle_message(update: Update, context: CallbackContext):
    message = update.message.text
    if "shopee.co.id/voucher/details" in message:
        promotion_id, signature = parse_shopee_url(message)

        if promotion_id:
            await update.message.reply_text(f"{promotion_id}")
        else:
            await update.message.reply_text("❌ Promotion ID tidak ditemukan.")
        if signature:
            await update.message.reply_text(f"{signature}")
        else:
            await update.message.reply_text("❌ Signature tidak ditemukan.")
    else:
            await update.message.reply_text("❌ URL tidak valid. Pastikan URL adalah voucher Shopee.")
def main():
    TOKEN = "7776325908:AAELkxGCsvd2uWXilEaNdtgpCZ4DRQmGFVE"
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()
if __name__ == "__main__":
    main()