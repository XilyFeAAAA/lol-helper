#! /usr/bin/env python
# -*- coding: utf-8 -*-#
import threading
import win32api
import win32con
import time
import ctypes
import os
import cmd
import sys
import simpleaudio as sa
from pynput import keyboard

# 资源文件目录访问
def source_path(relative_path):
    # 是否Bundle Resource
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def VoiceBoardcast(pos, key):
    sa.WaveObject.from_wave_file(f"data/{pos}{key}.wav").play()

class PlayerHandler:
    def __init__(self, pos, now_time, cd):
        self.pos = pos
        self.cd = cd
        self.cd_time = now_time + cd
        threading.Thread(target=self.Reminder, daemon=True).start()

    def Reminder(self):
        time.sleep(self.cd_time - 30)
        VoiceBoardcast(self.pos, 30)
        time.sleep(30)
        VoiceBoardcast(self.pos, 0)

class KeyboardController:
    def keydownup(self, arg):
        MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
        if isinstance(arg, str):
            key = self.getVK(arg)
            win32api.keybd_event(key, MapVirtualKey(key, 0), 0, 0)
            win32api.keybd_event(key, MapVirtualKey(key, 0), win32con.KEYEVENTF_KEYUP, 0)

    def getVK(self, i):
        if i.isdigit():
            return 48 + ord(i)
        elif i.isalpha() and len(i) == 1:
            return ord(i) - 32
        elif i == ' ':
            return 32
        elif i == 'enter':
            return 13

    def PressText(self, text):
        for i in text:
            self.keydownup(i)

class RecordHandler:
    def __init__(self):
        self.relay = 0.5
        self.text = ""
        self.now_time = 0
        self.thread = None
        self.players = []
        self.controller = KeyboardController()
        self.listener = keyboard.Listener(on_press=self.on_press)

    def Time_Refresh(self):
        self.now_time += 1
        self.createTimer()

    def createTimer(self):
        self.thread = threading.Timer(1, self.Time_Refresh)
        self.thread.start()

    def on_press(self, key):
        if key == keyboard.Key.f1:
            self.players.append(PlayerHandler('top', self.now_time,300))
        elif key == keyboard.Key.f2:
            self.players.append(PlayerHandler('jug', self.now_time,300))
        elif key == keyboard.Key.f3:
            self.players.append(PlayerHandler('mid', self.now_time,300))
        elif key == keyboard.Key.f4:
            self.players.append(PlayerHandler('ad', self.now_time,300))
        elif key == keyboard.Key.f5:
            self.players.append(PlayerHandler('sup', self.now_time,300))
        elif key == keyboard.Key.up:
            if self.thread != None:  # 重新计时
                self.thread.cancel()
                self.now_time = 0
            self.createTimer()
        elif key == keyboard.Key.f7:
            self.text = ""
            for i in self.players:
                if i.cd_time > self.now_time:
                    m, s = divmod(i.cd_time, 60)
                    s = str(s)
                    self.text += f"{i.pos}{m}{'0' + s if len(s) == 1 else s} "
                else:
                    self.players.remove(i)
            self.controller.keydownup('enter')  # 打开文本框
            time.sleep(0.1)  # 等待文本框
            self.controller.PressText(self.text)  # 输入
            self.controller.keydownup('enter')  # 发送

    def listen_key_nblock(self):
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()

class Cmd(cmd.Cmd):
    intro = '英雄联盟技能冷却辅助，输入 help 或者?查看帮助。\n'
    prompt = '>'
    print(f'游戏开始时按下方向↑键同步时间\nf1-f5记录各个位置闪现，f7发送cd时间')
    def do_start(self, arg):
        '开始'
        Recorder = RecordHandler()
        Recorder.listener.start()

    def do_exit(self, _):
        '退出'
        exit(0)

if __name__ == "__main__":
    # 修改当前工作目录，使得资源文件可以被正确访问
    cd = source_path('')
    os.chdir(cd)
    RecordHandler()
    Cmd = Cmd()
    Cmd.cmdloop()
