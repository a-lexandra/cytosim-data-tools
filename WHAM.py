import numpy as np
import os # for counting the number of directories 

class Histogram:
    def __init__(self):
        #f_a
#         norm_factor_array = self.calculate_norm_factors()
        
        # c_a
#         bias_factor_array = self.calcualte_bias_factors()
        
        # Read number of clones from iteration directory
#         n_clones = self.get_num_clones()
        
        # Read number of frames from clone directory
#         n_frames_per_clone = self.get_num_frames()
        
        # N_a
#         n_samples = n_clones * n_frames_per_clone

        
        print("initializing Histogram class")

    def get_num_clones(self):
        curr_dir = os.getcwd()
        
        
        
        print(curr_dir)
    
        # https://stackoverflow.com/a/29769297
                
        files = folders = 0

        for _, dirnames, filenames in os.walk(curr_dir):
          # ^ this idiom means "we won't be using this value"
            files += len(filenames)
            folders += len(dirnames)

        print("{:,} files, {:,} folders".format(files, folders))

                   
    def get_num_frames(self):
        pass
    
    def calculate_norm_factors(self):
        pass
    
    def calculate_bias_factors(self):
        pass
    
    def calculate_prob_dist(self):
        pass
    
    def monitor_convergence(self):
        pass
    
    
myHistogram = Histogram()

myHistogram.get_num_clones()