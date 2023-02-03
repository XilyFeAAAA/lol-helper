from pathlib import Path
from Enum.Structs import *
from utils.common import JsonReader


class UserClass:
    def __init__(self):
        self.info: SummonerInfo  # 登录人信息
        self.state: StateEvent  # 当前状态
        self.clientStatus: ClientStatus
        self.recent_rank: list = []  # 最近游戏
        self.loot: list = []  # 战利品
        self.runed: bool = False  # 是否配置符文
        self.sent: bool = False  # 是否发送战绩
        self.chatRoomId: str = ""  # 房间Id
        self.gamemode: str = ""  # 游戏模式
        self.current_champion: ChampionInfo = None  # 当前英雄
        self.pick_flag: bool = True
        self.ban_flag: bool = True
        self.pick_champions: dict = {}  # pick列表
        self.ban_champions: dict = {}  # ban列表
        self.swap_champions: list = []  # swap列表
        self.heros: list = JsonReader(Path('.') / 'scr/hero_list.js')['hero']
