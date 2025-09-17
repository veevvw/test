#BiLaL
import time
import asyncio
import importlib
import logging
import glob
import os
import sys
import urllib.request
from datetime import timedelta
from pathlib import Path
from random import randint
from datetime import datetime as dt
from pytz import timezone
import requests
import heroku3

from telethon import Button, functions, types, utils
from telethon.tl.functions.channels import JoinChannelRequest, EditAdminRequest
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.types import ChatAdminRights
from telethon.errors import FloodWaitError, FloodError, BadRequestError

from Matrix import BOTLOG, BOTLOG_CHATID, PM_LOGGER_GROUP_ID

from ..Config import Config
from ..core.logger import logging
from ..core.session import sedub
from ..helpers.utils import install_pip
from ..helpers.utils.utils import runcmd
from ..sql_helper.global_collection import (
    del_keyword_collectionlist,
    get_item_collectionlist,
)
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from .pluginmanager import load_module
from .tools import create_supergroup
heroku_var = os.getenv("heroku_var", "default_value_here")
ENV = bool(os.environ.get("ENV", False))
LOGS = logging.getLogger("Matrix")
cmdhr = Config.COMMAND_HAND_LER
Zel_Dev = (7291869416)
Zed_Dev = (7291869416)
Zed_Vip = Zed_Dev
Zzz_Vip = Zed_Dev
zchannel = {"@BDB0B"}
heroku_api = "https://api.heroku.com"
if Config.HEROKU_APP_NAME is not None and Config.HEROKU_API_KEY is not None:
    Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
    app = Heroku.app(Config.HEROKU_APP_NAME)
    heroku_var = app.config()
else:
    app = None

if ENV:
    VPS_NOLOAD = ["vps"]
elif os.path.exists("config.py"):
    VPS_NOLOAD = ["heroku"]

bot = sedub
DEV = 1895219306

async def autovars(): 
    if "ENV" in heroku_var and "TZ" in heroku_var:
        return
    if "ENV" in heroku_var and "TZ" not in heroku_var:
        LOGS.info("جـارِ اضافـة بقيـة الفـارات .. تلقائيـاً")
        zzcom = "."
        zzztz = "Asia/Baghdad"
        heroku_var["COMMAND_HAND_LER"] = zzcom
        heroku_var["TZ"] = zzztz
        LOGS.info("تم اضافـة بقيـة الفـارات .. بنجـاح")
    if "ENV" not in heroku_var and "TZ" not in heroku_var:
        LOGS.info("جـارِ اضافـة بقيـة الفـارات .. تلقائيـاً")
        zzenv = "ANYTHING"
        zzcom = "."
        zzztz = "Asia/Baghdad"
        heroku_var["ENV"] = zzenv
        heroku_var["COMMAND_HAND_LER"] = zzcom
        heroku_var["TZ"] = zzztz
        LOGS.info("تم اضافـة بقيـة الفـارات .. بنجـاح")

async def autoname(): 
    if Config.ALIVE_NAME:
        return
    await bot.start()
    await asyncio.sleep(15)
    LOGS.info("جـارِ اضافة فـار الاسـم التلقـائـي .. انتظـر قليـلاً")
    zlzlal = await bot.get_me()
    zzname = f"{zlzlal.first_name}"
    tz = Config.TZ
    tzDateTime = dt.now(timezone(tz))
    zdate = tzDateTime.strftime('%Y/%m/%d')
    militaryTime = tzDateTime.strftime('%H:%M')
    ztime = dt.strptime(militaryTime, "%H:%M").strftime("%I:%M %p")
    zzd = f"‹ {zdate} ›"
    zzt = f"‹ {ztime} ›"
    if gvarstatus("z_date") is None:
        zd = "z_date"
        zt = "z_time"
        addgvar(zd, zzd)
        addgvar(zt, zzt)
    LOGS.info(f"تم اضافـة اسـم المستخـدم {zzname} .. بنجـاح")
    heroku_var["ALIVE_NAME"] = zzname


