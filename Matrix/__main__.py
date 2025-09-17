import sys, asyncio
import Matrix
from Matrix import BOTLOG_CHATID, HEROKU_APP, PM_LOGGER_GROUP_ID
from telethon import functions
from .Config import Config
from .core.logger import logging
from .core.session import sedub
from .utils import mybot, autoname, autovars, saves
from .utils import add_bot_to_logger_group, load_plugins, setup_bot, startupmessage, verifyLoggerGroup

LOGS = logging.getLogger("ســـورس تيبثــون")
cmdhr = Config.COMMAND_HAND_LER

try:
    LOGS.info("⌭ جـارِ تحميـل الملحقـات ⌭")
    sedub.loop.run_until_complete(autovars())
    LOGS.info("✓ تـم تحميـل الملحقـات .. بنجـاح ✓")
except Exception as e:
    LOGS.error(f"- {e}")

if not Config.ALIVE_NAME:
    try:
        LOGS.info("⌭ بـدء إضافة الاسـم التلقـائـي ⌭")
        sedub.loop.run_until_complete(autoname())
        LOGS.info("✓ تـم إضافة فار الاسـم .. بـنجـاح ✓")
    except Exception as e:
        LOGS.error(f"- {e}")

try:
    LOGS.info("⌭ بـدء تنزيـل تيبثــون ⌭")
    sedub.loop.run_until_complete(setup_bot())
    LOGS.info("✓ تـم تنزيـل ماتركس .. بـنجـاح ✓")
except Exception as e:
    LOGS.error(f"{str(e)}")
    sys.exit()

class CatCheck:
    def __init__(self):
        self.sucess = True
Catcheck = CatCheck()

try:
    LOGS.info("⌭ بـدء إنشـاء البـوت التلقـائـي ⌭")
    sedub.loop.run_until_complete(mybot())
    LOGS.info("✓ تـم إنشـاء البـوت .. بـنجـاح ✓")
except Exception as e:
    LOGS.error(f"- {e}")

try:
    LOGS.info("⌭ جـارِ تفعيـل الاشتـراك ⌭")
    sedub.loop.create_task(saves())
    LOGS.info("✓ تـم تفعيـل الاشتـراك .. بنجـاح ✓")
except Exception as e:
    LOGS.error(f"- {e}")


async def startup_process():
    async def MarkAsViewed(channel_id):
        from telethon.tl.functions.channels import ReadMessageContentsRequest
        try:
            channel = await sedub.get_entity(channel_id)
            async for message in sedub.iter_messages(entity=channel.id, limit=5):
                try:
                    await sedub(GetMessagesViewsRequest(peer=channel.id, id=[message.id], increment=True))
                except Exception as error:
                    print ("✅")
            return True

        except Exception as error:
            print ("✅")

    async def start_bot():
      try:
          List = ["Matrix","PPYNY","Matrixe1","MatrixS","MatrixHelp","Matrixklaesh","Matrix_Support"]
          from telethon.tl.functions.channels import JoinChannelRequest
          for id in List :
              Join = await sedub(JoinChannelRequest(channel=id))
              MarkAsRead = await MarkAsViewed(id)
              print (MarkAsRead, "✅")
          return True
      except Exception as e:
        print("✅")
        return False

    
    await verifyLoggerGroup()
    await load_plugins("plugins")
    await load_plugins("assistant")
    LOGS.info(f"⌔ تـم تنصيـب ماتركس بنجـاح ✓ \n⌔ لـ إظهـار الأوامــر أرسـل (.الاوامر)")
    await verifyLoggerGroup()
    await add_bot_to_logger_group(BOTLOG_CHATID)
    if PM_LOGGER_GROUP_ID != -100:
        await add_bot_to_logger_group(PM_LOGGER_GROUP_ID)
    await startupmessage()
    Catcheck.sucess = True
    return


sedub.loop.run_until_complete(startup_process())

if len(sys.argv) not in (1, 3, 4):
    sedub.disconnect()
elif not Catcheck.sucess:
    if HEROKU_APP is not None:
        HEROKU_APP.restart()
else:
    try:
        sedub.run_until_disconnected()
    except ConnectionError:
        pass
