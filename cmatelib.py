#!/usr/bin/env python

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


import random
import curses
import time
import sys
import os
 
class cmate(object):
    def __init__(self):
	self.name="the hunt for 0days"
	self.lvl=0
	self.gold=0
	self.gcount=0
	self.collected=0
	self.eaten=0
	self.ms=0
	self.elive=0
	self.lives=3
	self.time=60
	self.gmap=[]
	self.mmap=[]
	self.gomap=[]
	self.win1=0
	self.win2=0
	self.sizex=25
	self.sizey=80
	self.winlist=[]
	self.stdscr=0
	self.msspeed=100

    def close_stdscr(self):
	""" at the end - we reset everything """
	curses.nocbreak()
	curses.echo()
	self.stdscr.keypad(0)
	curses.endwin()

    def create_stdscr(self):
	""" function for the stdscr """
	self.stdscr = curses.initscr()
	self.stdscr.border()
	self.stdscr.keypad(1)

	curses.cbreak()
	curses.noecho()
	curses.start_color()
	curses.curs_set(1)

    def create_colors(self):
	curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
	curses.init_pair(2,curses.COLOR_YELLOW,curses.COLOR_BLACK)
	curses.init_pair(3,curses.COLOR_RED,curses.COLOR_BLACK)
	curses.init_pair(4,curses.COLOR_WHITE,curses.COLOR_BLACK)
	curses.init_pair(5,curses.COLOR_WHITE,curses.COLOR_RED)
	curses.init_pair(6,curses.COLOR_YELLOW,curses.COLOR_BLUE)
	curses.init_pair(7,curses.COLOR_WHITE,curses.COLOR_BLUE)
	curses.init_pair(8,curses.COLOR_WHITE,curses.COLOR_WHITE)
	curses.init_pair(9,curses.COLOR_YELLOW,curses.COLOR_YELLOW)
	curses.init_pair(10,curses.COLOR_BLACK,curses.COLOR_BLACK)
	
    def check_windows(self):
	""" how many windows are in the list """
	wlen = len(self.winlist)
	return wlen

    def create_window(self,sizex,sizey,posx,posy):
	""" function for creating a new window """
	win = curses.newwin(sizex,sizey,posx,posy)
	self.winlist.append(win)
	return win

    def compute_strpos(self,win,pos,string):
	""" find relative positions for texts in the middle of the window"""
	sizex,sizey = win.getmaxyx()
	if pos == 1:
	    l = len(string)
	    spos = sizey - l
	    rpos = spos /2
	
	return rpos

    def write_window(self,win,posx,posy,text,attr):
	""" wrapper function for writing strings to a window """
	if posx!=-1 and posy!=-1 and attr !=-1:
	    win.addstr(posx,posy,text,attr)
	elif posx!=-1 and posy!=-1 and attr == -1:
	    win.addstr(posx,posy,text)
	elif posx==-1 and posy==-1 and attr == -1:
	    win.addstr(text)
	elif posx==-1 and posy==-1 and attr !=-1:
	    win.addstr(text,attr)
	
	win.refresh()

    def config_window(self,win,func):
	if func==1:
	    win.box()
	    win.refresh()
	elif func == 2:
	    win.erase()
	    win.refresh()
    
    def generate_map(self,x,y):
	fill = 35 # 35 is the fill element '#'
	gmap = []
	fields = x*y
	i = 0
	for cx in range(0,x):
	    for cy in range(0,y):
		gmap.append([cx,cy,32])
	    i+=1
	i+=1
	self.gmap = gmap
	
    def generate_monster(self,f,t):

	#gmap
	gmap = self.gmap
	#monsters
	ms = [f,t]
	ms = random.randint(ms[0],ms[1])
	l = len(gmap)-1
	mmap=[]

	for g in range(0,ms):
	    while 1:
		p = random.randint(0,l)
		if (gmap[p][0] != 0 and gmap[p][1] != 0) and (gmap[p][0] != 23 and gmap[p][1] != 79):
		    gmap[p][2] = 164
		    mmap.append(gmap[p])
		    break
	
	self.gmap = gmap
	self.mmap = mmap
	self.ms = ms

    def generate_gold(self,f,t):

	gmap = self.gmap

        #gold aka 0days
	gold = [f,t]
	gold = random.randint(gold[0],gold[1])
	l = len(gmap)-1

	for g in range(0,gold):
	    while 1:
		p = random.randint(0,l)
		if (gmap[p][0] != 0 and gmap[p][1] != 0) and (gmap[p][0] != 23 and gmap[p][1] != 79):
		    gmap[p][2] = 163
		    self.gomap.append(gmap[p])
		    break

	self.gold = gold
	self.gmap = gmap

    def generate_item(self,f,t,item):

	gmap = self.gmap
	#chill number 35
	f = [f,t]
	f = random.randint(f[0],f[1])
	l = len(gmap)-1
	for g in range(0,f):
	    while 1:
		p = random.randint(0,l)
		if (gmap[p][0] != 0 and gmap[p][1] != 0) and (gmap[p][0] != 23 and gmap[p][1] != 79) and gmap[p][2] != 163:
		    gmap[p][2] = item
		    break
	
	self.gmap = gmap

    def throw_items(self,win,rc):
	""" populate the map with the window with pre-generated items in gmap """
	gmap = self.gmap

	#general map
	for val in gmap:
	    if (val[0] != 0 and val[1] != 0) and (val[0] != 23 and val[1] != 79):
		if val[2] == 163:
		    win.addstr(val[0],val[1],chr(val[2]),curses.A_REVERSE)
		    win.refresh()
		elif val[2] == 164:
		    win.addstr(val[0],val[1],chr(val[2]),curses.color_pair(5))
		    win.refresh()
		else:
		    win.addstr(val[0],val[1],chr(val[2]),curses.color_pair(rc))
		    win.refresh()
	win.refresh()


	self.gmap = gmap

    def update_lifebar(self,win):
	""" show the player whats going on """

	#save my coordinates
	me = win.getyx()

	#which level
	collect = "lvl:%s" % (self.lvl)
	win.addstr(0,3,collect)
	
	#how much zerodays to grep
	gold = "%s / %s" % (self.gcount,self.gold)
	win.addstr(0,12,gold)

	#zeroday collection
	collect = "xploitz: %s" % (self.collected)
	win.addstr(0,20,collect)

	#lives
	lives = "live: %d" % (self.lives)
	win.addstr(0,35,lives)

	#knights name
	name = "%s" % (self.name)
	win.addstr(0,50,name)

	#time
	#time = "%s" % (self.time)
	#win.addstr(0,70,time)


	#how many fedz and whittezzzz
	fedz = "%s fedz" % (str(self.ms))
	win.addstr(23,3, fedz)

	#published by wh and eaten by fedz
	ate = "[%s]" % (str(self.eaten))
	win.addstr(23,20, ate)

	win.move(me[0],me[1])
	win.refresh()
	
    def check_object(self,win):
	""" check if a monster ate our zeroday """
