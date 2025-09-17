import random
import asyncio
import re
import requests
import time
import psutil
from datetime import datetime
from platform import python_version

import sys
import typing
from heroku3 import from_key
from cachetools import cached, LRUCache

from telethon import version, events, types
from telethon.tl import types, functions
from telethon.tl.types import UserStatusOnline as onn
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.utils import get_display_name
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)

from . import StartTime, sedub, zedversion
from ..Config import Config
from ..helpers.functions import zedalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id
from ..utils import Zed_Dev
from ..core.logger import logging
from ..helpers.utils import _format
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..core.managers import edit_delete, edit_or_reply
from ..core.logger import logging
from . import BOTLOG, BOTLOG_CHATID, mention

Zel_Uid = sedub.uid
zed_dev = (7291869416, 6806861615)
Zed_Vvv = (6806861615, 7291869416)
LOGS = logging.getLogger(__name__)
vocself = True
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
HEROKU_API_KEY = Config.HEROKU_API_KEY
VIP_DATE = Config.OPEN_WEATHER_MAP_APPID


class Heroku:
    def __init__(self) -> None:
        self.name: str = HEROKU_APP_NAME
        self.api: str = HEROKU_API_KEY

    def heroku(self) -> typing.Any:
        _conn = None
        try:
            if self.is_heroku:
                _conn = from_key(self.api)
        except BaseException as err:
            LOGS.exception(err)
        return _conn

    @property
    @cached(LRUCache(maxsize=512))
    def stack(self) -> str:
        try:
            app = self.heroku().app(self.name)
            stack = app.info.stack.name
        except BaseException:
            stack = "none"
        return stack

    @property
    def is_heroku(self) -> bool:
        return bool(self.api and self.name)


def mask_email(email: str) -> str:
    at = email.find("@")
    return email[0] + "•" * int(at - 2) + email[at - 1 :]


@sedub.zed_cmd(pattern="(تفعيل البصمه الذاتيه|تفعيل البصمه الذاتية|تفعيل البصمة الذاتيه|تفعيل البصمة الذاتية)")
async def start_datea(event):
    global vocself
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in Zed_Dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @dev_blal - \n⎉╎**")
    zid = int(gvarstatus("ZThon_Vip"))
    if Zel_Uid != zid:
        return
    if vocself:
        return await edit_or_reply(event, "**⎉╎حفظ البصمه الذاتية التلقائي 🎙**\n**⎉╎مفعلـه .. مسبقـاً ✅**")
    vocself = True
    await edit_or_reply(event, "**⎉╎تم تفعيل حفظ البصمه الذاتية 🎙**\n**⎉╎تلقائياً .. بنجاح ✅**")

@sedub.zed_cmd(pattern="(تعطيل البصمه الذاتيه|تعطيل البصمه الذاتية|تعطيل البصمة الذاتيه|تعطيل البصمة الذاتية)")
async def stop_datea(event):
    global vocself
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in Zed_Dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @BBBlibot - @EiAbot\n⎉╎او التواصـل مـع احـد المشرفيـن @AAAl1l**")
    zid = int(gvarstatus("ZThon_Vip"))
    if Zel_Uid != zid:
        return
    if vocself:
        vocself = False
        return await edit_or_reply(event, "**⎉╎تم تعطيل حفظ البصمه الذاتية 🎙**\n**⎉╎الان صارت مو شغالة .. ✅**")
    await edit_or_reply(event, "**⎉╎حفظ البصمه الذاتية التلقائي 🎙**\n**⎉╎معطلـه .. مسبقـاً ✅**")

