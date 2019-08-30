# Credit to @udf and @jaskaran

import asyncio
from asyncio import sleep
from io import BytesIO
from telethon import events
from telethon import types
from telethon.errors import PhotoInvalidDimensionsError
from telethon.tl.functions.messages import SendMediaRequest

from userbot.events import register
from userbot import bot, CMD_HELP


@register(outgoing=True, pattern="^.ttf (.*)")
async def get(event):
    name = event.text[5:]
    m = await event.get_reply_message()
    with open(name, "w") as f:
        f.write(m.message)
    await event.delete()
    await bot.send_file(event.chat_id,name,force_document=True)


@register(outgoing=True, pattern="^.f2i(?: |$)(.*)")
async def on_file_to_photo(pics):
    await pics.edit("Converting Document image to Full Size Image\nPlease wait...")
    await sleep(2.5)
    await pics.delete()
    target = await pics.get_reply_message()
    try:
        image = target.media.document
    except AttributeError:
        return
    if not image.mime_type.startswith('image/'):
        return  # This isn't an image
    if image.mime_type == 'image/webp':
        return  # Telegram doesn't let you directly send stickers as photos
    if image.size > 10 * 2560 * 1440:
        return  # We'd get PhotoSaveFileInvalidError otherwise

    file = await pics.client.download_media(target, file=BytesIO())
    file.seek(0)
    img = await pics.client.upload_file(file)
    img.name = 'image.png'

    try:
        await pics.client(SendMediaRequest(
            peer=await pics.get_input_chat(),
            media=types.InputMediaUploadedPhoto(img),
            message=target.message,
            entities=target.entities,
            reply_to_msg_id=target.id
        ))
    except PhotoInvalidDimensionsError:
        return

CMD_HELP.update({
    "ttf": ".ttf <file name> Converts text into file"
})
CMD_HELP.update({
    "f2i": "
})
