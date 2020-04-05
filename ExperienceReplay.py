
class experienceReplay:

    def __init__(self):

        self.Num_replay_memory = 50000
        self.replay_memory = []


    def experience_replay(self, state, action, reward, next_state, terminal):

        if len(self.replay_memory) > self.Num_replay_memory:
            del self.replay_memory[0]

        self.replay_memory.append([state, action, reward, next_state, terminal])