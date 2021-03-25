import numpy as np
import os
import argparse

import matplotlib.pyplot as plt



class CloningData:
	# For data from data files for all clones of all iterations
	# Multiple values of alpha
	def __init__(self):
		self.args = self.init_parser()

		self.tau = self.args.tau
		self.beta = self.args.beta

		# keys in the following dictionaries correspond to values of alpha

		self.wDot_avg_dict = self.get_wDot_data()

		self.wDot_avg_hist, self.wDot_avg_bin_centers = self.calculate_wDot_hist()

		self.num_samples_dict = self.calculate_num_samples()

		self.norm_factor_dict = dict.fromkeys(self.wDot_avg_dict.keys(),1)

		self.bias_factor_dict = self.calculate_bias_factors()

	def init_parser(self):
		parser = argparse.ArgumentParser(description='Process data files with avg wDot values over iterations')
		parser.add_argument('--beta', type=float, default=1.0)
		parser.add_argument('--tau', type=float, required=True)

		return parser.parse_args()

	def get_wDot_data(self):
		data = {}

		with os.scandir(os.getcwd()) as entries:
			for entry in entries:
				if entry.is_file() and ".txt" in entry.name:

					alpha = float(entry.name.split('-')[0])

					with open (entry, 'r') as file:
						# https://stackoverflow.com/a/6583635
						wDots_avg_array = np.array([[float(x) for x in line.split()] for line in file])
						# print(wDots_avg_array)

					data[alpha] = wDots_avg_array

		return data

	def calculate_wDot_hist(self):
		wDot_combined = []

		for alpha, wDot_avg_raw_data in self.wDot_avg_dict.items():
			wDot_combined += wDot_avg_raw_data[:,1].tolist()
			# print(wDot_avg_raw_data[:,1].shape)

		wDot_avg_hist, wDot_avg_bin_edges = np.histogram(np.array(wDot_combined).flatten(), bins='auto')
		wDot_avg_bin_centers = wDot_avg_bin_edges[:-1] + np.diff(wDot_avg_bin_edges)/2

		return (wDot_avg_hist, wDot_avg_bin_centers)

	def calculate_num_samples(self):
		num_samples_dict = dict.fromkeys(self.wDot_avg_dict.keys(),[])

		for alpha in num_samples_dict:
			num_samples_dict[alpha] = self.wDot_avg_dict[alpha].shape[0]

		return num_samples_dict

	def calculate_bias_factors(self):
		bias_factor_dict = dict.fromkeys(self.wDot_avg_dict.keys(),[])

		for alpha in bias_factor_dict:
			bias_factor_dict[alpha] = np.exp(-self.beta * alpha * self.tau * self.wDot_avg_bin_centers)

		return bias_factor_dict

	def calculate_prob_dist(self):

		denominator = np.zeros(self.wDot_avg_bin_centers.shape)

		print(denominator.shape)

		for alpha in self.wDot_avg_dict:

			# array over range of wDot
			# The bias factor dictionary entry is an array, the rest are scalar values
			denominator = np.add(denominator,
								 self.num_samples_dict[alpha] * self.norm_factor_dict[alpha] * self.bias_factor_dict[alpha]
								)

		p_dist = self.wDot_avg_hist / denominator

		return p_dist


	def calculate_norm_factors(self):

		for alpha in self.norm_factor_dict:
			self.norm_factor_dict[alpha] = 1 / (np.sum(np.multiply(self.prob_dist, self.bias_factor_dict[alpha])))

	def normalize_p_dist(self):
		bin_width = self.wDot_avg_bin_centers[1] - \
					self.wDot_avg_bin_centers[0]

		integral = np.sum(np.array([i*bin_width for i in self.prob_dist]))

		self.prob_dist /= integral

	def iterate_WHAM(self, n_iters):
		for i in range (0,n_iters):
			# print(self.norm_factor_dict)
			self.prob_dist = self.calculate_prob_dist()
			self.calculate_norm_factors()
			self.normalize_p_dist()

		# plt.plot(self.wDot_avg_bin_centers, self.prob_dist)
		# plt.show()


myCloningData = CloningData()

myCloningData.iterate_WHAM(100)

# with open ("300_avg.txt", "r") as file:
#  	wDots_unbiased = np.array([[float(x) for x in line.split()] for line in file])
#
# unbiased_hist , unbiased_bins = np.histogram(wDots_unbiased, bins="auto")
# unbiased_bin_centers = unbiased_bins[:-1] + np.diff(unbiased_bins)/2
#
# bw = unbiased_bins[1] - unbiased_bins[0]
#
# integral = np.sum(np.array([i*bw for i in unbiased_hist]))

# np.savetxt("unbiased_bins.txt", unbiased_bin_centers, delimiter="\t", fmt='%.8f')
# np.savetxt("unbiased_pdist.txt", unbiased_hist/integral, delimiter="\t", fmt='%.8f')
#
#
# # WHAM_data_array=np.concatenate(myHistogram.wDot_hist_bin_edges[:-1], myHistogram.prob_dist)
#
np.savetxt("bins.txt", myCloningData.wDot_avg_bin_centers, delimiter="\t", fmt='%.8f')
np.savetxt("pdist.txt", myCloningData.prob_dist, delimiter="\t", fmt='%.8f')
#
# plt.title("Probability distribution of average $\dot{w}$ values over period tau=30s \nfor biased and unbiased simulations")
# plt.plot(myCloningData.wDot_avg_bin_centers, myHistogram.prob_dist, label="WHAM")
# plt.ylabel(r"$\mathcal{P}( \langle \dot{w} \rangle_\tau )$")
# plt.xlabel(r"$\langle\dot{w}\rangle$")
# plt.plot(unbiased_bin_centers, unbiased_hist/integral, label="unbiased, k=3")
# plt.legend()
# plt.show()
