from data_class import Data
import numpy as np 
import pandas as pd
import sys

class DwellTime(Data):
    def __init__(self,  column_list):
        super().__init__(column_list=column_list)

        self.couple_force_df = pd.DataFrame(columns=['identity', 'force'])
        self.output_df = pd.DataFrame()

        self.get_params() # self.unbinding_rate and self.unbinding_force
    
    def get_args(self, argv):
        super().get_args(argv)

        self.parser.add_argument('--unbindingrate', type=float, help='')
        self.parser.add_argument('--unbindingforce', type=float, help='')

    def get_params(self):
        self.unbinding_rate = self.args.unbindingrate
        self.unbinding_force = self.args.unbindingforce

    def calc_avg_dwell_time(self):
        """Calculate the dwell time for the frame averaged
        over all doubly-bound motors
        """
        pass
        # self.unbinding_rate * exp[df['force']/self.unbinding_force]
        # print(self.couple_force_df)
        self.output_df = self.temp_dataframe['force'].apply(lambda x: self.unbinding_rate * np.exp(x/self.unbinding_force))
        self.avg_k_off = self.output_df.mean()
        self.avg_dwell_time = 1/self.avg_k_off
        self.avg_force = self.temp_dataframe['force'].mean()

        print(self.avg_dwell_time, self.avg_force, self.avg_dwell_time*self.avg_force)


if __name__=="__main__":
    column_list = ['identity', 'force']
    myDwellTime = DwellTime(column_list)
    myDwellTime.calc_avg_dwell_time()
    

    