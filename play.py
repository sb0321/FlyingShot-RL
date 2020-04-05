import flying_shot
import DQN
import Dueling_DQN
import numpy as np
import Util
import SkipAndStack
import tensorflow as tf
import matplotlib.pyplot as plt
from time import sleep


def main():

    game = flying_shot.GAME()

    #network
    #network = DQN.DQN()
    network = Dueling_DQN.DQN()
    network.update_target()

    #saver
    saver = tf.train.Saver()
    saver.restore(network.sess, 'model/model.ckpt')

    #initialization
    state = game.game_init()
    state = Util.img_resize(state)

    #stack
    stack = SkipAndStack.skipAndStack()
    # 초기 state를 동일하게 넣어줌
    for i in range(stack.Num_skipping * stack.Num_stacking):
        stack.state_set.append(state)

    stacked_state = stack.skip_and_stack_frame(state)

    max_step = 10001
    total_episodes = 50000
    episode = 0
    total_reward = 0
    total_step = 0
    win_count = 0
    loose_count = 0
    while episode < total_episodes:
        step = 0
        while step <= max_step:
            sleep(0.01)
            #select action
            action = network.select_action_testing(stacked_state)

            #take state, reward, termial
            next_state, reward, done, win, shot_bat_count = game.step(np.argmax(action))
            next_state = Util.img_resize(next_state)
            stacked_next_state = stack.skip_and_stack_frame(next_state)

            step += 1
            total_step += 1
            total_reward += reward
            stacked_state = stacked_next_state

            if episode > 0 and total_step % 100 == 0:
                print("episode: {} step: {} total_step: {} total_reward: {} epsilon: {} win_count_rate: {} shot: {}".
                    format(episode, step, total_step, total_reward, network.epsilon, win_count / episode, shot_bat_count))

            if done or step > max_step:
                if win == True:
                    print("승리")
                    win_count += 1

                elif win == False:
                    print("패배")
                    plt.imshow(stack.state_set[len(stack.state_set) - 1])
                break

        episode += 1

if __name__=='__main__':
    main()