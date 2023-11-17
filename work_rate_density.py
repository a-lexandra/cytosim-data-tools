import numpy as np
import matplotlib.pyplot
import pandas as pd

from simulation_class import Simulation

class WorkRateDensity(Simulation):
    def __init__(self, column_list=['']):
        self.column_list = column_list

        super().__init__(column_list=self.column_list)

        self.cos_theta_df = pd.DataFrame(columns=['time', 'motor_id', 'fil_id', 'cos_theta', 'fe_x', 'fe_y', 'fm_x', 'fm_y', 'v_m'])

    def calc_cos_theta(self):
        
        for data_obj in self.frame_data_list:
            time = data_obj.time
            
            for index, row in data_obj.temp_dataframe.iterrows():
                motor_id = row['identity']
                
                fil1_id = row['fiber1']
                fil1_dir = np.array([ row['dirFiber1X'], row['dirFiber1Y'] ])

                fil2_id = row['fiber2']
                fil2_dir = np.array([ row['dirFiber2X'], row['dirFiber2Y'] ])

                motor1_pos = np.array([ row['pos1X'], row['pos1Y'] ])
                motor2_pos = np.array([ row['pos2X'], row['pos2Y'] ])

                motor1_dir = motor2_pos - motor1_pos
                motor2_dir = motor1_pos - motor2_pos

                fil1_cos_theta = np.dot(fil1_dir, motor1_dir)/( np.sqrt(motor1_dir[0]**2 + motor1_dir[1]**2) * np.sqrt(fil1_dir[0]**2 + fil1_dir[1]**2) )
                fil2_cos_theta = np.dot(fil2_dir, motor2_dir)/( np.sqrt(motor2_dir[0]**2 + motor2_dir[1]**2) * np.sqrt(fil2_dir[0]**2 + fil2_dir[1]**2) )

                force = row['force']

                motor1_f_x = force * motor1_dir[0]
                motor1_f_y = force * motor1_dir[1]
                
                motor2_f_x = force * motor2_dir[0]
                motor2_f_y = force * motor2_dir[1]

                motor1_vel = self.unloaded_speed * (1 + force*np.dot(motor1_dir, fil1_dir)/self.unbinding_force)
                motor2_vel = self.unloaded_speed * (1 + force*np.dot(motor2_dir, fil2_dir)/self.unbinding_force)
                if self.simulation_df is not None:
                    df1 = self.simulation_df.loc[ (round(self.simulation_df['time'],3) == time) & (self.simulation_df['fil_id'] == fil1_id) ]
                    
                    fil1_f_ext_x = df1['f_dirX'].values
                    fil1_f_ext_y = df1['f_dirY'].values
                  
                    df2 = self.simulation_df.loc[ (round(self.simulation_df['time'],3) == time) & (self.simulation_df['fil_id'] == fil2_id) ]

                    fil2_f_ext_x = df2['f_dirX'].values
                    fil2_f_ext_y = df2['f_dirY'].values
                else:
                    fil1_f_ext_x = 0.0
                    fil1_f_ext_y = 0.0 

                    fil2_f_ext_x = 0.0
                    fil2_f_ext_y = 0.0

                #print(time, motor_id, fil1_id, fil1_cos_theta, fil1_f_ext_x, fil2_f_ext_y, motor1_f_x, motor1_f_y, motor1_vel)

                fil1_df = pd.DataFrame.from_dict({'time': time,
                                        'motor_id': motor_id,
                                        'fil_id': fil1_id,
                                        'cos_theta': fil1_cos_theta,
                                        'fe_x': fil1_f_ext_x,
                                        'fe_y': fil1_f_ext_y,
                                        'fm_x': motor1_f_x,
                                        'fm_y': motor1_f_y,
                                        'v_m': motor1_vel})

                fil2_df = pd.DataFrame.from_dict({'time': time,
                                        'motor_id': motor_id,
                                        'fil_id': fil2_id,
                                        'cos_theta': fil2_cos_theta,
                                        'fe_x': fil2_f_ext_x,
                                        'fe_y': fil2_f_ext_y,
                                        'fm_x': motor2_f_x,
                                        'fm_y': motor2_f_y,
                                        'v_m': motor2_vel})
                

                self.cos_theta_df = pd.concat([self.cos_theta_df, fil1_df, fil2_df], ignore_index=True)

    def calc_work_rate_density_per_fil(self):
        pass


if __name__=="__main__":
    column_list = ['class','identity','fiber1','abscissa1','pos1X','pos1Y','dirFiber1X','dirFiber1Y','fiber2','abscissa2','pos2X','pos2Y','dirFiber2X','dirFiber2Y','force','cos_angle']
    
    myWRD = WorkRateDensity(column_list)

    myWRD.calc_cos_theta()
    breakpoint()

    del myWRD