@sedub.on(events.NewMessage(func=lambda e: e.is_private and (e.audio or e.voice) and e.media_unread))
async def sddm(event):
    global vocself
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in Zed_Dev:
        return
    Matrixal = event.sender_id
    malath = sedub.uid
    if Matrixal == malath:
        return
    zid = int(gvarstatus("ZThon_Vip")) if gvarstatus("ZThon_Vip") else 0
    if Zel_Uid != zid:
        return
    if vocself:
        sender = await event.get_sender()
        username = f"@{sender.username}" if sender.username else "لا يوجد"
        chat = await event.get_chat()
        voc = await event.download_media()
        await sedub.send_file("me", voc, caption=f"[ᯓ 𝗭𝗧𝗵𝗼𝗻 - حفـظ البصمه الذاتيه 🎙](t.me/ZThon)\n⋆─┄─┄─┄─┄─┄─┄─⋆\n**⌔ مࢪحبـاً .. عـزيـزي 🫂\n⌔ تـم حفظ البصمه الذاتية .. تلقائياً ☑️** ❝\n**⌔ معلومـات المـرسـل :-**\n**• الاسم :** {_format.mentionuser(sender.first_name , sender.id)}\n**• اليوزر :** {username}\n**• الايدي :** `{sender.id}`")


@sedub.on(events.NewMessage(pattern="/vip"))
async def _(event):
    if not event.is_private:
        return

    user = await event.get_sender()

    # حالة اذا الرد على رسالة وكان المطور غير مسموح
    if event.reply_to and user.id in Zed_Dev and user.id not in Zed_Vvv:
        await event.reply(
            f"**- عـذراً عـزيـزي** [{user.first_name}](tg://user?id={user.id}) ✖️\n"
            "**- هـذا الامـر خـاص بمطـور السـورس فقـط 🚧**"
        )
        await event.delete()
        return

    # حالة اذا الرد على رسالة وكان المستخدم في لائحة Zed_Vvv
    if event.reply_to and user.id in Zed_Vvv:
        reply_msg = await event.get_reply_message()
        if not reply_msg:
            await event.reply("⚠️ لازم ترد على رسالة حتى أقدر أجيب معرف الشخص.")
            return

        # جلب الـ user_id بشكل آمن
        owner_id = None
        if getattr(reply_msg, "from_id", None):
            owner_id = getattr(reply_msg.from_id, "user_id", None)
        if not owner_id:
            owner_id = getattr(reply_msg, "sender_id", None)

        if not owner_id:
            await event.reply("⚠️ ما قدرت أجيب معرف المستخدم من الرسالة. تأكد إنها من حساب شخصي، مو قناة أو بوت.")
            return

        hk = Heroku()
        try:
            conn = hk.heroku()
            app = conn.app(hk.name)
        except Exception:
            return

        if Config.OPEN_WEATHER_MAP_APPID is not None:
            zzd = VIP_DATE
        elif gvarstatus("z_date") is not None:
            zzd = gvarstatus("z_date")
            zzt = gvarstatus("z_time")
            zedda = f"{zzd}┊{zzt}"
        else:
            zzd = f"{bt.year}/{bt.month}/{bt.day}"

        zzz = sedub.me
        Zname = f"{zzz.first_name} {zzz.last_name}" if zzz.last_name else zzz.first_name
        Zid = sedub.uid
        Zuser = f"@{zzz.username}" if zzz.username else "None"
        owner_name = f"[{Zname}](tg://user?id={Zid})"

        vip_caption = vip_temp
        caption = vip_caption.format(
            mention=owner_name,
            uuser=Zuser,
            uid=Zid,
            email=mask_email(app.owner.email),
            app_name=app.name,
            zedda=zzd
        )

        if owner_id == sedub.uid and owner_id not in Zed_Vvv:
            if gvarstatus("ZThon_Vip"):
                await event.reply(
                    f"**- عـزيـزي** [{user.first_name}](tg://user?id={user.id}) 🧞‍♂\n"
                    "**- الحساب مضاف للسورس المدفوع .. مسبقاً 🌟**"
                )
                await event.delete()
            else:
                await event.reply(caption)
                try:
                    messages = await sedub.get_messages(user.id, limit=1)
                    if messages:
                        latest_message = messages[0]
                        await sedub(functions.messages.UpdatePinnedMessageRequest(
                            peer=user.id,
                            id=latest_message.id,
                            unpin=False,
                            pm_oneside=False
                        ))
                except Exception as e:
                    return await event.reply(f"`{e}`")

                await event.reply(
                    f"**- بواسطـة** [{user.first_name}](tg://user?id={user.id}) 🧞‍♂\n"
                    f"**- تم اضافة** {owner_name}\n"
                    "**-لـ السورس المدفوع .. بنجـاح 🌟**\n"
                    "**- لـ تصفح الاوامـر المدفوعـه 💡**\n"
                    "**- ارسـل الامـر (** `.المميز` **)**"
                )
                addgvar("ZThon_Vip", owner_id)
                await event.delete()



