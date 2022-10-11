from aiogram.types import Message, PreCheckoutQuery, ContentType, LabeledPrice
from keyboards import keyboard
from aiogram.types import ReplyKeyboardRemove
from main import *
from aiogram.types import Message
from cfg import *


async def start(msg: Message):
    await bot.send_message(msg.from_user.id, "Привет! Это неофициальный бот <b>Nike-Web-Store</b> в Телеграм! \nПожалуйста заполните форму заказа, чтобы "
                                             "заказать кроссовки Nike, вы можете также поговорить с ботом! Просто напишите ему, и вы начнете разговор.\n\n\n<u>"
                                             "Пожалуйста, используйте эту карту для оплаты:</u>\nНомер карты - 4111 1111 1111 1111\nДата окончания действия - 2024/12\n"
                                             "CVC - 123\nПароль верефикации - 12345678\n\n\nПривет, давай пообщаемся?",reply_markup=keyboard())


PRICE = {
    '1': [LabeledPrice(label='Nike MAG', amount=2490000)],
    '2': [LabeledPrice(label='Nike Air Max Bolt', amount=249000)],
    '3': [LabeledPrice(label='NIKE AIR JORDAN 1', amount=699000)],
    '4': [LabeledPrice(label='Adapt BB 2.0', amount=1790000)],
    '5': [LabeledPrice(label='Nike Air Max Plus', amount=449000)],
    '6': [LabeledPrice(label='Nike LeBron 12', amount=399000)]
}


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


async def checkout_process(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def successful_payment(msg: Message):
    await bot.send_message(msg.from_user.id, '<b>Your order is ready</b>! Our couriers are already on their way to your address!🚴', reply_markup=ReplyKeyboardRemove())


async def lzt_dialogflow(message: Message):
    text_input = dialogflow.TextInput(text=message.text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    if response.query_result.fulfillment_text:
        await bot.send_message(message.from_user.id, response.query_result.fulfillment_text)
    else:
        await bot.send_message(message.from_user.id, "Я тебя не понимаю (наверное мой разработчик ненаучил меня понимать это)")


def register_web_hand(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')

    dp.register_message_handler(lzt_dialogflow)

    dp.register_message_handler(buy_process, content_types='web_app_data')
    dp.register_pre_checkout_query_handler(checkout_process, lambda q: True)
    dp.register_message_handler(successful_payment, content_types=ContentType.SUCCESSFUL_PAYMENT)