async def setup_bot():
    """
    To set up bot for zthon
    """
    try:
        await sedub.connect()
        config = await sedub(functions.help.GetConfigRequest())
        for option in config.dc_options:
            if option.ip_address == sedub.session.server_address:
                if sedub.session.dc_id != option.id:
                    LOGS.warning(
                        f"ايـدي DC ثـابت فـي الجلسـة مـن {sedub.session.dc_id}"
                        f" الـى {option.id}"
                    )
                sedub.session.set_dc(option.id, option.ip_address, option.port)
                sedub.session.save()
                break
        bot_details = await sedub.tgbot.get_me()
        Config.TG_BOT_USERNAME = f"@{bot_details.username}"
        # await sedub.start(bot_token=Config.TG_BOT_USERNAME)
        sedub.me = await sedub.get_me()
        sedub.uid = sedub.tgbot.uid = utils.get_peer_id(sedub.me)
        if Config.OWNER_ID == 0:
            Config.OWNER_ID = utils.get_peer_id(sedub.me)
    except Exception as e:
        if "object has no attribute 'tgbot'" in str(e):
            LOGS.error(f"- تـوكـن البـوت المسـاعـد غيـر صالـح او منتهـي - {str(e)}")
            LOGS.error("- شرح تغيير توكن البوت من فارات هيروكو ( https://t.me/BDB0B)")
        elif "Cannot cast NoneType to any kind of int" in str(e):
            LOGS.error(f"- كـود تيرمكـس غيـر صالـح او منتهـي - {str(e)}")
            LOGS.error("- شرح تغيير كود تيرمكس من فارات هيروكو ( https://t.me/BDB0B)")
        elif "was used under two different IP addresses" in str(e):
            LOGS.error(f"- كـود تيرمكـس غيـر صالـح او منتهـي - {str(e)}")
            LOGS.error("- شرح تغيير كود تيرمكس من فارات هيروكو ( https://t.me/BDB0B)")
        else:
            LOGS.error(f"كـود تيرمكس - {str(e)}")
        sys.exit()


async def mybot(): 
    if gvarstatus("z_assistant"):
        print("تم تشغيل البوت المسـاعـد .. بنجــاح ✅")
    else:
        Zname = Config.ALIVE_NAME
        Zid = Config.OWNER_ID
        zel_zal = f"[{Zname}](tg://user?id={Zid})"
        Zbotname = Config.TG_BOT_USERNAME
        botname = Config.TG_BOT_USERNAME
        fullname = f"{bot.me.first_name} {bot.me.last_name}" if bot.me.last_name else bot.me.first_name
        try:
            await bot.send_message("@BotFather", "/setinline")
            await asyncio.sleep(2)
            await bot.send_message("@BotFather", botname)
            await asyncio.sleep(2)
            await bot.send_message("@BotFather", fullname)
            await asyncio.sleep(3)
            await bot.send_message("@BotFather", "/setname")
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", botname)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", fullname)
            await asyncio.sleep(3)
            await bot.send_message("@BotFather", "/setuserpic")
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", botname)
            await asyncio.sleep(1)
            await bot.send_file("@BotFather", "Matrix/Matrix/logosed.jpg")
            await asyncio.sleep(3)
            await bot.send_message("@BotFather", "/setcommands")
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", botname)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", "start - start the bot")
            await asyncio.sleep(3)
            await bot.send_message("@BotFather", "/setabouttext")
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", botname)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", f"• البـوت المساعـد ♥️🦾\n• الخاص بـ  {fullname}\n• بوت خدمي متنـوع 🎁")
            await asyncio.sleep(3)
            await bot.send_message("@BotFather", "/setdescription")
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", botname)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", f"✧ البــوت الخدمـي المسـاعـد\n✧ الخـاص بـ {fullname}\n✧ أحتـوي على عـدة أقسـام خدميـه 🧸♥️\n 🌐 @BDB0B 🌐")
            await asyncio.sleep(2)
            await bot.send_message("@BotFather", f"**• إعـداد البـوت المسـاعـد .. تم بنجـاح ☑️**\n**• جـارِ الان بـدء تنصيب سـورس ماتركـس المدفـوع  ✈️. . .**\n\n**• ملاحظـه هامـه 🔰**\n- هـذه العمليه تحدث تلقائياً .. عبر جلسة التنصيب\n- لـذلك لا داعـي للقلـق 😇")
            addgvar("z_assistant", True)
            addgvar("z_assistant", True)
        except Exception as e:
            print(e)


