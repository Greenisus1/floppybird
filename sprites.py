"""Original floppy-disk sprite and 1/0 digit pipes, ANSI RGB half blocks, green on black."""
import os
PALETTE={'.':None,'G':(32,178,60),'S':(180,255,180),'W':(220,255,220),'K':(10,40,15)}
ART={
 'floppy':('GGGGGGGG','GGGGGSSG','GGGGGSSG','GGGGGGGG','GWWWWWWG','GWKKKWWG','GWWWWWWG','GGGGGGGG')}
DIGITS={
 '1':('.g.','gg.','.g.','.g.','ggg'),
 '0':('ggg','g.g','g.g','g.g','ggg')}
PIPE_HI=(57,255,20);PIPE_LO=(16,89,30);CAP=(120,255,90)
def supported():return os.environ.get('COLORTERM','').lower() in ('truecolor','24bit') or 'direct' in os.environ.get('TERM','').lower()
def frame(g,w,h):
 OY=2
 width=w;height=(h-OY)*2
 canvas=[[(0,0,0) for _ in range(width)] for _ in range(height)]
 for i,p in enumerate(g['pipes']):
  px=round(p['x']);pw=g['pipew'];gap_top=round(p['gap']);gap_bot=gap_top+g['gap_h']
  for y in range(height):
   if gap_top<=y//2+OY<gap_bot:continue
   for x in range(max(0,px),min(width,px+pw)):canvas[y][x]=PIPE_LO
  for gy in range(0,height,6):
   if gap_top<=gy//2+OY<gap_bot:continue
   digit=DIGITS['1' if (gy//6+i)%2==0 else '0']
   for yy in range(5):
    if gap_top<=(gy+yy)//2+OY<gap_bot:continue
    for xx in range(3):
     if digit[yy][xx]=='g':
      for x in range(max(0,px),min(width,px+pw)):
       if 0<=gy+yy<height and x%4==xx%4:canvas[gy+yy][x]=PIPE_HI
  for cap_row in (gap_top-1,gap_bot):
   if OY<=cap_row<h:
    for x in range(max(0,px),min(width,px+pw)):canvas[(cap_row-OY)*2][x]=CAP;canvas[min(height-1,(cap_row-OY)*2+1)][x]=CAP
 for yy in range(8):
  for xx in range(8):
   color=PALETTE[ART['floppy'][yy][xx]]
   x=g['bx']+xx;y=(round(g['by'])-OY)*2-4+yy
   if color is not None and 0<=x<width and 0<=y<height:canvas[y][x]=color
 out=[]
 for y in range(0,height,2):
  out.append(f'\x1b[{y//2+1+OY};1H');fg=bg=None
  for x in range(width):
   a,b=canvas[y][x],canvas[y+1][x]
   if a!=fg:out.append('\x1b[38;2;'+';'.join(map(str,a))+'m');fg=a
   if b!=bg:out.append('\x1b[48;2;'+';'.join(map(str,b))+'m');bg=b
   out.append('▀')
 out.append('\x1b[0m');return ''.join(out)
