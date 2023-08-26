from django.conf import settings
from telegram import Bot

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

def send_notification(receiver, message):
    bot.send_message(
        text=message,
        chat_id=receiver,
        parse_mode='Markdown'
    )

def unify_phone(raw_input: str):
    only_numbers = [number for number in str(raw_input) if number in '0123456789']
    only_numbers = ' '.join(only_numbers).split()

    if (11 >= len(only_numbers) >= 10) and (''.join(only_numbers[-10:-9]) in '789'):
        only_numbers = only_numbers[-10:]
        unified_phone_number = f"+7 ({''.join(only_numbers[:3])}) {''.join(only_numbers[3:6])}-{''.join(only_numbers[6:8])}-{''.join(only_numbers[8:10])}"
        return unified_phone_number
    else:
        return False