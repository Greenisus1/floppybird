import unittest,tempfile
from pathlib import Path
from unittest.mock import patch
import floppybird as a

class Tests(unittest.TestCase):
 def test_initial(self):
  g=a.Flight(24,80);self.assertEqual(g.score,0);self.assertFalse(g.over);self.assertEqual(g.by,12.)
 def test_flap(self):
  g=a.Flight(24,80);self.assertTrue(g.flap());self.assertLess(g.vy,0)
 def test_gravity(self):
  g=a.Flight(24,80);v=g.vy;g.tick(.05);self.assertGreater(g.vy,v)
 def test_floor(self):
  g=a.Flight(24,80)
  for _ in range(200):
   if g.over:break
   g.tick(.1)
  self.assertTrue(g.over)
 def test_ceiling(self):
  g=a.Flight(24,80)
  for _ in range(30):g.flap();g.tick(.05)
  self.assertGreaterEqual(g.by,1);self.assertFalse(g.over)
 def test_pipe_spawn(self):
  g=a.Flight(24,80,1)
  for _ in range(130):
   if g.over:break
   g.flap() if g.by>14 else None;g.tick(.1)
  self.assertTrue(g.pipes or g.score>0)
 def test_score(self):
  g=a.Flight(24,80);g.by=5;g.vy=0
  g.pipes=[{'x':float(g.bx+2),'gap':3}]
  gh=g.gap_h()
  for _ in range(200):
   g.by=5;g.vy=0  # hover: hold the disk inside the gap
   g.tick(.05)
   if g.score:break
  self.assertEqual(g.score,1)
 def test_pipe_hit(self):
  g=a.Flight(24,80);g.by=20;g.pipes=[{'x':float(g.bx),'gap':2}]
  g.tick(.05);self.assertTrue(g.over)
 def test_gap_shrinks(self):
  g=a.Flight(24,80);base=g.gap_h();g.score=40;self.assertLessEqual(g.gap_h(),base);self.assertGreaterEqual(g.gap_h(),8)
 def test_speed_up(self):
  g=a.Flight(24,80);s0=g.speed();g.score=50;self.assertGreaterEqual(g.speed(),s0)
 def test_record(self):
  with tempfile.TemporaryDirectory() as d,patch.object(a,'RECORD',Path(d)/'best.json'):
   self.assertTrue(a.save(7));a.save(2);self.assertEqual(a.best(),7)
 def test_art(self):
  import sprites
  for name,rows in sprites.ART.items():self.assertEqual(len(rows),8);self.assertTrue(all(len(r)==8 for r in rows));self.assertTrue(all(c in sprites.PALETTE for r in rows for c in r))
  for name,rows in sprites.DIGITS.items():self.assertEqual(len(rows),5);self.assertTrue(all(len(r)==3 for r in rows))
 def test_frame(self):
  import sprites
  g={'pipes':[{'x':30,'gap':8}],'pipew':6,'gap_h':9,'bx':10,'by':12.0}
  for w,h in ((60,20),(110,40)):self.assertIn('38;2;',sprites.frame(g,w,h))
 def test_over_flap(self):
  g=a.Flight(24,80);g.over=True;self.assertFalse(g.flap())
if __name__=='__main__':unittest.main()