async def startupmessage():
    """
    Start up message in telegram logger group
    """
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") != "false":
        delgvar("PMLOG")
    if gvarstatus("GRPLOG") and gvarstatus("GRPLOG") != "false":
        delgvar("GRPLOG")
    try:
        if BOTLOG:
            zzz = bot.me
            Zname = f"{zzz.first_name} {zzz.last_name}" if zzz.last_name else zzz.first_name
            Zid = bot.uid
            zel_zal = f"[{Zname}](tg://user?id={Zid})"
            Config.sedubLOGO = await sedub.tgbot.send_file(
                BOTLOG_CHATID,
                "https://telegra.ph/file/f821d27af168206b472ad.mp4",
                caption=f"**⌔ مرحبـاً عـزيـزي** {Zname} 🫂\n**⌔ تـم تشغـيل سـورس ماتركـس 🧸♥️**\n**⌔ التنصيب الخاص بـك .. بنجـاح ✅**\n**⌔ لـ تصفح قائمـة الاوامـر 🕹**\n**⌔ ارسـل الامـر** `{cmdhr}مساعده`",
                buttons=[[Button.url("𝗭𝗧𝗵𝗼𝗻 🎡 𝗨𝘀𝗲𝗿𝗯𝗼𝘁", "https://t.me/+kHkvf6hnqaJhYzVi")],[Button.url("إشتراكـات القسـم المدفـوع", "https://t.me/BDB0B")],[Button.url("حلـول الأخطـاء", "https://t.me/BDB0B"), Button.url("التحديثات المدفوعـة", "https://t.me/BDB0B")],[Button.url("MaTriX 𝗦𝘂𝗽𝗽𝗼𝗿𝘁", "https://t.me/BDB0B")],[Button.url("تواصـل مطـور السـورس", "https://t.me/O_P_G")]]
            )
    except Exception as e:
        LOGS.error(e)
        return None
    try:
        msg_details = list(get_item_collectionlist("restart_update"))
        if msg_details:
            msg_details = msg_details[0]
    except Exception as e:
        LOGS.error(e)
        return None
    try:
        if msg_details:
            await sedub.check_testcases()
            message = await sedub.get_messages(msg_details[0], ids=msg_details[1])
            text = message.text + "\n\n**•⎆┊تـم اعـادة تشغيـل السـورس بنجــاح 🧸♥️**"
            await sedub.edit_message(msg_details[0], msg_details[1], text)
            if gvarstatus("restartupdate") is not None:
                await sedub.send_message(
                    msg_details[0],
                    f"{cmdhr}بنك",
                    reply_to=msg_details[1],
                    schedule=timedelta(seconds=10),
                )
            del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
        return None


async def add_bot_to_logger_group(chat_id):
    """
    To add bot to logger groups
    """
    bot_details = await sedub.tgbot.get_me()
    try:
        await sedub(
            functions.messages.AddChatUserRequest(
                chat_id=chat_id,
                user_id=bot_details.username,
                fwd_limit=1000000,
            )
        )
    except BaseException:
        try:
            await sedub(
                functions.channels.InviteToChannelRequest(
                    channel=chat_id,
                    users=[bot_details.username],
                )
            )
        except Exception as e:
            LOGS.error(str(e))
    if chat_id == BOTLOG_CHATID:
        new_rights = ChatAdminRights(
            add_admins=False,
            invite_users=True,
            change_info=False,
            ban_users=False,
            delete_messages=True,
            pin_messages=True,
        )
        rank = "admin"
        try:
            await sedub(EditAdminRequest(chat_id, bot_details.username, new_rights, rank))
        except BadRequestError as e:
            LOGS.error(str(e))
        except Exception as e:
            LOGS.error(str(e))


