#!/usr/bin/env python3
import time
import mpv

player = mpv.MPV()

player.loop = True
player.play('1.mp4')

player.wait_until_playing()



while not player._core_shutdown:
   x = input()
   if (x == 'p'):
      if (player._get_property("pause") == True):
         player._set_property("pause", False)
         continue
      player._set_property("pause", True)
   else:
      continue
   