from data_class import Data

import numpy as np
import pandas as pd

class ClusterAngle(Data):
    def __init__(self,column_list):
        super().__init__(column_list=column_list)

        self.angle_output_df = pd.DataFrame()
    
    def calc_cluster_angle(self):

        angle_list = []

        for cluster_id, df_cluster in self.temp_dataframe.groupby('cluster'):
            dir_x = df_cluster['dirX'].values
            dir_y = df_cluster['dirY'].values

            cluster_size = df_cluster.shape[0]

            theta = np.arctan2(dir_y, dir_x)

            theta_arr = [ th + np.pi for th in theta if th <= 0]

            angle_arr = theta_arr #np.array(angle_list)

            avg_theta_arr = np.array([cluster_id, cluster_size, np.mean(angle_arr), np.std(angle_arr)])

            angle_list.append(avg_theta_arr)
        
        self.angle_array = np.array(angle_list)

        

    def analyze_angle(self):
        self.calc_cluster_angle()
        self.write_output_file()
    
    def write_output_file(self):
        self.angle_array.tofile(self.file_dict["output"]["name"], sep="\t")
        

column_list = [ 'cluster', 'fiber_id', 'posX', 'posY', 'dirX', 'dirY']
myClusterAngle = ClusterAngle(column_list)
myClusterAngle.analyze_angle()
del myClusterAngle