#	f = open('logme.txt','a')
	mmap = self.mmap
	gomap = self.gomap
	for gold in gomap:
	    for monster in mmap:
		if gold[0] == monster[0] and gold[1] == monster[1]:
		    self.eaten=int(self.eaten) + 1
		    gomap.remove(gold)
		    #g = "%s\n" % (gold)
		    #f.write(g)
		    #m = "%s\n" % (monster)
		    #f.write(m)
		    self.update_lifebar(win)
	#f.close()
	self.gomap = gomap

    def check_position(self,win):
	""" checks position for gold, this function should be optimized as
	    by now the whole gmap is searched, which could be done simpler """

	gmap = self.gmap
	i=0
	me = win.getyx()
	for val in gmap:
	    if me[0] == val[0] and me[1] == val[1] and val[2] == 163:

		self.gcount = int(self.gcount) + 1
		self.elive = int(self.elive) + 1
		self.collected = int(self.collected) + 1
		self.update_lifebar(win)

		#changing the field - clearing space
		win.addch(me[0],me[1]," ")

		#clearing space in table
		gmap[i][2]=32

		#ok i am back at the same old place
		win.move(me[0],me[1])
		win.refresh()
		self.gmap = gmap
	    i+=1
    
    def check_collision(self,win):
	""" lets check if a monster is byting our ass """

	me = win.getyx()
	mmap = self.mmap

	for val in mmap:
	    if val[0] == me[0] and val[1] == me[1]: 
		self.lives = self.lives - 1
		return 1

	return -1

    def move_monster(self,win):
	gmap = self.gmap
	mmap = self.mmap
	i=0
	me = win.getyx()
	for val in mmap:
    
	    m = random.randint(1,4)

#check what direction the random gen spitted
#check if monster has reached the cage

	    if m == 1: 
		if val[0]!=1:
		    win.addstr(val[0],val[1]," ")
		    x = val[0]
		    x = x - 1
		    mmap[i][0] = x
		    win.addstr(x,val[1],"O",curses.color_pair(5))
		    win.refresh()

	    elif m == 2: 
		if val[0]!=self.sizex-2:
		    win.addstr(val[0],val[1]," ")
		    x = val[0]	
		    x = x + 1
		    mmap[i][0] = x
		    win.addstr(x,val[1],"O",curses.color_pair(5))
		    win.refresh()

	    elif m == 3: 
		if val[1]!=1:
		    win.addstr(val[0],val[1]," ")
		    y = val[1]	
		    y = y - 1
		    mmap[i][1] = y
		    win.addstr(val[0],y,"O",curses.color_pair(5))
		    win.refresh()

	    elif m == 4: 
		if val[1]!=self.sizey-2:
		    win.addstr(val[0],val[1]," ")
		    y = val[1]	
		    y = y + 1
		    mmap[i][1] = y 
		    win.addstr(val[0],y,"O",curses.color_pair(5))
		    win.refresh()
#former monster field is empty now
	    i+=1

	win.move(me[0],me[1])
	win.refresh()
	self.mmap = mmap

    def move_cursor(self,win, x,y):
	""" for other useful and great animations """
	win.move(x,y)

    def delete_item(self, win, item, x,y):
	""" for deleting the littel things at the position xy """
	win.addch(x,y,item)

    def move_item(self, win, item, x,y,color):
	""" for moving "sprites" :) """
	win.move(x,y)
	self.write_window(win,x,y,item,color)
#	win.refresh()

    def move_player(self,action,win):

	a = action
	xy = win.getyx()
	x=xy[0]
	y=xy[1]

	win.addch(x,y," ")
	if a == 65:
	    if x!=1:
		win.move(x-1,y)
		win.refresh()
	    else:
		win.move(x,y)
		win.refresh()

	elif a == 66:
	    if x!=self.sizex-2:
		win.move(x+1,y)
		win.refresh()
	    else:
		win.move(x,y)
		win.refresh()

	elif a == 68:
	    if y!=1:
		win.move(x,y-1)
		win.refresh()
	    else:
		win.move(x,y)
		win.refresh()

	elif a == 67:
	    if y!=self.sizey-2:
		win.move(x,y+1)
		win.refresh()
	    else:
		win.move(x,y)
		win.refresh()
