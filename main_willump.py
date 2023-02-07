import threading
import time
import willump
import asyncio
from loguru import logger
from Enum.Structs import *
from utils.LeagueGameApi import LcuApi
from modules.UserData import UserClass


class WebSocketListen:
    def __init__(self, user: UserClass, api):
        self.user = user
        self.api = api

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
        logger.info("客户端监听已启动")
        self.user.info = await self.api.GetUserInfo()
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
        elif self.user.gamemode in ['NORMAL', 'PRACTICE_GAME']:
            return await self.api.Classic_Select(data, self.user)

    async def Session_func(self, data):
        if data['eventType'] != 'Update':
            return
        data = data['data']
        if data['phase'] == StateEvent.Champselect:
            self.user.reset()
            self.user.gamemode = data["gameData"]["queue"]["type"]
            logger.info(f"当前游戏模式:{self.user.gamemode}")

    async def Gameflow_func(self, data):
        if data['eventType'] != 'Update':
            return
        status = data['data']
        if status == StateEvent.ReadyCheck:
            if self.user.accept_flag:
                await self.api.Accept()  # 自动接受
                logger.info("自动接受对局")
        elif status == StateEvent.Reconnect:
            if self.user.reconnect_flag:
                await self.api.Reconnect()  # 自动重连
                logger.info("自动重连")
        elif status == StateEvent.Champselect:
            if self.user.analze_flag:
                text = ""
                self.user.chatRoomId = await self.api.GetRoomId()
                roommateIds = await self.api.GetRoomSummonerId(self.user.chatRoomId)
                for i in roommateIds:
                    text += f"玩家:{(await self.api.GetInfoById(i)).displayName} kda:{await self.api.GetRankScore(id=i)}\n"
                logger.info(text)
                #await self.api.msg2Room(self.user.chatRoomId, text, Msg.chat)
        elif status == StateEvent.InProgress:
            pass
        elif status == StateEvent.EndOfGame:
            pass