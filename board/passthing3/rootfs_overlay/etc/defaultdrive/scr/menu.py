#!/usr/bin/env python2

import curses
from curses import panel
import subprocess
import glob
import os

rpi = True
try:
    import RPi.GPIO as GPIO
except ImportError:
    rpi = False

if rpi:
    UP = 21
    DOWN = 8
    OK = 22
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(OK, GPIO.IN, pull_up_down=GPIO.PUD_UP)


class Menu(object):
    def __init__(self, items, stdscreen, name):
        self.name = name
        self.screen = stdscreen
        self.window = stdscreen.subwin(0, 0)
        self.window.keypad(1)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()

        self.position = 0
        self.items = items
        if self.name != "Main":
            self.items.append(("Exit", "exit"))

    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items) - 1

    def drawoverlay(self):
        if os.path.isdir("/sys/kernel/config/usb_gadget/g2"):
            with open("/sys/kernel/config/usb_gadget/g2/functions/mass_storage.usb0/lun.0/file", "r") as file:
                string = file.read()
            string = string.split("/")[-1]
        else:
            string = "Default"
        maxx = self.screen.getmaxyx()[1]
        self.window.addstr(0, maxx - (len(string)), string)

    def display(self): 
        self.position = 0
        self.panel.top()
        self.panel.show()
        self.window.clear()

        while True:
            self.window.refresh()
            #subprocess.call("tput civis".split(" "))
            curses.doupdate()
            start = 0
            if self.position > 1:
                start = self.position - 1
            end = min(start + self.screen.getmaxyx()[0] - 1, len(self.items))
            for index in range(0, self.screen.getmaxyx()[0]):
                self.window.addstr(index, 0, " "*(self.screen.getmaxyx()[1] - 1))
            self.window.addstr(0, 0, self.name, curses.A_REVERSE)
            for index in range(start, end):
                if index == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL
                msg = "%s" % (self.items[index][0])
                if len(msg) > self.screen.getmaxyx()[1] - 1:
                    msg = msg[0:self.screen.getmaxyx()[1] - 4] + "..."
                self.window.addstr(index + 1 - start, 0, msg, mode)
            self.drawoverlay()
            if rpi:
                if not GPIO.input(UP):
                    self.navigate(-1)
                    while not GPIO.input(UP): pass
                elif not GPIO.input(DOWN):
                    self.navigate(1)
                    while not GPIO.input(DOWN): pass
                elif GPIO.input(OK) == False:
                    while GPIO.input(OK) == False: pass
                    if self.position == len(self.items) - 1 and self.name != "Main":
                        break
                    else:
                        self.items[self.position][1]()
            else:
                key = self.window.getch()

                if key in [curses.KEY_ENTER, ord("\n")]:
                    if self.position == len(self.items) - 1:
                        break
                    else:
                        self.items[self.position][1]()

                elif key == curses.KEY_UP:
                    self.navigate(-1)

                elif key == curses.KEY_DOWN:
                    self.navigate(1)

        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()


class Script():
    def __init__(self, cmd):
        self.cmd = cmd

    def __call__(self):
        curses.noraw()
        subprocess.call(["/usr/bin/umountrun", self.cmd])
        curses.raw()

class Disk():
    def __init__(self, cmd):
        self.cmd = cmd

    def __call__(self):
        curses.noraw()
        subprocess.call(["/usr/bin/mountdisk", self.cmd])
        curses.raw()

class Ducky():
    def __init__(self, cmd):
        self.cmd = cmd

    def __call__(self):
        curses.noraw()
        subprocess.call(["/usr/bin/duckpi.sh", self.cmd])
        curses.raw()

browsemenus = {}


def nothing():
    pass


class browsefile():
    def __init__(self, path, screen):
        self.screen = screen
        self.path = path

    def __call__(self):
        global browsemenus
        if self.path not in browsemenus:
            pathmenu_items = [("Delete", nothing)]
            if self.path.split(".")[-1] in ["sh", "py"]:
                calls = Script("/root/disk.d/" + self.path)
                pathmenu_items += [("Run", calls)]
            elif self.path.split(".")[-1] in ["iso"]:
                calls = Disk("/root/disk.d/" + self.path)
                pathmenu_items += [("Mount", calls)]
            pathmenu = Menu(pathmenu_items, self.screen, self.path)
            browsemenus[self.path] = pathmenu
        browsemenus[self.path].display()


class browsedir():
    def __init__(self, path, screen):
        self.screen = screen
        self.path = path

    def __call__(self):
        global browsemenus
        if self.path not in browsemenus:
            pathmenu_items = []
            for i in glob.glob("/root/disk.d%s/*" % self.path):
                calls = browsedir(self.path + i.split("/")[-1] + "/", self.screen)
                if os.path.isfile(i):
                    calls = browsefile(self.path + i.split("/")[-1], self.screen)
                pathmenu_items += [[i.split("/")[-1], calls]]
            pathmenu = Menu(pathmenu_items, self.screen, self.path)
            browsemenus[self.path] = pathmenu
        browsemenus[self.path].display()

def reset_disk():
    subprocess.call(["/usr/bin/umountdisk"])

def reboot():
    subprocess.call(["reboot"])


class MyApp(object):
    def __init__(self, stdscreen):
        self.screen = stdscreen
        try:
            curses.curs_set(False)
        except curses.error:
            pass

        scriptmenu_items = []
        for i in glob.glob("/root/disk.d/scr/menu/*"):
            calls = Script(i)
            scriptmenu_items += [[i.split("/")[-1], calls]]

        diskmenu_items = []
        for i in glob.glob("/root/disk.d/doc/disks/*"):
            calls = Disk(i)
            diskmenu_items += [[i.split("/")[-1], calls]]
        diskmenu_items += [["Reset", reset_disk]]

        duckymenu_items = []
        for i in glob.glob("/root/disk.d/doc/payloads/*"):
            calls = Ducky(i)
            duckymenu_items += [[i.split("/")[-1], calls]]

        scriptmenu = Menu(scriptmenu_items, self.screen, "Main>Scripts")
        diskmenu = Menu(diskmenu_items, self.screen, "Main>Disks")
        duckymenu = Menu(duckymenu_items, self.screen, "Main>Ducky")

        main_menu_items = [
            ("Scripts", scriptmenu.display),
            ("Disks", diskmenu.display),
            ("Browse", browsedir("/", self.screen)),
            #("Ducky", duckymenu.display),
            ("Reboot", reboot),
        ]
        main_menu = Menu(main_menu_items, self.screen, "Main")
        main_menu.display()


if __name__ == "__main__":
    curses.wrapper(MyApp)
    GPIO.cleanup()
