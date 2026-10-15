#!/usr/bin/env python3
"""Original offline retro floppy-disk flyer. Python standard library only."""
import curses,os,json,random,time,sys
from pathlib import Path
from ui import put,run
import sprites
VERSION='1.0.0'
RECORD=Path.home()/'.local/share/floppybird/best.json'
class Flight:
 def __init__(self,h,w,seed=None):
  self.rng=random.Random(seed);self.h=h;self.w=w
  self.bx=max(4,w//6);self.by=h/2.;self.vy=0.;self.pipes=[];self.pipew=6
  self.score=0;self.over=False;self.dist=0.;self.nextpipe=w+8;self.message='Space/W/Up flaps. Thread the 1/0 pipes!'
 def speed(self):return 8+min(6,self.score*.15)
 def gap_h(self):return max(8,self.h//3-min(6,self.score//5))
 def flap(self):
  if self.over:return False
  self.vy=-6.5;return True
 def tick(self,dt):
  if self.over:return
  dt=min(.1,max(0,dt))
  self.vy=min(14,self.vy+22*dt);self.by+=self.vy*dt
  if self.by<1:self.by=1.;self.vy=max(0.,self.vy)
  self.dist+=self.speed()*dt
  self.nextpipe-=self.speed()*dt
  if self.nextpipe<=0:
   gh=self.gap_h();gy=self.rng.uniform(2,self.h-2-gh)
   self.pipes.append({'x':float(self.w),'gap':gy});self.nextpipe=26
  for p in list(self.pipes):
   p['x']-=self.speed()*dt
   if p['x']+self.pipew<0:self.pipes.remove(p);continue
   if not p.get('passed') and p['x']+self.pipew<self.bx:p['passed']=True;self.score+=1;self.message='Nice! Score '+str(self.score)+'.'
  if self.by>=self.h-3:self.by=self.h-3;self.over=True;self.message='Disk down. R restarts.';return
  for p in self.pipes:
   if p['x']<self.bx+4 and self.bx<p['x']+self.pipew:
    if self.by-1<p['gap'] or self.by+1>p['gap']+self.gap_h():
     self.over=True;self.message='Clipped a pipe. R restarts.';return
def best():
 try:
  if RECORD.is_symlink():return 0
  return max(0,int(json.loads(RECORD.read_text()).get('best',0)))
 except (OSError,ValueError,TypeError,AttributeError):return 0
def save(score):
 try:
  if any(p.is_symlink() for p in [RECORD,*RECORD.parents]):return False
  RECORD.parent.mkdir(parents=True,exist_ok=True,mode=0o700);tmp=RECORD.with_suffix('.tmp');fd=os.open(tmp,os.O_WRONLY|os.O_CREAT|os.O_TRUNC|os.O_NOFOLLOW,0o600)
  with os.fdopen(fd,'w') as f:json.dump({'best':max(score,best())},f)
  tmp.replace(RECORD);return True
 except OSError:return False
def palette():
 if not curses.has_colors():return False
 curses.start_color();curses.use_default_colors()
 values=[(46,-1),(82,-1),(28,-1),(22,-1)] if curses.COLORS>=256 else [(2,-1),(2,-1),(2,-1),(2,-1)]
 for i,(fg,bg) in enumerate(values,1):curses.init_pair(i,fg,bg)
 return True
def play(s):
 h,w=s.getmaxyx();g=Flight(h,w);last=time.monotonic();paused=False;recorded=False;high=best();pixels=sprites.supported() and '--ascii' not in sys.argv;colors=palette()
 def color(i):return curses.color_pair(i) if colors else 0
 while True:
  s.timeout(30);key=s.getch();now=time.monotonic();dt=now-last;last=now;h,w=s.getmaxyx();s.erase()
  if key in (27,ord('q'),ord('Q')):return
  if key in (ord('p'),ord('P')):paused=not paused
  if key in (ord('v'),ord('V')):pixels=not pixels;s.clear()
  if key in (ord('r'),ord('R')):g=Flight(h,w);paused=False;recorded=False
  if h<20 or w<60:put(s,1,1,'Resize to 60x20. Simulation paused. Q quits.');s.refresh();continue
  if not paused and not g.over:
   if key in (ord(' '),curses.KEY_UP,ord('w'),ord('W')):g.flap()
   g.tick(dt)
  if g.over and not recorded:g.message+=' Best saved.' if save(g.score) else ' Save unavailable.';recorded=True;high=max(high,best())
  if not pixels:
   for i,p in enumerate(g.pipes):
    gh=g.gap_h()
    for y in range(2,h-3):
     if p['gap']<=y<p['gap']+gh:continue
     for x in range(max(0,round(p['x'])),min(w,round(p['x'])+g.pipew)):
      put(s,y,x,'1' if (x+y+i)%2==0 else '0',color(2 if (x+y+i)%2==0 else 3))
    for cap in (round(p['gap'])-1,round(p['gap'])+gh):
     if 2<=cap<h-3:
      for x in range(max(0,round(p['x'])),min(w,round(p['x'])+g.pipew)):put(s,cap,x,'=',color(1))
   bird=('[## ]','[__]')
   for dy,line in enumerate(bird):
    put(s,round(g.by)-1+dy,g.bx,line,color(1))
  put(s,0,2,'FLOPPY BIRD | SCORE '+str(g.score)+' | BEST '+str(high)+(' | PAUSED' if paused else ''),color(1)|curses.A_BOLD)
  put(s,1,2,g.message,color(2))
  put(s,h-2,2,'Space/W/Up flap | P pause | V pixel/text | R restart | Q quit',color(2))
  put(s,h-1,2,'Pipes are made of 1s and 0s. Floor and pipes end the run.',color(3));s.refresh()
  if pixels:sys.stdout.write(sprites.frame(dict(pipes=g.pipes,pipew=g.pipew,gap_h=g.gap_h(),bx=g.bx,by=g.by),w,h));sys.stdout.flush()
if __name__=='__main__':
 if '--version' in sys.argv:print(VERSION)
 else:raise SystemExit(run(play))
