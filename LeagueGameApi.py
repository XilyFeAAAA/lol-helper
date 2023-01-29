import asyncio
import subprocess
import logging
import re
import httpx
import requests
from Enum.MessageEnum import *
from Enum.Structs import *


class LcuApi:
    def __init__(self):
        self.auth_token = None
        self.app_port = None
        self.url = None
        self.Clienturl = "127.0.0.1:2999"
        self.header = {
            'Accept': 'application/json',
            "Content-Type": "application/json",
            'Authorization': f'Basic {self.auth_token}'
        }

    def InitParam(self) -> bool:
        """
        初始化token和port，获得url
        """
        raw_output = subprocess.check_output(
            ['wmic', 'PROCESS', 'WHERE', "name='LeagueClientUx.exe'", 'GET', 'commandline']).decode('gbk')
        self.app_port = raw_output.split('--app-port=')[-1].split(' ')[0].strip('\"')
        self.auth_token = raw_output.split('--remoting-auth-token=')[-1].split(' ')[0].strip('\"')
        self.url = f"https://riot:{self.auth_token}@127.0.0.1:{self.app_port}"
        print(self.url)
        if 'CommandLine' in self.auth_token + self.app_port:
            logging.warning("Failed in retrieving token or port")
            return False
        return True

    async def doGet(self, route: str):
        """get请求"""
        print(self.url + route)
        async with httpx.AsyncClient(headers=self.header, verify=False) as client:
            req = await client.get(url=self.url + route)
            if req.status_code == 404:
                logging.error(f"[*]404 {req.json()['message']}  '{route}'")
            return req

    async def doPost(self, route: str, data: dict = None):
        """post请求"""
        async with httpx.AsyncClient(headers=self.header, verify=False) as client:
            req = await client.post(url=self.url + route, json=data)
            if req.status_code == 404:
                logging.error(f"[*]404 {req.json()['message']}  '{route}'")
            return req

    async def doDelete(self, route: str):
        """delete请求"""
        async with httpx.AsyncClient(headers=self.header, verify=False) as client:
            req = await client.delete(url=self.url + route)
            if req.status_code == 404:
                logging.error(f"[*]404 {req.json()['message']}  '{route}'")
            return req

    async def doPut(self, route: str, data: dict = None):
        """put请求"""
        async with httpx.AsyncClient(headers=self.header, verify=False) as client:
            req = await client.put(url=self.url + route, json=data)
            if req.status_code == 404:
                logging.error(f"[*]404 {req.json()['message']}  '{route}'")
            return req

    async def doPatch(self, route: str, data: dict = None):
        """patch请求"""
        async with httpx.AsyncClient(headers=self.header, verify=False) as client:
            req = await client.patch(url=self.url + route, json=data)
            if req.status_code == 404:
                logging.error(f"[*]404 {req.json()['message']}  '{route}'")
            return req

    async def GetClientState(self) -> bool:
        """RiotClientServices通讯正常"""
        response = await self.doGet(ROUTE.state).json()
        if response == 'Connected': return True
        else: return False

    async def GetUserInfo(self) -> Current_Summoner_Info:
        """
        获取英雄信息
        """
        req = (await self.doGet(ROUTE.current_summoner)).json()
        return Current_Summoner_Info(req['summonerId'], req['displayName'], req['puuid'], req['summonerLevel'])

    async def GetOnlineTime(self) -> float:
        """
        获取游戏时间
        """
        return (await self.doGet(ROUTE.allgamedata)).json()['gameData']['gameTime']

    async def Accept(self):
        """
        接受对局请求
        """
        return await self.doPost(ROUTE.accept_game)

    async def Decline(self):
        """
        拒绝对局请求
        """
        return await self.doPost(ROUTE.decline_game)

    async def Reconnect(self):
        """重新连接"""
        return await self.doPost(ROUTE.reconnect_game)

    async def Create_lobby(self, id: int):
        """创建房间"""
        data = {"queueId": id}
        return await self.doPost(ROUTE.lobby, data)

    async def Create_custom_lobby(self):
        """
        创建5v5训练营
        """
        custom = {
            'customGameLobby': {
                'configuration': {
                    'gameMode': 'PRACTICETOOL',
                    'gameMutator': '',
                    'gameServerRegion': '',
                    'mapId': 11,
                    'mutators': {'id': 1},
                    'spectatorPolicy': 'AllAllowed',
                    'teamSize': 5
                },
                'lobbyName': 'PRACTICETOOL',
                'lobbyPassword': ''
            },
            'isCustom': True
        }
        return await self.doPost(ROUTE.lobby, custom)

    async def Add_bots_team(self) -> bool:
        """添加机器人"""
        soraka = {
            'championId': 16,
            'botDifficulty': 'EASY',
            'teamId': '100'
        }
        return await self.doPost(ROUTE.lobby_bot, data=soraka)

    async def GrantAuthority(self, summonerId: int) -> bool:
        """赋予房间权限"""
        return await self.doPost(ROUTE.promote.format(summonerId))

    async def SearchMatch(self):
        """寻找对局"""
        return await self.doPost(ROUTE.search)

    async def CancelSearch(self):
        """取消寻找对局"""
        return await self.doDelete(ROUTE.search)

    async def Invite(self, summonerId: int) -> bool:
        """邀请玩家"""
        data = [
            {"toSummonerId": summonerId}
        ]
        return await self.doPost(ROUTE.invite, data=data)

    async def Revoke_Invite(self, summonerId: int) -> bool:
        """取消邀请"""
        data = [
            {"toSummonerId": summonerId}
        ]
        return await self.doPost(ROUTE.revoke_invite)

    async def Kick(self, summonerId: int) -> bool:
        """踢人"""
        return await self.doPost(ROUTE.kick.format(summonerId))

    async def SwitchTeam(self):
        """切换队伍"""
        return await self.doPost(ROUTE.switch)

    async def SetRank(self, rqueue, rtier, rdivision):
        """修改段位信息"""
        data = {
            "lol": {
                "rankedLeagueQueue": rqueue,
                "rankedLeagueTier": rtier,
                "rankedLeagueDivision": rdivision
            }
        }
        return await self.doPut(ROUTE.me, data)

    async def SetstatusMessage(self, msg):
        """设置状态信息"""
        data = {"statusMessage": msg}
        return await self.doPut(ROUTE.me, data)

    async def GetMe(self):
        """获取个人信息"""
        return await self.doGet(ROUTE.me).json()

    """
     * 生涯设置背景皮肤
     *
     * @param skinId 皮肤id,长度5位
     *               比如:其中 13006，这个ID分为两部分 13 和 006,
     *               13是英雄id,6是皮肤id(不足3位,前面补0)
    """

    async def SetBackgroundSkin(self, skinId: int):
        data = {
            "key": "backgroundSkinId",
            "value": skinId
        }
        return await self.doPost(ROUTE.summoner_profile, data)

    async def ChangeStatus(self, status: str):
        """改变状态"""
        data = {
            "availability": ClientStatus[status]
        }
        return await self.doPost(ROUTE.me, data)

    async def GetBackgroundSkin(self, heroId: int):
        """获取英雄皮肤"""
        return await self.doGet(ROUTE.champion_skin.format(heroId))

    async def msg2Room(self, roomId: str, msg: str):
        """组队房间发消息"""
        data = {
            "body": msg,
            "type": "chat"
        }
        return await self.doPost(ROUTE.chat_info.format(roomId), data)

    async def msg2Frient(self, name: str, msg: str):
        """好友发消息"""
        return await self.doGet(ROUTE.chat_frient.format(name, msg))

    async def GetRoomId(self):
        """获取选英雄房间id"""
        regex = r"(.*)?@"
        chatRoomName = (await self.doGet(ROUTE.BpSession)).json()['chatDetails']['chatRoomName']
        return re.search(regex, chatRoomName).group().replace("@", "")

    async def GetTeamDivision(self):
        """判断是红方还是蓝方"""
        return (await self.doGet(ROUTE.notification)).json()['mapSide']

    async def GetRoomSummonerId(self, roomId: str):
        """获取队友id"""
        summoner_list = []
        data = (await self.doGet(ROUTE.chat_info.format(roomId))).json()
        for i in data:
            if i['body'] == 'joined_room':
                summoner_id = i['fromSummonerId']
                if summoner_id not in summoner_list: summoner_list.append(i['fromSummonerId'])
        return summoner_list

    async def GetFrientList(self):
        """获取好友列表"""
        return (await self.doGet(ROUTE.friend_list)).json()

    async def GetInfoByName(self, name: str):
        """用户名查找玩家"""
        return (await self.doGet(ROUTE.summoner_by_name.format(name))).json()

    async def GetInfoById(self, id: str):
        """summoner_id查找玩家"""
        return (await self.doGet(ROUTE.summoner.format(id))).json()

    async def GetInfoByPuuid(self, puuid: str):
        """puuid查找玩家"""
        return (await self.doGet(ROUTE.summoner_by_puuid.format(puuid))).json()

    async def GetRank(self, puuid: str):
        """查找段位"""
        return (await self.doGet(ROUTE.rank.format(puuid))).json()

    async def GetScore(self, beginIdx: str, endIndex: str, id: str = None, puuid: str = None):
        """通过id、puuid查找对局记录"""
        return (await self.doGet(ROUTE.match_list_by_puuid.format(id if id else puuid, beginIdx, endIndex))).json()

    async def GetTeamPuuid(self):
        """获取对局双方puuid"""
        res = [[], []]
        resp = (await self.doGet(ROUTE.session)).json()
        print(resp)
        for i in resp['teamOne']:
            res[0].append(SummonerData(i['puuid'], i['summonerId']))
        for i in resp['teamTwo']:
            res[1].append(SummonerData(i['puuid'], i['summonerId']))
        return res

    async def SetPosition(self, first, second):
        """预选位"""
        position = {"firstPreference": Position[first], "secondPreference": Position[second]}
        return await self.doPut(ROUTE.position, position)

    async def Get_match_details(self, id: str):
        """通过游戏ID获取详细信息"""
        return (await self.doGet(ROUTE.match_detail.format(id))).json()

    async def Get_lobby(self) -> LobbyInfo:
        req = (await self.doGet(ROUTE.lobby)).json()
        lobby = LobbyInfo()
        lobby.chatRoomId = req['chatRoomId']
        gameMode = req['gameConfig']['gameMode']
        if gameMode == 'CLASSIC':
            if not req['gameConfig']['showPositionSelector']:
                lobby.gameMode = Gamemode.NORMAL
            elif req['gameConfig']['maxLobbySize'] == 2:
                lobby.gameMode = Gamemode.RANKED_SOLO_5x5
            else: lobby.gameMode = Gamemode.RANKED_FLIX_SR
        elif gameMode == 'ARAM':lobby.gameMode = Gamemode.ARAM
        elif gameMode == 'URF': lobby.gameMode = Gamemode.URF
        elif gameMode == 'TFT': lobby.gameMode = Gamemode.TFT
        return lobby

    async def Get_match_mode(self):
        """获得游戏模式"""
        return (await self.doGet(ROUTE.session)).json()["gameData"]["queue"]["type"]

    async def Ban_Pick(self):
        """自动bp"""
        gamemode = await self.Get_match_mode()
        if gamemode == 'RANKED_SOLO_5x5' or 'RANKED_FLIX_SR':
            await self.Pick

    async def Pick_Champion(self, champion_id: int, mode: int):
        session_info = (await self.doGet(ROUTE.BpSession)).json()
        if session_info["benchEnabled"]:  # 大乱斗
            if champion_id in session_info["benchChampionIds"]:
                await self.doPost(
                    ROUTE.swap_champion.format(champion_id))
            return
        for actions in session_info.get("actions", []):  # 峡谷
            for action in actions:
                if action["actorCellId"] == session_info["localPlayerCellId"] \
                        and action['type'] == 'pick' \
                        and action['isInProgress']:
                    return await self.doPatch(
                        ROUTE.bp_champion.format(action["id"]),
                        data={
                            "completed": True,
                            "type": "pick",
                            "championId": champion_id
                        }
                    )