@sedub.on(events.NewMessage(pattern="/zip"))
async def _(event):
    if not event.is_private:
        return
    user = await event.get_sender()
    if user.id in Zed_Dev:
        if gvarstatus("ZThon_Vip"):
            await event.reply(f"**- عـزيـزي** [{user.first_name}](tg://user?id={user.id}) 🧞‍♂\n**- الحساب مضاف للسورس المدفوع .. مسبقاً 🌟**")
        else:
            await event.reply(f"**- بواسطـة** [{user.first_name}](tg://user?id={user.id}) 🧞‍♂\n**- تم اضافة الحساب** `{Zel_Uid}` 🧚‍♂\n**- السورس المدفوع .. بنجـاح 🌟**")
            addgvar("ZThon_Vip", Zel_Uid)


vip_temp = """
┏───────────────┓
│ ◉ sᴏʀᴄᴇ  ɪs ʀᴜɴɴɪɴɢ ᴠɪᴘ
┣───────────────┫
│ ● Name  ➪ {mention}
│ ● User  ➪ {uuser}
│ ● Id  ➪ `{uid}`
│ ● Email  ➪ `{email}`
│ ● App  ➪ `{app_name}`
│ ● Date  ➪ `{zedda}`
┗───────────────┛
**◉ ملاحظات هامة ⚠️**

`¹- في حالة توقف تنصيبك المدفوع خلال اقل من شهر يتم إعادة تشغيله لك`

`²- في حال توقف تنصيبك قم بمراسلة نفس المشرف الذي نصب لك وتحلى بالصبر (لا تقم بازعاج المشرف أو الاستعجال لأن اغلب وقتنا مشغولين)`

`³- في حال تنصيبك عدى الشهر وتوقف لا يحق لك ان تطالب بتعويض لان مدة الضمان شهر فقط`

`⁴- جميع التنصيبات لا يتم ايقافها من قبلنا انما بسبب حظر او توقف حسابات هيروكو او السيرفر .. في حال طولت ع الشهر تنصيبك راح يظل شغال لحتى يتوقف بنفسه`
"""

@sedub.on(events.NewMessage(pattern="/dip"))
async def _(event):
    if not event.is_private:
        return
    user = await event.get_sender()
    if user.id in Zed_Dev and Zel_Uid in Zed_Dev:
        if gvarstatus("ZThon_Vip"):
            await event.reply(f"**- بواسطـة** [{user.first_name}](tg://user?id={user.id}) 🧞‍♂\n**- تم تنزيل الحساب من السورس المدفوع 🗑**")
            delgvar("ZThon_Vip")
            await event.delete()
        else:
            await event.reply(f"**- عـزيـزي** [{user.first_name}](tg://user?id={user.id}) 🧞‍♂\n**- هـذا الحساب ليس مرفوع بعـد 🧌**")
            await event.delete()

@sedub.on(events.NewMessage(pattern="/live"))
async def zalive(event):
    if not event.is_private:
        return
    user = await event.get_sender()
    if user.id not in Zed_Dev:
        return
    if Zel_Uid in Zed_Dev:
        return
    #reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    start = datetime.now()
    zedevent = await event.reply("**⎆┊جـاري .. فحـص بـوت ماتركـس**")
    await event.delete()
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    _, check_sgnirts = check_data_base_heal_th()
    if gvarstatus("z_date") is not None:
        zzd = gvarstatus("z_date")
        zzt = gvarstatus("z_time")
        zedda = f"{zzd}┊{zzt}"
    else:
        zedda = f"{bt.year}/{bt.month}/{bt.day}"
    Z_EMOJI = gvarstatus("ALIVE_EMOJI") or "✥┊"
    ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "** بـوت  ماتركـس 𝙎𝙀𝘿𝙏𝙃𝙊𝙈  يعمـل .. بنجـاح ☑️ 𓆩 **"
    ZED_IMG = gvarstatus("ALIVE_PIC")
    zed_caption = gvarstatus("ALIVE_TEMPLATE") or zed_temp
    caption = zed_caption.format(
        ALIVE_TEXT=ALIVE_TEXT,
        Z_EMOJI=Z_EMOJI,
        mention=mention,
        uptime=uptime,
        zedda=zzd,
        zzd=zzd,
        zzt=zzt,
        telever=version.__version__,
        zdver=zedversion,
        pyver=python_version(),
        dbhealth=check_sgnirts,
        ping=ms,
    )
    if ZED_IMG:
        ZED = [x for x in ZED_IMG.split()]
        PIC = random.choice(ZED)
        try:
            await event.client.send_file(event.chat_id, PIC, caption=caption) #reply_to=reply_to_id)
            await zedevent.delete()
        except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
            return await edit_or_reply(
                zedevent,
                f"**⌔∮ عـذراً عليـك الـرد ع صـوره او ميـديـا  ⪼  `.اضف صورة الفحص` <بالرد ع الصـوره او الميـديـا> ",
            )
    else:
        await event.reply(caption, link_preview=False)
        await zedevent.delete()

