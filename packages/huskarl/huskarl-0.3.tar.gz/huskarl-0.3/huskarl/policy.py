import random
import numpy as np
from scipy.stats import truncnorm


class Policy:
	"""Abstract base class for all implemented policies.
	
	Do not use this abstract base class directly but instead use one of the concrete policies implemented.

	A policy ultimately returns the action to be taken based on the output of the agent.
	The policy is the place to implement action-space exploration strategies.
	If the action space is discrete, the policy usually receives action values and has to pick an action/index.
	A discrete action-space policy can explore by pick an action at random with a small probability e.g. EpsilonGreedy.
	If the action space is continuous, the policy usually receives a single action or a distribution over actions.
	A continuous action-space policy can simply sample from the distribution and/or add noise to the received action.	
	
	To implement your own policy, you have to implement the following method:
	"""
	def act(self, **kwargs):
		raise NotImplementedError()


# Discrete action-space policies =======================================================================================


class Greedy(Policy):
	"""Greedy Policy

	This policy always picks the action with largest value.
	"""
	def act(self, qvals):
		return np.argmax(qvals)


class EpsGreedy(Policy):
	"""Epsilon-Greedy Policy
	
	This policy picks the action with largest value with probability 1-epsilon.
	It picks a random action and therefore explores with probability epsilon.
	"""
	def __init__(self, eps):
		self.eps = eps

	def act(self, qvals):
		if random.random() > self.eps:
			return np.argmax(qvals)
		return random.randrange(len(qvals))


class GaussianEpsGreedy(Policy):
	"""Gaussian Epsilon-Greedy Policy

	Like the Epsilon-Greedy Policy except it samples epsilon from a [0,1]-truncated Gaussian distribution.
	This method is used in "Asynchronous Methods for Deep Reinforcement Learning" (Mnih et al., 2016).
	"""
	def __init__(self, eps_mean, eps_std):
		self.eps_mean = eps_mean
		self.eps_std = eps_std
	
	def act(self, qvals):
		eps = truncnorm.rvs((0 - self.eps_mean) / self.eps_std, (1 - self.eps_mean) / self.eps_std)
		if random.random() > eps:
			return np.argmax(qvals)
		return random.randrange(len(qvals))


# Continuous action-space policies (noise generators) ==================================================================


class PassThrough(Policy):
	"""Pass-Through Policy

	This policy simply outputs the model's raw output, unchanged.
	"""
	def act(self, action):
		return action


class OrnsteinUhlenbeck(Policy):
	"""Ornstein-Uhlenbeck Policy

	This policy adds noise sampled from an Ornstein-Uhlenbeck process to the model's output.
	"""
	def __init__(self):
		self.oup = OrnsteinUhlenbeckProcess(theta=.15, mu=0., sigma=.3)

	def act(self, action):
		return action + self.oup.sample()






















import numpy as np


class RandomProcess(object):
    def reset_states(self):
        pass


class AnnealedGaussianProcess(RandomProcess):
    def __init__(self, mu, sigma, sigma_min, n_steps_annealing):
        self.mu = mu
        self.sigma = sigma
        self.n_steps = 0

        if sigma_min is not None:
            self.m = -float(sigma - sigma_min) / float(n_steps_annealing)
            self.c = sigma
            self.sigma_min = sigma_min
        else:
            self.m = 0.
            self.c = sigma
            self.sigma_min = sigma

    @property
    def current_sigma(self):
        sigma = max(self.sigma_min, self.m * float(self.n_steps) + self.c)
        return sigma


class GaussianWhiteNoiseProcess(AnnealedGaussianProcess):
    def __init__(self, mu=0., sigma=1., sigma_min=None, n_steps_annealing=1000, size=1):
        super(GaussianWhiteNoiseProcess, self).__init__(mu=mu, sigma=sigma, sigma_min=sigma_min, n_steps_annealing=n_steps_annealing)
        self.size = size

    def sample(self):
        sample = np.random.normal(self.mu, self.current_sigma, self.size)
        self.n_steps += 1
        return sample

# Based on http://math.stackexchange.com/questions/1287634/implementing-ornstein-uhlenbeck-in-matlab
class OrnsteinUhlenbeckProcess(AnnealedGaussianProcess):
    def __init__(self, theta, mu=0., sigma=1., dt=1e-2, size=1, sigma_min=None, n_steps_annealing=1000):
        super(OrnsteinUhlenbeckProcess, self).__init__(mu=mu, sigma=sigma, sigma_min=sigma_min, n_steps_annealing=n_steps_annealing)
        self.theta = theta
        self.mu = mu
        self.dt = dt
        self.size = size
        self.reset_states()

    def sample(self):
        x = self.x_prev + self.theta * (self.mu - self.x_prev) * self.dt + self.current_sigma * np.sqrt(self.dt) * np.random.normal(size=self.size)
        self.x_prev = x
        self.n_steps += 1
        return x

    def reset_states(self):
        self.x_prev = np.random.normal(self.mu,self.current_sigma,self.size)




