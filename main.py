import flying_shot
import DQN
import Dueling_DQN
import numpy as np
import Util
import SkipAndStack
import ExperienceReplay
import tensorflow as tf
import matplotlib.pyplot as plt

import os


def main():

    game = flying_shot.GAME()

    #network
    #network = DQN.DQN()
    network = Dueling_DQN.DQN()
    network.update_target()

    game.game_init()
    game_state = 'Explore'

    #stack
    stack = SkipAndStack.skipAndStack()

    #experience replay
    experience = ExperienceReplay.experienceReplay()

    #saver
    saver = tf.train.Saver()

    #make dir
    if not os.path.exists('model/'):
        os.mkdir('model/')

    # if you want restore model
    #saver.restore(network.sess, network.save_file)



    #initialization
    state = game.game_init()
    state = Util.img_resize(state)

    # 초기 state를 동일하게 넣어줌
    for i in range(stack.Num_skipping * stack.Num_stacking):
        stack.state_set.append(state)


    stacked_state = stack.skip_and_stack_frame(state)

    max_step = 10001
    total_episodes = 50000
    episode = 0
    total_reward = 0
    total_step = 0

    step_progress = []
    reward_progress = []

    win_count = 0
    loose_count = 0

    while episode < total_episodes:
        step = 0
        while step <= max_step:

            #select action
            action = network.select_action(stacked_state)

            #take state, reward, termial
            next_state, reward, done, win, shot_bat_count = game.step(np.argmax(action))
            next_state = Util.img_resize(next_state)
            stacked_next_state = stack.skip_and_stack_frame(next_state)

            #input experience replay
            experience.experience_replay(stacked_state, action, reward, stacked_next_state, done)

            #training Q_table
            if episode > 10:
                if episode >= 10:
                    game_state = 'Training'
                network.train(experience.replay_memory)
            else:
                network.epsilon = network.first_epsilon

            if total_step % 20000 == 0:
                saver.save(network.sess, network.save_file)

            if total_step % network.Num_target_update == 0:
                network.update_target()

            step += 1
            total_step += 1
            total_reward += reward
            stacked_state = stacked_next_state

            if total_step % 100 == 0 and game_state == 'Training':
                print("episode: {} step: {} total_step: {} total_reward: {} epsilon: {} win_count_rate: {}".
                    format(episode, step, total_step, total_reward, network.epsilon, win_count / episode))

                if len(step_progress) > 100:
                    del step_progress[0]
                    del reward_progress[0]
                step_progress.append(total_step)
                reward_progress.append(total_reward)

                #plotting
                plt.xlabel("steps")
                plt.ylabel("total reward")
                plt.grid(True)
                plt.plot(step_progress, reward_progress, ms=5)
                plt.draw()
                plt.pause(0.000001)

            if done or step > max_step:
                if win == True:
                    print("승리")
                    win_count += 1
                elif win == False:
                    print("패배")
                    loose_count += 1
                break

        episode += 1
        game.restart()

if __name__=='__main__':
    main()