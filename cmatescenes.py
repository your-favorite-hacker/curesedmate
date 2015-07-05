# Copyright (C) 2010 dash@uberwall.org
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. All advertising materials mentioning features or use of this software
#    must display the following acknowledgement:
#      This product includes software developed by dash.
# 4. The name dash may not be used to endorse or promote
#    products derived from this software without specific prior written
#    permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

import cmatelib
import random
import curses
import sys
import time

def pre_intro(cm,func):
    """ what can i say, the coordinates are fucked up """
    win20 = cm.create_window(cm.sizex,cm.sizey,0,0)
    curses.curs_set(0)
    x=0
    y=13
    y1=11
    char="|"
    while 1:
	win20.hline(y,x,char,cm.sizey)
	win20.hline(y1,x,char,cm.sizey)
	y+=1
	y1-=1
	win20.refresh()
	time.sleep(0.1)
	if y == cm.sizex:
	    break

    if func==1:
	y=12
	x=0
	curses.curs_set(1)
	while 1:
	    cm.move_cursor(win20,y,x)
	    win20.refresh()
	    time.sleep(0.1)
	    x+=1
	    if x == 80:
		break

    if func==2:
	y=12
	x=79
	curses.curs_set(1)
	while 1:
	    cm.move_cursor(win20,y,x)
	    win20.refresh()
	    time.sleep(0.1)
	    x-=1
	    if x == 0:
		break

def intro(cm):
    win5 = cm.create_window(cm.sizex,cm.sizey,0,0)
    cm.config_window(win5,1)
    welc = ".oOo.oOO w3lcome to cursedmate OOo.oOo."
    rpos = cm.compute_strpos(win5,1,welc)
    cm.write_window(win5,5,rpos,welc,curses.color_pair(2))
    i = 0
    y = 78
    x = 16
    y1 = 78
    x1 = 16
    while 1:
	if y == 0:
	    curses.curs_set(0)

	if y >= 0:
	    cm.move_cursor(win5,x,y)

	if y == 60:
	    cm.move_item(win5,"O",x1,y1,curses.color_pair(5))
	    cm.config_window(win5,1)
	    curses.curs_set(0)
	    shitno0days = "oh shit!!111 it is a fed!!!"
	    rpos = cm.compute_strpos(win5,1,shitno0days)
	    cm.write_window(win5,(cm.sizex/4)+2,rpos,shitno0days,curses.color_pair(1))
	    time.sleep(2)
	    curses.curs_set(1)
	elif y < 60:
	    if y1 == 0:
		cm.delete_item(win5," ",x1,y1+1)
		win5.refresh()
		break
	    cm.delete_item(win5," ",x1,y1+1)
	    cm.move_item(win5,"O",x1,y1,curses.color_pair(5))
	    cm.config_window(win5,1)
	    y1 = y1 -1

	if y >= 0:
	    cm.move_cursor(win5,x,y)

	if y != 0 and y >= 50:
	    y = y -1

	elif y > 2 and y <= 50:
	    y = y - 2

	elif y <= 2 and y <=50:
	    y = y - 1 

	win5.refresh()
	time.sleep(0.1)

    win5.nodelay(1)
    win5.move(cm.sizex/2,rpos)
    win5.box()

    i = 0
    o = 100
    win5.nodelay(1)
    while 1:
	a = win5.getch()
	if i%o == 0:
	    space = "press <SPACE> to contiue"
	    rpos = cm.compute_strpos(win5,1,space)
	    cm.write_window(win5,cm.sizex/2,rpos,space,curses.color_pair(5))
	    win5.refresh()
	    time.sleep(3)
	    win5.move(cm.sizex/2,rpos)
	    win5.clrtoeol()
	    win5.box()
	    win5.refresh()
	time.sleep(0.1)
	if a == 32:
	    return

def level_info(win,cm):
    string = "there are %s zerodays and %s fed(z)" % (cm.gold, cm.ms)
    rpos = cm.compute_strpos(win,1,string)
    cm.write_window(win,3,rpos,string,curses.color_pair(2))
    win.box()
    win.refresh()
    time.sleep(0.1)
    string = ">- Go -<"
    rpos = cm.compute_strpos(win,1,string)
    cm.write_window(win,6,rpos,string,curses.color_pair(4))
    win.box()
    win.refresh()
    while 1:
	a = win.getch()
	if a == 32:
	    win.erase()
	    return