zed_temp = """
┏───────────────┓
│ ◉ sᴏʀᴄᴇ ᴢᴛʜᴏɴ ɪs ʀᴜɴɴɪɴɢ ɴᴏᴡ
┣───────────────┫
│ ● ɴᴀᴍᴇ ➪  {mention}
│ ●  ➪ {telever}
│ ● ᴘʏᴛʜᴏɴ ➪ {pyver}
│ ● ᴘʟᴀᴛғᴏʀᴍ ➪ 𐋏ᥱr᧐κᥙ
│ ● ᴘɪɴɢ ➪ {ping}
│ ● ᴜᴘ ᴛɪᴍᴇ ➪ {uptime}
│ ● ᴀʟɪᴠᴇ sɪɴᴇᴄ ➪ {zedda}
│ ● ᴍʏ ᴄʜᴀɴɴᴇʟ ➪ [ᴄʟɪᴄᴋ ʜᴇʀᴇ](https://t.me/BDB0B)
┗───────────────┛"""


async def get_all_private_chat_ids(limit=20):
    ids = []
    try:
        dialogs = await sedub.get_dialogs(limit=limit)
        for dialog in dialogs:
            if isinstance(dialog.entity, types.User):
                ids.append(dialog.entity.id)
    except Exception as e:
        async for dialog in sedub.iter_dialogs(limit=limit):
            if dialog.is_user:
                ids.append(dialog.entity.id)
    return ids

# لمراقبة عدة حسابات مخصصه
# سوف يتم تحديثه لاحقاً
# كود مهم جداً
async def get_private_chat_ids(user_id):
    ids = []
    try:
        dialogs = await sedub.get_dialogs()
        for dialog in dialogs:
            if isinstance(dialog.entity, types.User) and user_id == dialog.entity.id:
                ids.append(dialog.entity.id)
    except Exception:
        async for dialog in sedub.iter_dialogs(limit=limit):
            if dialog.is_user and user_id == dialog.entity.id:
                ids.append(dialog.entity.id)
    return ids


# يمكنك استخدام الدالة التالية للحصول على id حسابات الأشخاص المحددين
# سيتم تمرير قائمة بأسماء المستخدمين للدالة
# مثلا: ['username1', 'username2', ...]
"""
usernames = ['username1']
ids = await get_private_chat_ids(usernames)
"""

# بعد ذلك يمكنك استخدام ids للتحقق من حالة online وإرسال التنبيهات

#يتحقق من وجود خاص مع المستخدم
"""
async def check_private_chat_with_user(user_id):
    async for dialog in sedub.iter_dialogs():
        if dialog.is_user and dialog.entity.id == user_id:
            return True
    return False
"""

