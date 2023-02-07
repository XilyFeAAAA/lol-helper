import asyncio
import threading
import tkinter
from tkinter import BooleanVar, Tk, ttk, Text
from main_willump import WebSocketListen
from modules.UserData import UserClass
from modules import Config
from loguru import logger
from Enum.Enums import *
from ui.ComBoPicker import Combopicker
from utils.LeagueGameApi import LcuApi
from Enum.Structs import *

class UI(Tk):
    def __init__(self):
        super().__init__()
        self.title("LOL助手")
        self.geometry("785x495")
        self.user = UserClass()
        self.api = LcuApi()
        self.ws = WebSocketListen(self.user, self.api)

        # 自动确认开关
        self.autoacceptkVar = BooleanVar(value=self.user.accept_flag)
        ttk.Checkbutton(self,
                        text="自动接受",
                        variable=self.autoacceptkVar,
                        command=self.Accept
                        ).place(x=10, y=5)

        self.autopickVar = BooleanVar(value=self.user.autobp_flag)
        ttk.Checkbutton(self,
                        text="自动BP",
                        variable=self.autopickVar,
                        command=self.AutoBP
                        ).place(x=110, y=5)

        self.analysisVar = BooleanVar(value=self.user.analze_flag)
        ttk.Checkbutton(self,
                        text="战绩分析",
                        variable=self.analysisVar,
                        command=self.Analyze
                        ).place(x=10, y=35)

        self.recordVar = BooleanVar(value=self.user.record_flag)
        ttk.Checkbutton(self,
                        text="记录cd",
                        variable=self.recordVar
                        ).place(x=110, y=35)
        # 设置英雄优先级
        ttk.Button(
            self, text="保存设置", command=self.Save
        ).place(x=200, y=3)

        # "配置符文
        ttk.Button(
            self, text="配置符文", command=lambda: threading.Thread(target=self.SetRune).start()).place(x=300, y=3)

        # 启动按钮
        ttk.Button(
            self, text="启动助手", command=self.Start).place(x=200, y=33)

        # 分解碎片
        ttk.Button(
            self, text="分解碎片", command=lambda :threading.Thread(target=self.Loot).start()).place(x=300, y=33)
        # 日志框
        text = Text(self, width=55, height=33)
        text.place(x=0, y=60)

        tkinter.Label(self, text='游戏ID').place(x=400,y=250)

        self.entry1 = tkinter.Entry(self, width=20, relief='groove')
        self.entry1.place(x=620, y=250)
        self.entry1.bind("<Return>", lambda event: threading.Thread(target=self.Search).start())

        tkinter.Label(self, text='段位伪造').place(x=400,y=285)

        self.Rankvar = tkinter.StringVar()
        com1 = ttk.Combobox(self,
                            textvariable=self.Rankvar,
                            width=18,
                            values=('坚韧黑铁',
                                    '英勇黄铜',
                                    '不屈白银',
                                    '荣耀黄金',
                                    '华贵铂金',
                                    '璀璨钻石',
                                    '超凡大师',
                                    '傲世宗师',
                                    '最强王者',
                                    '没有段位'),  # 选择列表以元组提供
                            state='readonly')  # 选择项只读
        com1.place(x=620, y=285)
        com1.bind("<<ComboboxSelected>>", self.RankChange)

        tkinter.Label(self, text='状态伪造').place(x=400, y=320)

        self.Statusvar = tkinter.StringVar()
        com2 = ttk.Combobox(self,
                            textvariable=self.Statusvar,
                            width=18,
                            values=("在线",
                                    "离开",
                                    "游戏中",
                                    "离线",
                                    "手机在线"),
                            state='readonly')  # 选择项只读
        com2.place(x=620, y=320)
        com2.bind("<<ComboboxSelected>>", self.StatusChange)

        tkinter.Label(self, text='生涯背景').place(x=400, y=355)

        ttk.Button(self, text='选择', width=20).place(x=620, y=355)

        tkinter.Label(self, text='5v5训练营').place(x=400, y=390)

        ttk.Button(self, text='创建', width=20, command=lambda :asyncio.run(self.api.Create_custom_lobby())).place(x=620, y=390)

        tkinter.Label(self, text='训练营人机').place(x=400, y=425)

        ttk.Button(self, text='添加', width=20, command=lambda :asyncio.run(self.api.Add_bots_team())).place(x=620, y=425)

        tkinter.Label(self, text='观战').place(x=400, y=460)

        self.entry2 = tkinter.Entry(self, width=20, relief='groove')
        self.entry2.place(x=620, y=460)
        #self.entry2.bind("<Return>", lambda event: threading.Thread(target=self.Search).start())

        tkinter.Label(self, text='匹配秒抢').place(x=400, y=180)

        self.Classicvar = tkinter.StringVar()
        self.Classicvar.set(Config.heros_dict[str(self.user.classic_pick)])
        com3 = ttk.Combobox(self,
                            textvariable=self.Classicvar,
                            width=17,
                            values=Config.heros_list,
                            state='readonly')  # 选择项只读
        com3.place(x=620, y=180)
        com3.bind("<<ComboboxSelected>>", self.ClassicSelected)

        tkinter.Label(self, text='大乱斗秒抢').place(x=400, y=215)

        self.cp_aram = Combopicker(self, values=Config.heros_list)
        self.cp_aram.place(x=620, y=215)
        self.cp_aram.bind("<<ComboboxSelected>>", )
        self.cp_aram.entry_var.set(",".join([Config.heros_dict[str(i)] for i in self.user.swap_champions]))


        tkinter.Label(self, text='上路(P/B)').place(x=400, y=5)
        self.cp_top_pick = Combopicker(self, values=Config.heros_list)
        self.cp_top_pick.place(x=470, y=5)
        self.cp_top_pick.entry_var.set(",".join([Config.heros_dict[str(i)] for i in self.user.pick_champions['top']]))

        self.cp_top_ban = Combopicker(self, values=Config.heros_list)
        self.cp_top_ban.place(x=620, y=5)
        self.cp_top_ban.entry_var.set(",".join([Config.heros_dict[str(i)] for i in self.user.ban_champions['top']]))

        tkinter.Label(self, text='打野').place(x=400, y=40)
        self.cp_jug_pick = Combopicker(self, values=Config.heros_list)
        self.cp_jug_pick.place(x=470, y=40)
        self.cp_jug_pick.entry_var.set(",".join([Config.heros_dict[str(i)] for i in self.user.pick_champions['jug']]))

        self.cp_jug_ban = Combopicker(self, values=Config.heros_list)
        self.cp_jug_ban.place(x=620, y=40)
        self.cp_jug_ban.entry_var.set(",".join([Config.heros_dict[str(i)] for i in self.user.ban_champions['jug']]))

        tkinter.Label(self, text='中单').place(x=400, y=75)
        self.cp_mid_pick = Combopicker(self, values=Config.heros_list)
        self.cp_mid_pick.place(x=470, y=75)
        self.cp_mid_pick.entry_var.set(",".join([Config.heros_dict[str(i)] for i in self.user.pick_champions['mid']]))

        self.cp_mid_ban = Combopicker(self, values=Config.heros_list)
        self.cp_mid_ban.place(x=620, y=75)
        self.cp_mid_ban.entry_var.set(",".join([Config.heros_dict[str(i)] for i in self.user.ban_champions['mid']]))

        tkinter.Label(self, text='射手').place(x=400, y=110)
        self.cp_ad_pick = Combopicker(self, values=Config.heros_list)
        self.cp_ad_pick.place(x=470, y=110)
        self.cp_ad_pick.entry_var.set(",".join([Config.heros_dict[str(i)] for i in self.user.pick_champions['ad']]))

        self.cp_ad_ban = Combopicker(self, values=Config.heros_list)
        self.cp_ad_ban.place(x=620, y=110)
        self.cp_ad_ban.entry_var.set(",".join([Config.heros_dict[str(i)] for i in self.user.ban_champions['ad']]))

        tkinter.Label(self, text='辅助').place(x=400, y=145)
        self.cp_sup_pick = Combopicker(self, values=Config.heros_list)
        self.cp_sup_pick.place(x=470, y=145)
        self.cp_sup_pick.entry_var.set(",".join([Config.heros_dict[str(i)] for i in self.user.pick_champions['sup']]))

        self.cp_sup_ban = Combopicker(self, values=Config.heros_list)
        self.cp_sup_ban.place(x=620, y=145)
        self.cp_sup_ban.entry_var.set(",".join([Config.heros_dict[str(i)] for i in self.user.ban_champions['sup']]))

        logger.add(lambda msg: text.insert("end", msg) or text.see("end"),
                   format="{time:HH:mm:ss} {message}")

    def Start(self):
        self.thread = threading.Thread(target=self.ws.run, daemon=True)
        self.thread.start()

    def Accept(self):
        self.user.accept_flag = self.autoacceptkVar.get()

    def AutoBP(self):
        self.user.autobp_flag = self.autopickVar.get()

    def Analyze(self):
        self.user.analze_flag = self.analysisVar.get()

    def RankChange(self, event):
        asyncio.run(self.api.SetRank(RankC2E[self.Rankvar.get()]))

    def StatusChange(self, event):
        asyncio.run(self.api.ChangeStatus(self.Statusvar.get()))

    def Search(self):
        asyncio.run(self.api.SearchSummoner(self.entry1.get()))

    def Loot(self):
        asyncio.run(self.api.Rental_dissolve())

    def SetRune(self):
        asyncio.run(self.ws.api.SetRune())

    def ClassicSelected(self, event):
        self.user.classic_pick = Config.heros_dict[self.Classicvar.get()]
        print(self.user.classic_pick)
    def Save(self):
        self.user.pick_champions = {
            'top': [Config.heros_dict[i] for i in self.cp_top_pick.get().split(',')],
            'jug': [Config.heros_dict[i] for i in self.cp_jug_pick.get().split(',')],
            'mid': [Config.heros_dict[i] for i in self.cp_mid_pick.get().split(',')],
            'ad': [Config.heros_dict[i] for i in self.cp_ad_pick.get().split(',')],
            'sup': [Config.heros_dict[i] for i in self.cp_sup_pick.get().split(',')]
        }
        self.user.ban_champions = {
            'top': [Config.heros_dict[i] for i in self.cp_top_ban.get().split(',')],
            'jug': [Config.heros_dict[i] for i in self.cp_jug_ban.get().split(',')],
            'mid': [Config.heros_dict[i] for i in self.cp_mid_ban.get().split(',')],
            'ad': [Config.heros_dict[i] for i in self.cp_ad_ban.get().split(',')],
            'sup': [Config.heros_dict[i] for i in self.cp_sup_ban.get().split(',')]
        }
        self.user.swap_champions = [Config.heros_dict[i] for i in self.cp_aram.get().split(',')]
        Config.INFO['pick_champions'] = self.user.pick_champions
        Config.INFO['ban_champions'] = self.user.ban_champions
        Config.INFO['Record'] = self.user.record_flag
        Config.INFO['Accept'] = self.user.accept_flag
        Config.INFO['Autobp'] = self.user.autobp_flag
        Config.INFO['Analyze'] = self.user.analze_flag
        Config.INFO['swap_champions'] = self.user.swap_champions
        Config.INFO['Classic_pick'] = self.user.classic_pick
        Config.save()
if __name__ == "__main__":
    root = UI()
    root.mainloop()