def congrats(win,cm):
    string = "awesome! u collected enough zerodays"
    rpos = cm.compute_strpos(win,1,string)
    cm.write_window(win,3,rpos,string,curses.color_pair(2))
    win.box()
    win.refresh()
    time.sleep(0.5)
    if cm.collected<=10:
	string = "uid=65535(nobody) gid=65535(nobody)"
    elif cm.collected>=10 and cm.collected <40:
	string = "uid=8080(www) gid=8080(www)"
    elif cm.collected>=40 and cm.collected <70:
	string = "uid=1(operator) gid=1(operator)"
    elif cm.collected>=70 and cm.collected <100:
	string = "uid=0(root) gid=0(wheel) groups=0(wheel)"
    elif cm.collected>=100 and cm.collected <=120:
	string = "isn't there a remote shell waiting for you?"
	color=curses.color_pair(2)
    elif cm.collected>=120 and cm.collected <=140:
	string = "yes. yes. xss is dangerous too"
	color=curses.color_pair(2)
    elif cm.collected>=140 and cm.collected <=160:
	string = "moaarr - do u ever considered stop playing?"
	color=curses.color_pair(2)
    elif cm.collected>=160 and cm.collected <=180:
	string = "the latest phrack is out! yes!"
	color=curses.color_pair(2)
    elif cm.collected>=180 and cm.collected <=200:
	string = "btw. what happened to phrack.ru?!"
	color=curses.color_pair(2)
    elif cm.collected>=200 and cm.collected <=220:
	string = "..."
	color=curses.color_pair(2)
    elif cm.collected>=220 and cm.collected <=240:
	string = "strange things happen in the dark edges of the morloch"
	color=curses.color_pair(2)
    elif cm.collected>=240:
	string = "ok, i am off have fun!"
	color=curses.color_pair(2)

    color=curses.color_pair(5)
    rpos = cm.compute_strpos(win,1,string)
    cm.write_window(win,5,rpos,string,color)
    win.box()
    win.refresh()
    win.nodelay(0)
    while 1:
	a = win.getch()
	if a == 32:
	    win.erase()
	    return

def lost_a_live(win,cm):
    string = "watch out man!"
    rpos = cm.compute_strpos(win,1,string)
    cm.write_window(win,3,rpos,string,curses.color_pair(2))
    win.box()
    win.refresh()
    while 1:
	a = win.getch()
	if a == 32:
	    win.erase()
	    return

def start_of_game(win,cm):
    win.box()
    win.refresh()
    win.scrollok(1)
    win.idlok(1)
    curses.curs_set(1)
    string = "here u go stranger, u installed ncurses,\nhave a working python interpreter\na fully colorable xterm or rxvt\nsitting at work on a boring monday morning\nTHIS IS THE CHANCE TO FEEL LIKE 1985\n(no matter if u were not born yet)\n\n\nnow, you have 20 levels\ndont worry if u loose a life\nu get new one with 35 exploits collected\n(from now on this is working in RL as well)\nu meet already one of the bad guys\n%s <---- this is what u want to collect\nu move ur ass with the cursors\n\nif ur listening to LCP\nnow is the time to turn it up\nbring da noize\n\n\n(press space)\n\n\n\n\n\n\n" % (chr(163))
    parts = string.split('\n')
    xpos=0
    win.nodelay(1)
    for ln in parts:
	if xpos < 14:
	    xpos+=1
	if xpos>=14:
	    win.scroll(1)
	    win.move(xpos,1)
	    win.clrtoeol()
	    win.box()

	rpos = cm.compute_strpos(win,1,ln)
	cm.write_window(win,xpos,rpos,ln,curses.color_pair(1))
	time.sleep(2.0)

	a = win.getch()
	if a == 32:
	    win.erase()
	    return
	win.box(0,0)

    while 1:
	a = win.getch()
	if a == 32:
	    win.erase()
	    return

def end_of_game(win,cm):
    string = "that's it stranger!\nu did it! the game is over\neven the fedz from hell could not stop u!\n\n\ni hope u had fun.\n" 
    parts = string.split('\n')
#    win.move(0,0)
    xpos=1
    for ln in parts:
	rpos = cm.compute_strpos(win,1,ln)
#	win.addstr(ln, curses.color_pair(1))
	cm.write_window(win,xpos,rpos,ln,curses.color_pair(1))
	time.sleep(2)
	xpos+=1

    win.nodelay(1)
    while 1:
	rc = random.randint(0,10)
	string = "~~ keep the spirit - hack the planet! ~~"
	rpos = cm.compute_strpos(win,1,string)
	cm.write_window(win,5,rpos,string,curses.color_pair(rc))
	win.box()
	win.refresh()
	time.sleep(0.3)
	a = win.getch()
	if a == 32:
	    win.erase()
	    return

def ur_dead(win,cm):
    string = "dangit! .gov has u!"
    rpos = cm.compute_strpos(win,1,string)
    cm.write_window(win,3,rpos,string,curses.color_pair(2))

    string = "# rm -fr /"
    rpos = cm.compute_strpos(win,1,string)
    cm.write_window(win,5,rpos,string,curses.color_pair(2))
    win.box()
    win.refresh()
    while 1:
	a = win.getch()
	if a == 32:
	    win.erase()
	    return

def pause_game(win,cm):
    win.nodelay(0)
    string = "PAUSE"
    rpos = cm.compute_strpos(win,1,string)
    cm.write_window(win,3,rpos,string,curses.color_pair(2))
    win.box()
    win.refresh()
    while 1:
	a = win.getch()
	if a == 32:
	    win.erase()
	    return

def really_quit(win,cm):
    string = "Quit the game Y/N"
    rpos = cm.compute_strpos(win,1,string)
    cm.write_window(win,3,rpos,string,curses.color_pair(2))
    win.box()
    win.refresh()
    while 1:
	a = win.getch()
	if a == 110: #110 == n
	    return -1
	if a == 122 or a ==121 : #122 == z / 121 == y
	    return 1
    win.erase()

