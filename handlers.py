from aiogram.types import Message, PreCheckoutQuery, ContentType, LabeledPrice
from cfg import bot, dp, SB_TOKEN
from keyboards import keyboard
from aiogram.types import ReplyKeyboardRemove


@dp.message_handler(commands='start')
async def start(msg: Message):
    await bot.send_message(msg.from_user.id, "Hello, this is the official <b>Nike-Web-Store</b> on Telegram! \nPlease fill out the customer form, and place your order.\n\n\n<u>"
                                             "Please use these card details for payment:</u>\nCard number - 4111 1111 1111 1111\nExpiration Date - 2024/12\n"
                                             "CSV code - 123\n3-D Secure - veres=y, pares=y\nVerification code 3-D Secure - 12345678" ,reply_markup=keyboard())


PRICE = {
    '1': [LabeledPrice(label='Nike MAG', amount=2490000)],
    '2': [LabeledPrice(label='Nike Air Max Bolt', amount=249000)],
    '3': [LabeledPrice(label='NIKE AIR JORDAN 1', amount=699000)],
    '4': [LabeledPrice(label='Adapt BB 2.0', amount=1790000)],
    '5': [LabeledPrice(label='Nike Air Max Plus', amount=449000)],
    '6': [LabeledPrice(label='Nike LeBron 12', amount=399000)]
}


@dp.message_handler(content_types='web_app_data')
async def buy_process(message):
    await bot.send_invoice(message.from_user.id,
                           title='Your order',
                           description='Nike sneakers',
                           provider_token=SB_TOKEN,
                           currency='RUB',
                           need_email=True,
                           need_phone_number=True,
                           prices=PRICE[f'{message.web_app_data.data}'],
                           start_parameter='example',
                           payload='some_invoice')


@dp.pre_checkout_query_handler(lambda q: True)
async def checkout_process(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(msg: Message):
    await bot.send_message(msg.from_user.id, '<b>Your order is ready</b>! Our couriers are already on their way to your address!🚴', reply_markup=ReplyKeyboardRemove())
