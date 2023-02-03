import asyncio
import json
import subprocess
import logging
import re
import httpx
import requests
from Enum.MessageEnum import *
from Enum.Structs import *
import base64


class LcuApi:
    def __init__(self):
        self.auth_token = None
        self.app_port = None
        self.url = None
        self.Clienturl = "127.0.0.1:2999"
        self.InitParam()

    def InitParam(self):
        """
        初始化token和port，获得url
        """
        raw_output = subprocess.check_output(
            ['wmic', 'PROCESS', 'WHERE', "name='LeagueClientUx.exe'", 'GET', 'commandline']).decode('gbk')
        self.app_port = raw_output.split('--app-port=')[-1].split(' ')[0].strip('\"')
        self.auth_token = raw_output.split('--remoting-auth-token=')[-1].split(' ')[0].strip('\"')
        self.url = f"https://127.0.0.1:{self.app_port}"  # riot:{self.auth_token}@
        self.auth = httpx.BasicAuth('riot', self.auth_token)
        self.header = {
            'Connection': 'keep-alive',
            'Accept': 'application/json',
            "Content-Type": "application/json"
            # "Authorization": self.token
        }

    async def doGet(self, route: str, http2: bool = False):
        """get请求"""
        async with httpx.AsyncClient(auth=self.auth, headers=self.header, verify=False, http2=http2) as client:
            req = await client.get(url=self.url + route)
            if req.status_code == 404:
                logging.error(f"[*]404 {req.json()['message']}  '{route}'")
            return req

    async def doPost(self, route: str, http2: bool = False, **kwargs):
        """post请求"""
        async with httpx.AsyncClient(auth=self.auth, headers=self.header, verify=False, http2=http2) as client:
            if kwargs.get('data'):
                kwargs['data'] = json.dumps(kwargs['data'])
            req = await client.post(self.url + route, **kwargs)
            if req.status_code == 404:
                logging.error(f"[*]404 {req.json()['message']}  '{route}'")
            return req

    async def doDelete(self, route: str):
        """delete请求"""
        async with httpx.AsyncClient(auth=self.auth, headers=self.header, verify=False) as client:
            req = await client.delete(url=self.url + route)
            if req.status_code == 404:
                logging.error(f"[*]404 {req.json()['message']}  '{route}'")
            return req

    async def doPut(self, route: str, data: dict = None):
        """put请求"""
        async with httpx.AsyncClient(auth=self.auth, headers=self.header, verify=False) as client:
            req = await client.put(url=self.url + route, json=data)
            if req.status_code == 404:
                logging.error(f"[*]404 {req.json()['message']}  '{route}'")
            return req

    async def doPatch(self, route: str, data: dict = None):
        """patch请求"""
        async with httpx.AsyncClient(auth=self.auth, headers=self.header, verify=False) as client:
            req = await client.patch(url=self.url + route, json=data)
            if req.status_code == 404:
                logging.error(f"[*]404 {req.json()['message']}  '{route}'")
            return req

    async def GetEnvironment(self) -> str:
        """获取玩家大区"""
        return Environment[(await self.doGet(ROUTE.environment)).json()['environment']]

    async def GetClientState(self) -> bool:
        """RiotClientServices通讯正常"""
        response = (await self.doGet(ROUTE.state)).json()
        if response == 'Connected':
            return True
        else:
            return False

    async def GetUserInfo(self) -> SummonerInfo:
        """
        获取英雄信息
        """
        req = (await self.doGet(ROUTE.current_summoner)).json()
        print(req)
        env = await self.GetEnvironment()
        return SummonerInfo(req['summonerId'], req['displayName'], req['puuid'], req['summonerLevel'], req['profileIconId'], env)

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
        return await self.doPost(ROUTE.lobby, json=data)

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
        return await self.doPost(ROUTE.lobby, json=custom)

    async def Add_bots_team(self) -> bool:
        """添加机器人"""
        soraka = {
            'championId': 16,
            'botDifficulty': 'EASY',
            'teamId': '100'
        }
        return await self.doPost(ROUTE.lobby_bot, json=soraka)

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
        return await self.doPost(ROUTE.invite, json=data)

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

    async def ChangeStatus(self, status: str):
        """改变状态"""
        data = {
            "availability": ClientStatus[status]
        }
        return await self.doPost(ROUTE.me, json=data)

    async def GetBackgroundSkin(self, heroId: int):
        """获取英雄皮肤"""
        return await self.doGet(ROUTE.champion_skin.format(heroId))

    async def msg2Room(self, roomId: str, msg: str):
        """组队房间发消息"""
        data = {
            "body": msg,
            "type": "chat"
        }
        return await self.doPost(ROUTE.chat_info.format(roomId), json=data)

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

    async def GetRoomSummonerId(self, chatRoomId):
        """获取队友id"""
        data = (await self.doGet(ROUTE.conversation_msg.format(chatRoomId, http2=True))).json()
        summoners = []
        # Loop through team
        for summoner in data:
            print(summoner)
            if summoner["body"] == "joined_room":
                summoners.append(summoner["fromSummonerId"])
        return summoners

    async def GetFrientList(self):
        """获取好友列表"""
        return (await self.doGet(ROUTE.friend_list)).json()

    async def GetInfoByName(self, name: str):
        """用户名查找玩家"""
        req = (await self.doGet(ROUTE.summoner_by_name.format(name))).json()
        return SummonerInfo(req['summonerId'], req['displayName'], req['puuid'], req['summonerLevel'])

    async def GetInfoById(self, id: str):
        """summoner_id查找玩家"""
        req = (await self.doGet(ROUTE.summoner.format(id))).json()
        return SummonerInfo(req['summonerId'], req['displayName'], req['puuid'], req['summonerLevel'])

    async def GetInfoByPuuid(self, puuid: str):
        """puuid查找玩家"""
        req = (await self.doGet(ROUTE.summoner_by_puuid.format(puuid))).json()
        return SummonerInfo(req['summonerId'], req['displayName'], req['puuid'], req['summonerLevel'])

    async def GetRank(self, puuid: str):
        """查找段位"""
        return (await self.doGet(ROUTE.rank.format(puuid))).json()

    async def GetRankList(self, beginIdx: str, endIndex: str, id: str = None, puuid: str = None):
        """通过id、puuid查找对局记录"""
        if id:
            return (await self.doGet(ROUTE.match_list_by_id.format(id, beginIdx, endIndex))).json()
        else:
            return (await self.doGet(ROUTE.match_list_by_puuid.format(puuid, beginIdx, endIndex))).json()

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
        """获取组队界面信息"""
        req = (await self.doGet(ROUTE.lobby)).json()
        lobby = LobbyInfo()
        lobby.chatRoomId = req['chatRoomId']
        gameMode = req['gameConfig']['gameMode']
        if gameMode == 'CLASSIC':
            if not req['gameConfig']['showPositionSelector']:
                lobby.gameMode = Gamemode.NORMAL
            elif req['gameConfig']['maxLobbySize'] == 2:
                lobby.gameMode = Gamemode.RANKED_SOLO_5x5
            else:
                lobby.gameMode = Gamemode.RANKED_FLIX_SR
        elif gameMode == 'ARAM':
            lobby.gameMode = Gamemode.ARAM
        elif gameMode == 'URF':
            lobby.gameMode = Gamemode.URF
        elif gameMode == 'TFT':
            lobby.gameMode = Gamemode.TFT
        return lobby

    async def Get_match_mode(self):
        """获得游戏模式"""
        return (await self.doGet(ROUTE.session)).json()["gameData"]["queue"]["type"]

    async def ARAM_Select(self, session_info: json, conn):
        """大乱斗抢英雄"""
        if not conn.pick_flag:
            return
        benches = set()
        prefers = set(conn.swap_champions)
        if session_info["benchEnabled"]:  # 大乱斗
            for i in session_info["benchChampions"]:
                benches.add(i['championId'])
            # overlap = prefers.intersection(benches)
            # for champion_id in prefers.intersection(benches):
            for champion_id in benches:
                res = await self.doPost(ROUTE.swap_champion.format(champion_id))
                if not res.is_error:
                    break
            return

    async def ChampSelect(self, championId: int, actionId: int, patchType: str):
        """选择禁用英雄"""
        # print(f"[{patchType}] id: {actionId}")
        return await self.doPatch(
            ROUTE.bp_champion.format(actionId),
            data={
                "completed": True,
                "type": patchType,
                "championId": championId
            }
        )

    async def Rental_info(self):
        """获取战利品信息"""
        data = (await self.doGet(ROUTE.loot_map)).json()
        items = []
        for item in data:
            items.append(LootInfo(
                item['count'],
                item['itemDesc'],
                item['type'],
                item['lootName'],
                item['storeItemId'],
                item['disenchantValue'],
                item['redeemableStatus']
            ))
        return items

    async def Rental_dissolve(self, loot: LootInfo, repeat: int):
        """分解英雄碎片"""
        """
        info = LootInfo(1,"",LootType.champion_rental,"CHAMPION_RENTAL_11",1,1)
		await api.Rental_dissolve(info,1)
        """
        data = [loot.lootName]
        route = ROUTE.champion_rental if loot.type == LootType.champion_rental else ROUTE.skin_rental
        return await self.doPost(route.format(repeat), data=data)

    async def SetRune(self, champion: ChampionInfo):
        """自动配置符文"""
        runes = requests.get(f'https://www.bangingheads.net/runes?champion={champion.championId}').json()
        page = (await self.doGet(ROUTE.current_rune)).json()
        if 'errorCode' not in page:
            await self.doDelete(f'/lol-perks/v1/pages/{page["id"]}')
        return await self.doPost(ROUTE.page, json={
            "name": "Automatic rune configuration",
            "primaryStyleId": runes['primaryTree'],
            "subStyleId": runes['secondaryTree'],
            "selectedPerkIds": runes['perks'],
            "current": True
        })

    """
     * @param skinId 皮肤id,长度5位
     *               比如:其中 13006，这个ID分为两部分 13 和 006,
     *               13是英雄id,6是皮肤id(不足3位,前面补0)
     */
    """

    async def SetBackgroundSkin(self, skinId: int):
        """生涯设置背景皮肤"""
        data = {
            "backgroundSkinId": skinId
        }
        return await self.doPost(ROUTE.summoner_profile, json=data)

    async def GetRankScore(self, id: str = None, puuid: str = None):
        """获取kda"""
        count: int = 5
        data = await self.GetRankList(beginIdx=0, endIndex=count, id=id, puuid=puuid)
        scores = 0
        for rank in data['games']['games']:
            # print(rank)
            stats = rank['participants'][0]['stats']
            info = RankInfo(
                stats['kills'],
                stats['deaths'],
                stats['assists'],
                stats['firstBloodKill'],
                stats['pentaKills'],
                stats['quadraKills'],
                stats['tripleKills'],
                stats['win']
            )
            scores += info.Calculate()
        return round(scores / count, 2)

    async def Reroll(self):
        """随机英雄"""
        return await self.doPost(ROUTE.reroll)

    async def sendNotifications(self, title: str, details: str):
        """发送notification"""
        data = {
            'backgroundUrl': '',
            'created': '',
            'critical': True,
            'data': {
                'details': details,
                'title': title,
            },
            'detailKey': 'pre_translated_details',
            'dismissible': True,
            'expires': '',
            'iconUrl': '',
            'id': 0,
            'source': '',
            'state': 'toast',
            'titleKey': 'pre_translated_title',
            'type': 'ranked_summary',
        }
        return await self.doPost(ROUTE.notification, json=data)

    async def AutoBP(self, data: json, conn):
        """自动BP"""
        if not conn.pick_flag and not conn.ban_flag:
            return
        cellId: int = None
        position: str = None
        for order in data['myTeam']:
            if order['summonerId'] == conn.info.summonerId:
                cellId = order['cellId']
                position = order['assignedPosition']
                break
        if position is None:
            return
        actions = data['actions']
        if data['timer']['phase'] == 'PLANNING':
            return
        if data['timer']['phase'] == 'BAN_PICK':
            # ban
            if conn.ban_flag:
                banActionId: int = None
                for action in actions[0]:
                    if action['actorCellId'] == cellId:
                        banActionId = action['id']
                        if not action['completed'] and action['isInProgress']:
                            bannable = set((await self.doGet(ROUTE.bannable)).json())  # 可ban
                            bans = set(conn.ban_champions[position])  # 想ban
                            for ban in bans.intersection(bannable):  # 并集
                                res = await self.ChampSelect(ban, banActionId, 'ban')
                                if not res.is_error:
                                    break
                            return
            # pick
            if conn.pick_flag:
                pickActionId: int = None
                for actionItem in actions[2:]:
                    for action in actionItem:
                        if action['actorCellId'] == cellId:
                            pickActionId = action['id']
                            if not action['completed'] and action['isInProgress']:
                                pickable = set((await self.doGet(ROUTE.pickable)).json())  # 可ban
                                picks = set(conn.pick_champions[position])  # 想ban
                                for pick in picks.intersection(pickable):  # 并集
                                    res = await self.ChampSelect(pick, pickActionId, 'pick')
                                    if not res.is_error:
                                        break
                                return

    async def getProfileIcon(self, profileId):
        """获取头像base64"""
        a = await self.doGet(ROUTE.profile_icon.format(profileId))
        return a.text.encode()

    async def getMastery(self, summonerId: int, limit: int):
        """获取最熟练英雄"""
        return (await self.doGet(ROUTE.collection.format(summonerId, limit))).json()['masteries']