@sedub.zed_cmd(pattern="تفعيل الكاشف الذكي(?: |$)(.*)")
async def start_Matrixali(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in Zed_Dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @DEV_BLAL - **") 
    zid = int(gvarstatus("ZThon_Vip")) if gvarstatus("ZThon_Vip") else 0
    input_str = event.pattern_match.group(1)
    #if not input_str:
        #return await edit_or_reply(event, "**- ارسل الامر + اليوزر او الايدي**")
    reply_message = await event.get_reply_message()
    if not input_str and not reply_message:
        return await edit_or_reply(event, "**- بالـرد ع الشخص او باضافة معـرف/ايـدي الشخـص للامـر**")
    uid = None
    if input_str and not reply_message:
        if input_str.isnumeric():
            uid = input_str
        if input_str.startswith("@"):
            user = await event.client.get_entity(input_str)
            uid = user.id
    if input_str and reply_message:
        if input_str.isnumeric():
            uid = input_str
        if input_str.startswith("@"):
            user = await event.client.get_entity(input_str)
            uid = user.id
    if not input_str and reply_message:
        user = await event.client.get_entity(reply_message.sender_id)
        uid = user.id
    private_chat_ids = await get_private_chat_ids(uid)
    if uid not in private_chat_ids:
        return await edit_or_reply(event, "**⎉╎عـذرا عـزيـزي ..✖️**\n**⎉╎لايوجـد لديك خاص مسبقاَ**\n**⎉╎مع صاحب هذا الحساب**\n**⎉╎لـ مراقبـة حالة متصل لـ هـذا الشخص ☑️**")
    ZAZ = gvarstatus("ZAZ") and gvarstatus("ZAZ") != "false"
    if ZAZ and gvarstatus("UIU") == f"{uid}":
        privacy_settings = types.InputPrivacyValueAllowAll()
        privacy_key = types.InputPrivacyKeyStatusTimestamp()
        await sedub(functions.account.SetPrivacyRequest(key=privacy_key, rules=[privacy_settings]))
        await asyncio.sleep(2)
        await edit_or_reply(event, "**⎉╎إشعـارات الحالـة (متصـل) .. مفعـله مسبقـاً لمراقبـة حالة هذا الشخص ☑️**")
    else:
        privacy_settings = types.InputPrivacyValueAllowAll()
        privacy_key = types.InputPrivacyKeyStatusTimestamp()
        await sedub(functions.account.SetPrivacyRequest(key=privacy_key, rules=[privacy_settings]))
        await asyncio.sleep(2)
        addgvar("ZAZ", True)
        addgvar("UIU", f"{uid}")
        zzz = await event.client.get_entity(uid)
        Zname = f"{zzz.first_name} {zzz.last_name}" if zzz.last_name else zzz.first_name
        Zid = uid
        Zuser = f"@{zzz.username}" if zzz.username else "None"
        target = f"[{Zname}](tg://user?id={Zid})"
        await edit_or_reply(event, f"**⎉╎تم تفعيـل إشعـارات الحالـة (متصـل) .. بنجـاح ☑️**\n**⎉╎لـ مراقبـة الحسـاب** {target}")

@sedub.zed_cmd(pattern="(تعطيل الكاشف الذكي|تعطيل اشعارات الحالة)")
async def stop_Matrixali(event):
    ZAZ = gvarstatus("ZAZ") and gvarstatus("ZAZ") != "false"
    if ZAZ:
        addgvar("ZAZ", False)
        delgvar("UIU")
        await edit_or_reply(event, "**⎉╎تم تعطيـل إشعـارات الحالـة (متصـل) .. بنجـاح ☑️**")
    else:
        await edit_or_reply(event, "**⎉╎إشعـارات الحالـة (متصـل) .. معطلـه مسبقـاً ☑️**")


"""
@sedub.on(events.UserUpdate)
async def Matrixal_online_ai(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in Zed_Dev:
        return
    zid = int(gvarstatus("ZThon_Vip"))
    #if Zel_Uid != zid:
        #return
    if gvarstatus("ZAZ") == "false":
        return
    if gvarstatus("ZAZ") is None:
        return
    #private_chat_ids = await get_private_chat_ids(limit=50)
    #username = gvarstatus("UIU")
    #user = await sedub.get_entity(username)
    #user_id = user.id
    #if event.user_id == user_id:
    private_chat_ids = await get_all_private_chat_ids(limit=20)
    if event.user_id in private_chat_ids and event.user_id != sedub.uid:
        if event.online:
            user = await event.get_user()
            first_name = user.first_name
            last_name = user.last_name
            full_name = f"{user.first_name}{user.last_name}"
            full_name = full_name if last_name else first_name
            if BOTLOG:
                zaz = f"<b>⌔┊الحسـاب : </b>" 
                zaz += f'<a href="tg://user?id={user.id}">{full_name}</a>'
                zaz += f"\n<b>⌔┊اصبـح متصـل الان ⦿</b>"
                await sedub.send_message(Config.PM_LOGGER_GROUP_ID, zaz, parse_mode="html")
                    #f"<b>⌔┊الحسـاب :</b> <a href='tg://user?id={user.id}'>{full_name}</a>\n<b>⌔┊اصبـح متصـل الان ⦿</b>",
                #)
"""

#TARGET_USER_ID = 232499688  # استبدل هذا برقم معرف المستخدم الذي تريد مراقبته

@sedub.on(events.UserUpdate)
async def Matrixal_online_ai(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in Zed_Dev:
        return
    #zid = int(gvarstatus("ZThon_Vip"))
    #if Zel_Uid != zid:
        #return
    if gvarstatus("ZAZ") == "false":
        return
    if gvarstatus("ZAZ") is None:
        return
    if gvarstatus("UIU") is None:
        return
    TARGET_USER_ID = int(gvarstatus("UIU"))
    if event.user_id == TARGET_USER_ID and event.online:  # تحقق من أن المستخدم هو المستهدف وأنه متصل
        user = await event.get_user()
        first_name = user.first_name
        last_name = user.last_name
        full_name = f"{user.first_name}{user.last_name}"
        full_name = full_name if last_name else first_name
        if BOTLOG:
            zaz = f"<b>⌔┊الحسـاب : </b>" 
            zaz += f'<a href="tg://user?id={user.id}">{full_name}</a>'
            zaz += f"\n<b>⌔┊اصبـح متصـل الان ⦿</b>"
            await sedub.send_message(Config.PM_LOGGER_GROUP_ID, zaz, parse_mode="html")


@sedub.zed_cmd(pattern="المتصليين?(.*)")
async def _(e):
    if e.is_private:
        return await edit_or_reply(e, "**- عـذراً ... هـذه ليـست مجمـوعـة ؟!**")
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in Zed_Dev:
        return await edit_or_reply(e, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @DEV_BLAL**")
    chat = await e.get_chat()
    if not chat.admin_rights and not chat.creator:
        await edit_or_reply(e, "**- عـذراً ... يجب ان تكـون مشرفـاً هنـا ؟!**")
        return False
    zel = await edit_or_reply(e, "**- جـارِ الكشـف اونـلايـن ...**")
    zzz = e.pattern_match.group(1)
    o = 0
    zilzali = "𓆩 [𝗦𝗼𝘂𝗿𝗰𝗲 𝙎𝙀𝘿𝙏𝙃𝙊𝙈 - 🝢 - الڪـٓاشـف الذڪـٓي](t.me/BDB0B) 𓆪\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n**- تـم انتهـاء الكشـف .. بنجـاح ✅**\n**- قائمـة بعـدد الاعضـاء المتصليـن واسمائـهـم :**\n"
    xx = f"{zzz}" if zzz else zilzali
    zed = await e.client.get_participants(e.chat_id, limit=99)
    for users, bb in enumerate(zed):
        x = bb.status
        y = bb.participant
        if isinstance(x, onn):
            o += 1
            xx += f"\n- [{get_display_name(bb)}](tg://user?id={bb.id})"
    await e.client.send_message(e.chat_id, xx)
    await zel.delete()


MatrixalVip_Orders = (
"[ᯓ 𝙎𝙀𝘿𝙏𝙃𝙊𝙈 𝗩𝗶𝗽 🌟 الاوامــر المـدفـوعـة](t.me/bdb0b) .\n"
"⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
"**✾╎قـائمـة الاوامـر المـدفـوعـة الخاصـة بسـورس ماتركـس :** \n\n"
"`.همسه`\n"
"**⪼ لـ عمـل همسـه سريـة بالـرد ع شخص بكـل سهولـه 🧧**\n"
"**⪼ ايضاً يستطيـع الشخص المهموس له رد الهمسه بضغطة زر 🏷**\n\n\n"
"`.لايك`\n"
"**⪼ لـ إظهـار الايـدي بـ زر لايـك ♥️**\n"
"`.المعجبين`\n"
"**⪼ لـ جلب قائمـة بالاشخـاص الذين صوتوا بـ لايك ع كليشة الايـدي الخاصه بك 🤳**\n"
"`.مسح المعجبين`\n"
"**⪼ لـ مسح لايكات وقائمة معجبين حسابك 🖤**\n\n\n"
"`.مساعده`\n"
"**⪼ لـ عـرض ادوات الذكـاء الاصطنـاعـي 🧠**\n"
"**⪼ الادوات موجودة في لوحة المساعدة .. البعض منها مجاني والبعض الآخر مدفـوع 🏌‍♂**\n\n\n" 
"`.هاك`\n"
"**⪼ لـ عـرض اوامـر الاختـراق عبـر كـود تيرمكـس ☠**\n"
"**⪼ الاختـراق يدعـم كود تليثـون او بايروجـرام معـاً 🏌‍♂**\n\n\n"
"`.تفعيل الكاشف الذكي`\n"
"**⪼ بالـرد ع الشخـص او بإضافة ايـدي او يـوزر الشخـص للامـر**\n"
"**⪼ لـ تفعيـل إشعـارات كشـف ومراقبـة حسـاب شخـص متصـل 🛜**\n\n\n"
"`.تعطيل الكاشف الذكي`\n"
"**⪼ لـ تعطيـل إشعـارات كشـف الشخـص المتصل بالخـاص 🛃**\n\n\n"
"`.موقع`\n"
"**⪼ ارسـل الامـر (.موقع + الدولة + المحافظة/المدينة + اسم محل خدمي او تجاري)**\n"
"**⪼ مثــال (.موقع العراق بغداد المنصور مطعم الساعة)**\n"
"**⪼ لـ جـلب صـورة مباشـرة لـ الموقـع عبـر الاقمـار الصنـاعيـة 🗺🛰**\n\n\n"
"`.تفعيل البصمه الذاتيه`\n"
"**⪼ لـ تفعيـل حفـظ البصمـه الذاتيـه .. تلقائياً 🎙**\n\n\n"
"`.تعطيل البصمه الذاتيه`\n"
"**⪼ لـ تعطيـل حفـظ البصمـه الذاتيـه .. تلقائياً 🔇**\n\n\n"
"** رشق لايكات انستا 🖤**\n"
"**⪼ ارسـل الامـر** ( `.بوتي` )\n"
"**⪼ ثم اذهب الى بوت المساعد وارسل /start واختر زر رشق لايكات انستا 💘**\n"
"**⪼ لـ رشق 50 لايك لمنشور انستا كل يوم ♾**\n\n\n"
"** رشق مشاهدات تيك توك 👁‍🗨**\n"
"**⪼ ارسـل الامـر** ( `.بوتي` )\n"
"**⪼ ثم اذهب الى بوت المساعد وارسل /start واختر زر رشق مشاهدات تيك توك 👁‍🗨**\n"
"**⪼ لـ رشق 1000 مشاهده لفيديو تيك توك كل يوم ♾**\n\n\n"
"**⪼ ملاحظــه 💡:**\n"
"يتـم اضافـة المزيـد مـن الاوامـر المدفوعـة بشكـل متواصـل كـل تحديث 🏌‍♂\n\n"
"𓆩 [𝙎𝙀𝘿𝙏𝙃𝙊𝙈 𝗩𝗶𝗽 🌟](t.me/bdb0b) 𓆪"
)
#BiLaL
@sedub.zed_cmd(pattern="(المميز|vip)$")
async def zvip(event):
    if gvarstatus("ZThon_Vip") is None and Zel_Uid not in Zed_Dev:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @dev_blal **")
    if Zel_Uid in Zed_Dev:
        addgvar("ZThon_Vip", Zel_Uid)
    zid = int(gvarstatus("ZThon_Vip")) if gvarstatus("ZThon_Vip") else 0
    if Zel_Uid != zid:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @dev_blal**")
    return await edit_or_reply(event, MatrixalVip_Orders)

