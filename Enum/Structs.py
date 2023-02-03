from .MessageEnum import *


# 个人信息
class SummonerInfo:
    def __init__(self, id, name, uid, level, profileIcon, environment=''):
        self.summonerId: int = id
        self.displayName: str = name
        self.environment: str = environment
        self.puuid: str = uid
        self.summonerLevel: int = level
        self.rank: str
        self.rankLevel: str
        self.profileIcon: int = profileIcon

class ChampionInfo:
    def __init__(self, id: int, name: str):
        self.championId: int = id
        self.championName: str = name
        self.pickable: bool = True
        self.bannable: bool = True


# 玩家信息
class SummonerData:
    def __init__(self, puuid, summonerid):
        self.puuid: str
        self.summonerId: str
        self.ranks: list


# 房间信息
class LobbyInfo:
    def __init__(self):
        self.gameMode: GameInfo
        self.chatRoomId: str


# 对局信息
class RankInfo:
    def __init__(self, kill, death, assist, FirstBloodKill, Pentakill, QuadraKill, TripleKill, win):
        self.kill: int = kill
        self.death: int = death
        self.assist: int = assist
        self.FirstBloodKill: bool = FirstBloodKill
        self.PentaKills: int = Pentakill
        self.QuadraKills: int = QuadraKill
        self.TripleKills: int = TripleKill
        self.win: bool = win
        self.score: int = 0

    def Calculate(self):
        self.score = (self.kill * 1.2 + self.assist * 0.8) / (1 if not self.death else self.death * 1.2)
        self.score += self.PentaKills * 2 + self.QuadraKills * 1 + self.TripleKills * 0.5
        self.score += self.win + self.FirstBloodKill
        return self.score



class GameInfo:
    def __init__(self):
        self.gameId: int  # 11:峡谷  12:嚎哭深渊
        self.gameMode: str  # ARAM: 大乱斗 CLASSIC 排位 URF 无心火力
        self.mapId: int


# 战利品
class LootInfo:
    def __init__(self, count, localizedName, type, lootName, storItemId, value, redeem):
        self.count: int = count  # 数量
        self.localizedName: str = localizedName  # 名字
        self.type: str = type  # 类型
        self.lootName: str = lootName
        self.storeItemId: int = storItemId  # Id
        self.value: int = value  # 价值
        self.redeem: str = redeem
