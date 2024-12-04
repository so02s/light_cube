from aiogram.types import Message

async def send_msg(msg: Message, text: str) -> None:
    """
    Отправляет текстовое сообщение, разбивая его на части, если длина превышает 4000 символов.

    Параметры:
    msg (Message): Объект сообщения, через который будет отправлено сообщение.
    text (str): Текст, который необходимо отправить. Если длина текста превышает 4000 символов,
                он будет разбит на несколько сообщений.
    """
    while len(text) > 0:
        ans = text[:4000]
        await msg.answer(ans)
        text = text[4000:]