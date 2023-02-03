import threading
import time
import willump
import asyncio
from Enum.Structs import *
from utils.LeagueGameApi import LcuApi
from modules.UserData import UserClass


class WebSocketListen:
    def __init__(self, user: UserClass):
        self.user = user
        self.api = LcuApi()

    def run(self):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.start())

    async def start(self):
        self.wllp = await willump.start()
        json_subscription = await self.wllp.subscribe('OnJsonApiEvent')
        json_subscription.filter_endpoint(ROUTE.BpSession, self.BpSession_func)
        json_subscription.filter_endpoint(ROUTE.session, self.Session_func)
        json_subscription.filter_endpoint(ROUTE.game_flow, self.Gameflow_func)
        while True:
            await asyncio.sleep(10)


    async def BpSession_func(self, data):
        if data['eventType'] != 'Update':
            return
        data = data['data']
        # 自动bp
        if self.user.gamemode in ['ARAM_UNRANKED_5x5', 'URF']:
            return await self.api.ARAM_Select(data, self.user)
        elif self.user.gamemode in ['RANKED_FLIX_SR', 'RANKED_SOLO_5x5']:
            return await self.api.AutoBP(data, self.user)

    async def Session_func(self, data):
        if data['eventType'] != 'Update':
            return
        data = data['data']
        if data['phase'] == StateEvent.Champselect:
            self.user.gamemode = data["gameData"]["queue"]["type"]
            print(self.user.gamemode)

    async def Gameflow_func(self, data):
        if data['eventType'] != 'Update':
            return
        status = data['data']
        print(status)
        if status == StateEvent.ReadyCheck:
            await self.api.Accept()  # 自动接受
        elif status == StateEvent.Reconnect:
            await self.api.Reconnect()  # 自动重连
        elif status == StateEvent.Champselect:
            if not self.user.sent:
                self.user.sent = True
                text = ""
                self.user.chatRoomId = await self.api.GetRoomId()
                roommateIds = await self.api.GetRoomSummonerId(self.user.chatRoomId)
                for i in roommateIds:
                    text += f"玩家:{(await self.api.GetInfoById(i)).displayName} kda:{await self.api.GetRankScore(id=i)}\n"
                print(text)
                # await self.api.msg2Room(info.chatRoomId, text)
        elif status == StateEvent.InProgress:
            pass
        elif status == StateEvent.EndOfGame:
            pass
# user = UserClass()
# ws = WebSocketListen(user)
# ws.run()
# if __name__ == '__main__':
#
#     p.start()
#     while 1:
#         time.sleep(5)
#     #b = threading.Thread(target=b).start()