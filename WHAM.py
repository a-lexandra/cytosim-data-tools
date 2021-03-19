import numpy as np
import os

import matplotlib.pyplot as plt

class Clone:
	# For a single clone
	def __init__(self):
		self.num_frames = self.get_num_frames()

		self.wDots_array = self.get_wDots()

		self.wDotIntegral = self.get_wDotIntegral()

		# inverse k_B*T
		self.beta = 1


	def get_num_frames(self):
		num_frames = 0

		curr_dir = os.getcwd()

		num_frames = len(open("wDots.txt").readlines()) - 1

		return num_frames

	def get_wDots(self):
		with open ('wDots.txt', 'r') as file:
			# https://stackoverflow.com/a/6583635
			wDots_array = [[float(x) for x in line.split()] for line in file]

		return np.array(wDots_array)

	def get_wDotIntegral(self):
		with open('wDotIntegral.txt', 'r') as file:
			# https://stackoverflow.com/a/6583635
			wDotIntegral = [float(x) for x in next(file).split()]

		return wDotIntegral[0]

class Alpha:
	# For a single value of alpha
	def __init__(self):
		# alpha
		self.bias_param = self.get_bias_param()

		# Read number of clones from iteration directory
		self.num_clones = self.get_num_clones()

		# Array of Clone objects
		self.clone_array = self.get_clone_data()

		# c_a
		self.bias_factor_array = self.calculate_bias_factors()

		# N_a
		self.num_samples = self.get_num_samples()

		# n_a
		self.wDot_data_all_clones = self.combine_wDot_data()

		#f_a
		self.norm_factor = 1

	def get_bias_param(self):
		with open('alpha.txt', 'r') as file:
			alpha = [float(x) for x in next(file).split()]

		return alpha[0]

	def get_num_clones(self):
		num_clones = 0

		root_dir = os.getcwd()

		# Go through the entries in the current directory
		with os.scandir(root_dir) as entries:
			for entry in entries:
				# Only count entries that are directories and have clone in name
				if entry.is_dir() and "clone" in entry.name:
					num_clones += 1

		return num_clones

	def get_clone_data(self):
		root_dir = os.getcwd()

		clone_array = []

		with os.scandir(root_dir) as entries:
			for entry in entries:
				if entry.is_dir() and "clone" in entry.name:
					os.chdir(entry)
					CloneInstance = Clone()
					clone_array.append(CloneInstance)

		return clone_array

	def calculate_bias_factors(self):
		bias_factor_array = []

		for clone in self.clone_array:
			bias_factor = np.exp(-clone.beta * self.bias_param * clone.wDotIntegral)
			bias_factor_array.append(bias_factor)

		return np.array(bias_factor_array)

	def get_num_samples(self):
		num_samples = 0

		for clone in self.clone_array:
			num_samples += clone.num_frames

		return num_samples

	def combine_wDot_data(self):
		wDots = []

		for clone in self.clone_array:
			wDots.append(clone.wDots_array[1:,1])

		wDots_array = np.array(wDots).flatten()

		return wDots_array

class Histogram():
	def __init__(self):
		self.alpha_array = self.get_alpha_data()

		self.wDot_data_all_alphas = self.combine_wDot_data()

		self.wDot_hist, self.wDot_hist_bin_edges = \
			np.histogram(self.wDot_data_all_alphas, bins="auto")

		self.prob_dist = self.calculate_prob_dist()

	def get_alpha_data(self):
		root_dir = os.getcwd()

		alpha_array = []

		with os.scandir(root_dir) as entries:
			for entry in entries:
				if entry.is_dir():
					os.chdir(entry)
					AlphaInstance = Alpha()
					alpha_array.append(AlphaInstance)

		return alpha_array

	def combine_wDot_data(self):
		wDots = []

		for alpha in self.alpha_array:
			wDots.append(alpha.wDot_data_all_clones)

		wDots_array = np.array(wDots).flatten()

		return wDots_array

	def calculate_prob_dist(self):
		denominator = 0

		for alpha in self.alpha_array:
			denominator += alpha.num_samples * alpha.norm_factor * np.sum(alpha.bias_factor_array)

		return self.wDot_hist/denominator

	def calculate_norm_factors(self):
		for alpha in self.alpha_array:
			alpha.norm_factor = 1 / (np.sum(alpha.bias_factor_array)*np.sum(self.prob_dist))


	def monitor_convergence(self):
		pass

	def iterate_WHAM(self):
		for i in range(0,10):
			self.prob_dist = self.calculate_prob_dist()
			self.calculate_norm_factors()

		plt.plot(self.wDot_hist_bin_edges[:-1], self.prob_dist)
		plt.show()

myHistogram = Histogram()

myHistogram.iterate_WHAM()
