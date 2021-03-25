import numpy as np
import os

import matplotlib.pyplot as plt

class Clone:
	# For a single clone
	def __init__(self):
		self.num_frames = self.get_num_frames()

		self.wDots_array = self.get_wDots()

		self.tau = self.wDots_array[-1,0]

		self.wDot_avg = np.mean(self.wDots_array[:,1])

		self.wDotIntegral = self.get_wDotIntegral()

		# wdi = 0 #np.trapz(self.wDots_array[:,1], self.wDots_array[:,0])
		# for idx in range( 1, self.wDots_array.shape[0]):
		# 	wdi += (self.wDots_array[idx,1]) * (self.wDots_array[idx,0] - self.wDots_array[idx-1,0])
		#
		# print(self.wDotIntegral, wdi, self.wDot_avg*self.tau)

		# inverse k_B*T
		self.beta = 1


	def get_num_frames(self):
		num_frames = 0

		curr_dir = os.getcwd()

		if os.path.exists('wDots.txt'):
			num_frames = len(open("wDots.txt").readlines()) - 1

		return num_frames

	def get_wDots(self):
		wDots_array = []
		if os.path.exists('wDots.txt'):
			with open ('wDots.txt', 'r') as file:
				# https://stackoverflow.com/a/6583635
				wDots_array = [[float(x) for x in line.split()] for line in file]

		return np.array(wDots_array)

	def get_wDotIntegral(self):
		if os.path.exists('wDotIntegral.txt'):
			with open('wDotIntegral.txt', 'r') as file:
				# https://stackoverflow.com/a/6583635
				wDotIntegral = [float(x) for x in next(file).split()]
				return wDotIntegral[0]
		else:
			wDotIntegral = 0 #np.trapz(self.wDots_array[:,1], self.wDots_array[:,0])
			for idx in range( 1, self.wDots_array.shape[0]):
				wDotIntegral += self.wDots_array[idx,1] * \
								(self.wDots_array[idx,0] - self.wDots_array[idx-1,0])

			return wDotIntegral

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

		self.bias_factor_sum = np.sum(self.bias_factor_array)



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

		os.chdir(root_dir)

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
			num_samples += 1 #clone.num_frames

		return num_samples

	def combine_wDot_data(self):
		wDots = []

		for clone in self.clone_array:
			wDots.append(clone.wDot_avg)

		wDots_array = np.array(wDots).flatten()

		return wDots_array

class Histogram():
	def __init__(self):
		self.alpha_array = self.get_alpha_data()

		self.wDot_data_all_alphas = self.combine_wDot_data()

		self.wDot_hist, self.wDot_hist_bin_edges = \
			np.histogram(self.wDot_data_all_alphas, bins="auto")

		self.wDot_hist_bin_centers = \
			0.5*(self.wDot_hist_bin_edges[1:] + self.wDot_hist_bin_edges[:-1])

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
					np.savetxt("Sm.txt", np.array([AlphaInstance.bias_factor_sum]), delimiter="\t", fmt='%.16f')

		os.chdir(root_dir)

		return alpha_array

	def combine_wDot_data(self):
		wDots = np.array([])

		for alpha in self.alpha_array:
			wDots = np.append(wDots, alpha.wDot_data_all_clones)

		return wDots.flatten()

	def calculate_prob_dist(self):
		denominator = 0

		for alpha in self.alpha_array:
			denominator += alpha.num_samples * \
						   alpha.norm_factor * \
						   np.sum(alpha.bias_factor_array)

		return self.wDot_hist/denominator

	def calculate_norm_factors(self):
		for alpha in self.alpha_array:
			alpha.norm_factor = 1 / \
				(np.sum(np.sum(alpha.bias_factor_array)*self.prob_dist))


	def monitor_convergence(self):
		pass

	def normalize_p_dist(self):
		bin_width = myHistogram.wDot_hist_bin_centers[1] - \
					myHistogram.wDot_hist_bin_centers[0]

		integral = np.sum(np.array([i*bin_width for i in self.prob_dist]))

		self.prob_dist /= integral

	def iterate_WHAM(self):
		print([(alpha.bias_param, alpha.norm_factor) for alpha in self.alpha_array])
		for i in range(0,10):
			self.prob_dist = self.calculate_prob_dist()
			self.calculate_norm_factors()
			# print([(alpha.bias_param, alpha.norm_factor) for alpha in self.alpha_array])

		self.normalize_p_dist()

		#plt.plot(self.wDot_hist_bin_edges[:-1], self.prob_dist)
		#plt.show()

myHistogram = Histogram()

myHistogram.iterate_WHAM()

with open ("300_avg.txt", "r") as file:
	wDots_unbiased = np.array([[float(x) for x in line.split()] for line in file])

unbiased_hist , unbiased_bins = np.histogram(wDots_unbiased, bins="auto")

bw = unbiased_bins[1] - unbiased_bins[0]

integral = np.sum(np.array([i*bw for i in unbiased_hist]))

np.savetxt("unbiased_bins.txt", unbiased_bins[:-1], delimiter="\t", fmt='%.8f')
np.savetxt("unbiased_pdist.txt", unbiased_hist/integral, delimiter="\t", fmt='%.8f')


# WHAM_data_array=np.concatenate(myHistogram.wDot_hist_bin_edges[:-1], myHistogram.prob_dist)

np.savetxt("bins.txt", myHistogram.wDot_hist_bin_edges[:-1], delimiter="\t", fmt='%.8f')
np.savetxt("pdist.txt", myHistogram.prob_dist, delimiter="\t", fmt='%.8f')

plt.title("Probability distribution of average $\dot{w}$ values over period tau=30s \nfor biased and unbiased simulations")
plt.plot(myHistogram.wDot_hist_bin_edges[:-1], myHistogram.prob_dist, label="WHAM")
plt.ylabel(r"$\mathcal{P}( \langle \dot{w} \rangle_\tau )$")
plt.xlabel(r"$\langle\dot{w}\rangle$")
plt.plot(unbiased_bins[:-1], unbiased_hist/integral, label="unbiased, k=3")
plt.legend()
plt.show()
