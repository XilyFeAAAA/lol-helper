import threading
from pathlib import Path
from Enum.Structs import *
from lcu_driver import Connector
from utils.LeagueGameApi import LcuApi
from utils.common import JsonReader
from modules.UserData import UserClass
import json


connector = Connector()
api = LcuApi()
user = UserClass()


@connector.ready
async def connect(connection):
    user.info = await api.GetUserInfo()
    print(f"玩家登陆:\n"
          f"名字:{user.info.displayName}\n"
          f"服务器:{user.info.environment}\n"
          f"等级:{user.info.summonerLevel}\n"
          f"summonerId:{user.info.summonerId}\n"
          f"puuid:{user.info.puuid}")


@connector.close
async def disconnect(_):
    await connector.stop()


@connector.ws.register(ROUTE.BpSession, event_types=('UPDATE',))
async def _(connection, event):
    # 自动bp
    if user.gamemode in ['ARAM_UNRANKED_5x5', 'URF']:
        return await api.ARAM_Select(event.data, user)
    elif user.gamemode in ['RANKED_FLIX_SR', 'RANKED_SOLO_5x5']:
        return await api.AutoBP(event.data, user)


@connector.ws.register(ROUTE.session, event_types=('UPDATE',))
async def _(connection, event):
    data = event.data
    if data['phase'] == StateEvent.Champselect:
        user.gamemode = data["gameData"]["queue"]["type"]


@connector.ws.register(ROUTE.game_flow, event_types=('UPDATE',))
async def _(connection, event):
    status = event.data
    if status == StateEvent.ReadyCheck:
        await api.Accept()  # 自动接受
    elif status == StateEvent.Reconnect:
        await api.Reconnect()  # 自动重连
    elif status == StateEvent.Champselect:
        if not user.sent:
            user.sent = True
            text = ""
            user.chatRoomId = await api.GetRoomId()
            roommateIds = await api.GetRoomSummonerId()
            for i in roommateIds:
                text += f"玩家:{(await api.GetInfoById(i)).displayName} kda:{await api.GetRankScore(id=i)}\n"
            print(text)
            # await api.msg2Room(info.chatRoomId, text)
    elif status == StateEvent.InProgress:
        pass
    elif status == StateEvent.EndOfGame:
        pass


@connector.ws.register(ROUTE.current_rune, event_types=('UPDATE',))
async def _(connection, event):
    pass
    # if not info.runed and event.data['isActive']:
    #     info.runed = True
    #     await api.SetRune(info.current_champion)

#threading.Thread(target=connector.start).start()
connector.start()
