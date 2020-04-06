# FlyingShot-RL

Abstract
-------------
This is a project to make and evaluate a game named FlyingShot.

Make DQN with 3 conv layer and 2 fully connected layer.

### Applied technique
> * Dueling Network
> * Experience Replay
> * Frame Skipping & Stacking
> * Target Network


### Game Environment

![explain_photo](https://user-images.githubusercontent.com/33660224/78472605-43c3b600-7775-11ea-89ff-de55a7155d8b.jpg)
> * FlyingShot has 3 actions-> UP, DOWN, SHOOT
> * The game gives you state, reward, terminal, win_status
> * There are 2 enemies-> Bat, Fireball
> * Fireball is invulnerable
> * If the agent kills 10 bats without dying, gets reward: 1
> * If the agent is hit a bat or a fireball, the agent will dead, gets reward : -1


![reward_progress](https://user-images.githubusercontent.com/33660224/78471816-ffcdb280-776e-11ea-9a70-cb372f24b4fc.png)
> * After about 260,000 steps, the agent learned how to win the game.


Requirements
-------------
* tensorflow-gpu=1.15.0
* pygame=1.9.6
* numpy
* matplotlib
* openCV


FlyingShot demo
-------------
[![demo](http://img.youtube.com/vi/T6Ud1fAa9Iw/0.jpg)](https://www.youtube.com/watch?v=T6Ud1fAa9Iw)

Reference
-------------
https://blog.naver.com/samsjang/220710524226
