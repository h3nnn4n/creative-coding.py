import os
import random


class RandomController:
    def __init__(self, seed=None):
        if seed is None:
            self.set_random_seed()
        else:
            self.set_seed(seed)

    def set_random_seed(self):
        random_data = os.urandom(6)
        seed = int.from_bytes(random_data, byteorder="big")
        random.seed(seed)
        print('seed(%d)' % seed)

        self.seed = seed

    def set_seed(self, seed):
        random.seed(seed)

        self.seed = seed
