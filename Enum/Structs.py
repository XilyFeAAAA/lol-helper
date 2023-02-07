from .Enums import *


# 个人信息
class SummonerInfo:
    def __init__(self, id, name, uid, level, profileIcon=-1, environment=''):
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
    def __init__(self, flexTier, flexDivision, flexWin, flexLoss, soloTier, soloDivision, soloWin, soloLoss, highestTier, highestDivision):
        self.flexTier: str = flexTier
        self.flexDivision: str = flexDivision if flexDivision != 'NA' else ""
        self.flexWin: int = flexWin
        self.flexLoss: int = flexLoss
        self.flexGames = self.flexWin + self.flexLoss
        self.flexRate = round(float(self.flexWin) / (self.flexGames if self.flexGames != 0 else 1.0), 2)
        self.soloTier: str = soloTier
        self.soloDivision: str = soloDivision if soloDivision != 'NA' else ""
        self.soloWin: int = soloWin
        self.soloLoss: int = soloLoss
        self.soloGamse: int = self.soloWin + self.soloLoss
        self.soloRate: float = round(float(self.soloWin) / (self.soloGamse if self.soloGamse != 0 else 1.0), 2)
        self.highestTier: str = highestTier
        self.highestDivision: str = highestDivision if highestDivision != 'NA' else ""


class GameInfo:
    def __init__(self):
        self.gameId: int  # 11:峡谷  12:嚎哭深渊
        self.gameMode: str  # ARAM: 大乱斗 CLASSIC 排位 URF 无心火力
        self.mapId: int

