# 112tp
15-112 Term Project

TP3

Description:
This is an off brand fruit ninja. It is a remake of the classic Fruit Ninja game, where user can use their mouse to slice 'fruits' and avoid attacks from the bombs. User could also play the hand mode and use their hands to slice the fruits and avoid bomb attacks with their heads. 

Required modules:
  OpenCV, MediaPipe, PIL, CMU(CS3) graphics, random, math
  
OpenCV: pip install opencv-python

MediaPipe: pip install mediapipe

How to play:
  After downloading the file, unzip and all needed files will be in there. Start the game by running main.py.
  Once the game has started, there will be two different modes, normal mode and hand mode.
    Normal Mode:
    
      Move your mouse to slice the fruits(red dots), each red dot is 1 point
      Frenzy fruits(yellow dots) will randomly drop from above, where frenzy will be activated if sliced. Frenzy mode will have more fruits concentrated in a moving area(boids algorithim).
      If you hit a bomb(black dots), game over. You can restart by hitting the back button to the main menu.
   Hand Mode:
   
      In this mode, user will need to use their hand to slice the fruits.
      Same as normal mode, frenzy fruits(yellow dots) will activate frenzy.
      Smart Bombs(green dots) will be thrown towards your face, you will have to avoid the bomb by moving your head around and make sure the bomb does not touch the rectangle around your face.
           
  
