#!/usr/bin/env python
#this is not even an exploit!!!1111

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


import cmatescenes
import cmatelib
import random
import curses
import sys
import time

def play_level(win1,win2,cm,mspeed):

    try:
	    cm.update_lifebar(win1)
	    win1.move(cm.sizex/2,cm.sizey/2)
	    curses.curs_set(1)
	    win1.nodelay(1)
	    o=0
	    while 1:
		a = win1.getch()
		if a == 65:
		    cm.move_player(a,win1)
		elif a == 66:
		    cm.move_player(a,win1)
		elif a == 68:
		    cm.move_player(a,win1)
		elif a == 67:
		    cm.move_player(a,win1)
		elif a == 112:
		    cmatescenes.pause_game(win2,cm)
		    win1.redrawwin()

		cm.check_position(win1)
	    
		if (o%mspeed == 0):
		    cm.move_monster(win1)

		#watch out for ur lifes
		ret = cm.check_collision(win1)
		if ret == 1:
		    cmatescenes.lost_a_live(win2,cm)
		    win1.move(cm.sizex-2,cm.sizey-2)
		    time.sleep(2)
		    cm.update_lifebar(win1)
		    win1.redrawwin()
		if cm.lives < 0:
		    cmatescenes.ur_dead(win2,cm)
		    return -1
		
		#check if a zero day was eaten
		cm.check_object(win1)

		if cm.gcount + cm.eaten >= cm.gold:
		    cmatescenes.congrats(win2,cm)
		    return 0
		if cm.gold == cm.gcount:
		    cmatescenes.congrats(win2,cm)
		    return 0
		o+=1

		if cm.elive == 35:
		    cm.lives+=1
		    cm.elive = 0

    except KeyboardInterrupt:
	if cmatescenes.really_quit(win2,cm) != -1:
	    cm.close_stdscr()
	    sys.exit(1)

def create_level(win1,win2,cm,ming,maxg,minm,maxm):
    rc = random.randint(0,10) 
    cm.config_window(win1,1)
    cm.generate_map(cm.sizex-1,cm.sizey-1)
    cm.generate_item(500,1000,35)
    cm.generate_gold(int(ming),int(maxg))
    cm.generate_monster(int(minm),int(maxm))
    cm.throw_items(win1,rc)
    cmatescenes.level_info(win2,cm)
    cm.throw_items(win1,rc)
    cm.update_lifebar(win1)
    win1.move(cm.sizex/2,cm.sizey/2)
    win1.refresh()

cm = cmatelib.cmate()
cm.create_stdscr()
cm.create_colors()

cm.sizex=24
cm.sizey=80

cmatescenes.pre_intro(cm,2)
cmatescenes.intro(cm)
win1 = cm.create_window(cm.sizex,cm.sizey,0,0)
win2 = cm.create_window(8,50,5,16)
win3 = cm.create_window(16,50,5,16)
cmatescenes.start_of_game(win3,cm)

#open level file
l = open('levelfile.txt','r')
for lvl in l.readlines():
	    if lvl[0]!='#' and lvl[0]!='\n':
		    cm.gcount=0
		    cm.eaten=0
		    cm.gomap=[]
		    cm.mmap=[]
		    items = lvl.split(',')	 
		    level=items[0]
		    ming=items[1]
		    maxg=items[2]
		    minm=items[3]
		    maxm=items[4]
		    mspeed=items[5]
		    cm.lvl=level
		    create_level(win1,win2,cm,ming,maxg,minm,maxm)

		    while 1:
			ret = play_level(win1,win2,cm,int(mspeed))
			if ret ==0:
			    break
			elif ret ==-1:
			    endgame=-1
			    cm.close_stdscr()
			    sys.exit(1)

		    cmatescenes.pre_intro(cm,1)

cmatescenes.end_of_game(win2,cm)

#the end
cm.close_stdscr()
