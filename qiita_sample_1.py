import matplotlib.pyplot as plt
import numpy as np


class HiddenMarkovModel(object):

    def __init__(self, n_states_hidden, n_states_observe):
        # 潜在変数の状態数 |Q|
        self.n_states_hidden = n_states_hidden                      # e.g: 2
        # 観測変数の状態数 |Σ|
        self.n_states_observe = n_states_observe                    # e.g: 2
        # 初期状態確率分布  π
        self.initial = np.ones(n_states_hidden) / n_states_hidden   # e.g: (0.5, 0.5)
        # 状態遷移確率分布  A
        self.transition = np.ones((n_states_hidden, n_states_hidden)) / (2 * n_states_hidden)  # ([[0.25,0.25],[0.25,0.25]])
        self.transition += np.eye(n_states_hidden) * 0.5
        # 記号出力確率分布  B
        self.observation = np.random.rand(n_states_observe, n_states_hidden)
        self.observation /= np.sum(self.observation, axis=0, keepdims=True)

    # π, A, B の最尤推定
    def fit(self, sequence, iter_max=100):
        # repeat EM algorithm
        for i in range(iter_max):
            params = np.hstack((self.transition.ravel(), self.observation.ravel()))  # np.ravel() returns a contiguous flattened array  # np.hstack() stacks arrays in sequence horizontally
            p_hidden, p_transition = self.expectation(sequence)
            self.maximization(sequence, p_hidden, p_transition)
            if np.allclose(params, np.hstack((self.transition.ravel(), self.observation.ravel()))):  # np.allclose() returns True if two arrays are element-wise equal within a tolerance
                break

    def expectation(self, sequence):
        N = len(sequence)
        forward = np.zeros(shape=(N, self.n_states_hidden))
        forward[0] = self.initial * self.observation[sequence[0]]
        backward = np.zeros_like(forward)
        backward[-1] = self.observation[sequence[-1]]
        for i in range(1, len(sequence)):
            forward[i] = self.transition.dot(forward[i - 1]) * self.observation[sequence[i]]
        for j in range(N - 2, -1, -1):
            backward[j] = (self.observation[sequence[j + 1]] * backward[j + 1]).dot(self.transition)
        p_hidden = forward * backward
        p_hidden /= np.sum(p_hidden, axis=-1, keepdims=True)
        p_transition = self.transition * (self.observation[sequence[1:]] * backward[1:])[:, :, None] * forward[:-1, None, :]
        p_transition /= np.sum(p_transition, axis=(1, 2), keepdims=True)

        return p_hidden, p_transition

    def maximization(self, sequence, p_hidden, p_transition):
        self.initial = p_hidden[0] / np.sum(p_hidden[0])
        self.transition = np.sum(p_transition, axis=0) / np.sum(p_transition, axis=(0, 2))
        self.transition /= np.sum(self.transition, axis=0, keepdims=True)
        x = p_hidden[:, None, :] * (np.eye(self.n_states_observe)[sequence])[:, :, None]
        self.observation = np.sum(x, axis=0) / np.sum(p_hidden, axis=0)


def create_toy_data(sample_size=100):

    # inner function
    def throw_coin(bias):
        if bias == 1:
            return np.random.choice(range(2), p=[0.2, 0.8])
        else:
            return np.random.choice(range(2), p=[0.8, 0.2])
        # range(2)     => (0,2)
        # p=[0.2, 0.8] => p(x=0)=0.2, p(x=1)=0.8

    bias = np.random.uniform() > 0.5  # uniform() returns [0,1) on default
    coin = []
    cheats = []
    for i in range(sample_size):
        coin.append(throw_coin(bias))
        cheats.append(bias)
        bias = bias + np.random.choice(range(2), p=[0.99, 0.01])
        bias = bias % 2  # change the biased coin with a probabily of 0.01
    coin = np.asarray(coin)

    return coin, cheats


def main():
    coin, cheats = create_toy_data(200)
    print("coin  :", coin)
    print("cheats:", cheats)

    # we do not give the cheat to HMM; we try to guess this
    hmm = HiddenMarkovModel(2, 2)
    hmm.fit(coin, 100)                   # train 100 times
    p_hidden, _ = hmm.expectation(coin)  # get the result (100 trains + 1)
    print("p_hidden:", p_hidden)

    plt.plot(cheats)                     # answer data
    plt.plot(p_hidden[:, 1])             # trained result
    for i in range(0, len(coin), 2):
        plt.annotate(str(coin[i]), (i - .75, coin[i] / 2. + 0.2))
    plt.ylim(-0.1, 1.1)
    plt.show()


if __name__ == '__main__':
    main()


"""
code from below link
https://qiita.com/ctgk/items/ccfad9feeb937da07185
"""