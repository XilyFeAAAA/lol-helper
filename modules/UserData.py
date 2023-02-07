from pathlib import Path
from Enum.Structs import *
import json
from modules import Config
from utils.common import JsonReader


class UserClass:
    def __init__(self):
        self.info: SummonerInfo  # 登录人信息
        self.state: StateEvent  # 当前状态
        self.clientStatus: ClientStatus
        self.recent_rank: list = []  # 最近游戏
        self.loots: list = []  # 战利品
        self.chatRoomId: str = ""  # 房间Id
        self.gamemode: str = ""  # 游戏模式
        self.picked: bool = False
        self.banned: bool = False
        self.classic_pick: int = Config.INFO['Classic_pick']
        self.record_flag: bool = Config.INFO['Record']
        self.accept_flag: bool = Config.INFO['Accept']
        self.autobp_flag: bool = Config.INFO['Autobp']
        self.analze_flag: bool = Config.INFO['Analyze']
        self.reconnect_flag: bool = Config.INFO['Reconnect']
        self.pick_champions: json = Config.INFO['pick_champions']  # pick列表
        self.ban_champions: json = Config.INFO['ban_champions']  # ban列表
        self.swap_champions: list = Config.INFO['swap_champions']  # swap列表
        self.heros: json = Config.heros_dict
    def reset(self):
        self.picked: bool = False
        self.banned: bool = False