async def saves():
   for Zcc in zchannel:
        try:
             await sedub(JoinChannelRequest(channel=Zcc))
             await asyncio.sleep(9)
        except FloodWaitError as zed: # تبعي
            wait_time = int(zed.seconds)
            waitime = wait_time + 1
            LOGS.error(f"Getting FloodWaitError ({zed.seconds}) - (ImportChatInviteRequest)")
            await asyncio.sleep(waitime) # Add a buffer
            continue
        except OverflowError:
            LOGS.error("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
            continue
        except Exception as e:
            if "too many channels" in str(e):
                print("- انت منضم في العديد من القنوات والمجموعات .. قم بالمغادرة من 10 او 15 قناة ثم قم بعمل إعادة تشغيل يدوي")
                continue
            else:
                continue
        await asyncio.sleep(1)


async def load_plugins(folder, extfolder=None):
    """
    To load plugins from the mentioned folder
    """
    if extfolder:
        path = f"{extfolder}/*.py"
        plugin_path = extfolder
    else:
        path = f"Matrix/{folder}/*.py"
        plugin_path = f"Matrix/{folder}"
    files = glob.glob(path)
    files.sort()
    success = 0
    failure = []
    for name in files:
        with open(name) as f:
            path1 = Path(f.name)
            shortname = path1.stem
            pluginname = shortname.replace(".py", "")
            try:
                if (pluginname not in Config.NO_LOAD) and (
                    pluginname not in VPS_NOLOAD
                ):
                    flag = True
                    check = 0
                    while flag:
                        try:
                            load_module(
                                pluginname,
                                plugin_path=plugin_path,
                            )
                            if shortname in failure:
                                failure.remove(shortname)
                            success += 1
                            break
                        except ModuleNotFoundError as e:
                            install_pip(e.name)
                            check += 1
                            if shortname not in failure:
                                failure.append(shortname)
                            if check > 5:
                                break
                else:
                    os.remove(Path(f"{plugin_path}/{shortname}.py"))
            except Exception as e:
                if shortname not in failure:
                    failure.append(shortname)
                os.remove(Path(f"{plugin_path}/{shortname}.py"))
                LOGS.info(
                    f"لا يمكنني تحميل {shortname} بسبب الخطأ {e}\nمجلد القاعده {plugin_path}"
                )
    if extfolder:
        if not failure:
            failure.append("None")
        await sedub.tgbot.send_message(
            BOTLOG_CHATID,
            f'Your external repo plugins have imported \n**No of imported plugins :** `{success}`\n**Failed plugins to import :** `{", ".join(failure)}`',
        )



async def verifyLoggerGroup():
    """
    Will verify the both loggers group
    """
    flag = False
    if BOTLOG:
        try:
            entity = await sedub.get_entity(BOTLOG_CHATID)
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(
                        "- الصلاحيات غير كافيه لأرسال الرسالئل في مجموعه فار ااـ PRIVATE_GROUP_BOT_API_ID."
                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(
                        "لا تمتلك صلاحيات اضافه اعضاء في مجموعة فار الـ PRIVATE_GROUP_BOT_API_ID."
                    )
        except ValueError:
            LOGS.error(
                "PRIVATE_GROUP_BOT_API_ID لم يتم العثور عليه . يجب التاكد من ان الفار صحيح."
            )
        except TypeError:
            LOGS.error(
                "PRIVATE_GROUP_BOT_API_ID قيمه هذا الفار غير مدعومه. تأكد من انه صحيح."
            )
        except Exception as e:
            LOGS.error(
                "حدث خطأ عند محاولة التحقق من فار PRIVATE_GROUP_BOT_API_ID.\n"
                + str(e)
            )
    else:
        try:
            descript = "لا تقم بحذف هذه المجموعة أو التغيير إلى مجموعة عامه (وظيفتهـا تخزيـن كـل سجـلات وعمليـات البـوت.)"
            photozed = await sedub.upload_file(file="BiLaL/malath/Zpic.jpg")
            _, groupid = await create_supergroup(
                "مجمـوعـة السجـل مـاتركـس", sedub, Config.TG_BOT_USERNAME, descript, photozed
            )
            addgvar("PRIVATE_GROUP_BOT_API_ID", groupid)
            print(
                "المجموعه الخاصه لفار الـ PRIVATE_GROUP_BOT_API_ID تم حفظه بنجاح و اضافه الفار اليه."
            )
            flag = True
        except Exception as e:
            if "can't create channels or chat" in str(e):
                print("- حسابك محظور من شركة تيليجرام وغير قادر على إنشاء مجموعات السجل والتخزين")
                print("- قم بالذهاب الى طريقة الحل عبر الرابط (https://t.me/heroku_error/22)")
                print("- لتطبيق الطريقة والاستمرار في التنصيب")
            else:
                print(str(e))

    if PM_LOGGER_GROUP_ID != -100:
        try:
            entity = await sedub.get_entity(PM_LOGGER_GROUP_ID)
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(
                        " الصلاحيات غير كافيه لأرسال الرسالئل في مجموعه فار ااـ PM_LOGGER_GROUP_ID."
                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(
                        "لا تمتلك صلاحيات اضافه اعضاء في مجموعة فار الـ  PM_LOGGER_GROUP_ID."
                    )
        except ValueError:
            LOGS.error("PM_LOGGER_GROUP_ID لم يتم العثور على قيمه هذا الفار . تاكد من أنه صحيح .")
        except TypeError:
            LOGS.error("PM_LOGGER_GROUP_ID قيمه هذا الفار خطا. تاكد من أنه صحيح.")
        except Exception as e:
            LOGS.error("حدث خطأ اثناء التعرف على فار PM_LOGGER_GROUP_ID.\n" + str(e))
    else:
        try:
            descript = "لا تقم بحذف هذه المجموعة أو التغيير إلى مجموعة عامه (وظيفتهـا تخزيـن رسـائل الخـاص.)"
            photozed = await sedub.upload_file(file="BiLaL/malath/Apic.jpg")
            _, groupid = await create_supergroup(
                "مجمـوعـة التخـزين", sedub, Config.TG_BOT_USERNAME, descript, photozed
            )
            addgvar("PM_LOGGER_GROUP_ID", groupid)
            print("تم عمل المجموعة التخزين بنجاح واضافة الفارات اليه.")
            flag = True
            if flag:
                executable = sys.executable.replace(" ", "\\ ")
                args = [executable, "-m", "Matrix"]
                os.execle(executable, *args, os.environ)
                sys.exit(0)
        except Exception as e:
            if "can't create channels or chat" in str(e):
                print("- حسابك محظور من شركة تيليجرام وغير قادر على إنشاء مجموعات السجل والتخزين")
                print("- قم بالذهاب الى طريقة الحل عبر الرابط (https://t.me/heroku_error/22)")
                print("- لتطبيق الطريقة والاستمرار في التنصيب")
            else:
                print(str(e))


async def install_externalrepo(repo, branch, cfolder):
    zedREPO = repo
    rpath = os.path.join(cfolder, "requirements.txt")
    if zedBRANCH := branch:
        repourl = os.path.join(zedREPO, f"tree/{zedBRANCH}")
        gcmd = f"git clone -b {zedBRANCH} {zedREPO} {cfolder}"
        errtext = f"There is no branch with name `{zedBRANCH}` in your external repo {zedREPO}. Recheck branch name and correct it in vars(`EXTERNAL_REPO_BRANCH`)"
    else:
        repourl = zedREPO
        gcmd = f"git clone {zedREPO} {cfolder}"
        errtext = f"The link({zedREPO}) you provided for `EXTERNAL_REPO` in vars is invalid. please recheck that link"
    response = urllib.request.urlopen(repourl)
    if response.code != 200:
        LOGS.error(errtext)
        return await sedub.tgbot.send_message(BOTLOG_CHATID, errtext)
    await runcmd(gcmd)
    if not os.path.exists(cfolder):
        LOGS.error("- حدث خطأ اثناء استدعاء رابط الملفات الاضافية .. قم بالتأكد من الرابط اولاً...")
        return await sedub.tgbot.send_message(BOTLOG_CHATID, "**- حدث خطأ اثناء استدعاء رابط الملفات الاضافية .. قم بالتأكد من الرابط اولاً...**",)
    if os.path.exists(rpath):
        await runcmd(f"pip3 install --no-cache-dir -r {rpath}")
    await load_plugins(folder="Matrix", extfolder=cfolder)
