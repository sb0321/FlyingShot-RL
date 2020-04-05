import numpy as np
import DQN

class skipAndStack:

    def __init__(self):

        self.state_set = []
        self.Num_skipping = 4
        self.Num_stacking = 4

    def skip_and_stack_frame(self, state):
        self.state_set.append(state)

        state_in = np.zeros((80, 80, self.Num_stacking))

        for stack_frame in range(self.Num_stacking):
            state_in[:,:,stack_frame] = self.state_set[-1 - (self.Num_skipping * stack_frame)]

        del self.state_set[0]

        state_in = np.uint8(state_in)
        return state_in