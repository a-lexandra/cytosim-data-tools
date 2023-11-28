import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from simulation_class import Simulation

class WorkRateDensity(Simulation):
    def __init__(self, column_list=['']):
        self.column_list = column_list

        super().__init__(column_list=self.column_list)

        self.cos_theta_df = pd.DataFrame(columns=['time', 'motor_id', 
                                                  'fil_id', 'cos_theta', 
                                                  'f_e', 'f_m', 'v_m'])

        self.work_rate_per_fil_df = pd.DataFrame(columns=['time', 'fil_id', 'work_rate'])

        self.work_rate_per_motor_df = pd.DataFrame(columns=['time', 'motor_id', 'work_rate'])

        self.avg_cos_theta_df = pd.DataFrame(columns=['time', 'cos_theta_mean', 'cos_theta_std', 'n_fil'])
        self.fil_pair_angles = pd.DataFrame(columns=['time', 'motor_id', 'fil_pair_angle'])

    def calc_cos_theta(self):
        
        for data_obj in self.frame_data_list:
            time = data_obj.time
            
            for index, row in data_obj.temp_dataframe.iterrows():
                motor_id = int(row['identity'])
                fil_pair_angle = float(row['cos_angle'])

                fil_pair_df = pd.DataFrame([{'time': time, 'motor_id': motor_id, 'fil_pair_angle': fil_pair_angle}])

                self.fil_pair_angles = pd.concat([self.fil_pair_angles, fil_pair_df])
                
                fil1_id = int(row['fiber1'])
                fil1_dir = np.array([ row['dirFiber1X'], row['dirFiber1Y'] ])

                fil2_id = int(row['fiber2'])
                fil2_dir = np.array([ row['dirFiber2X'], row['dirFiber2Y'] ])

                motor1_pos = np.array([ row['pos1X'], row['pos1Y'] ])
                motor2_pos = np.array([ row['pos2X'], row['pos2Y'] ])

                motor1_dir = motor2_pos - motor1_pos
                motor2_dir = motor1_pos - motor2_pos

                mag1 = np.sqrt(motor1_dir[0]**2 + motor1_dir[1]**2) * np.sqrt(fil1_dir[0]**2 + fil1_dir[1]**2) 
                mag2 = np.sqrt(motor2_dir[0]**2 + motor2_dir[1]**2) * np.sqrt(fil2_dir[0]**2 + fil2_dir[1]**2) 

                if (mag1 > 0.0) and (mag2 > 0.0):

                    fil1_cos_theta = np.dot(fil1_dir, motor1_dir)/mag1
                    fil2_cos_theta = np.dot(fil2_dir, motor2_dir)/mag2

                    force = row['force']

                    motor1_vel = self.unloaded_speed * (1 + force*np.dot(motor1_dir, fil1_dir)/self.unbinding_force)
                    motor2_vel = self.unloaded_speed * (1 + force*np.dot(motor2_dir, fil2_dir)/self.unbinding_force)
                    if self.simulation_df is not None:
                        df1 = self.simulation_df.loc[ (round(self.simulation_df['time'],3) == time) & (self.simulation_df['fil_id'] == fil1_id) ]
                        if df1.shape[0]>0:
                            fil1_f_ext_arr = np.array( [ df1['f_dirX'].values, df1['f_dirY'].values ] ).flatten()
                            fil1_f_ext_mag = np.sqrt( fil1_f_ext_arr[0]**2 + fil1_f_ext_arr[1]**2)
                        else: 
                            fil1_f_ext_mag = 0.0

                        df2 = self.simulation_df.loc[ (round(self.simulation_df['time'],3) == time) & (self.simulation_df['fil_id'] == fil2_id) ]

                        if df2.shape[0]>0:
                            fil2_f_ext_arr = np.array( [ df2['f_dirX'].values, df2['f_dirY'].values ] ).flatten()
                            fil2_f_ext_mag = np.sqrt( fil2_f_ext_arr[0]**2 + fil2_f_ext_arr[1]**2)
                        else:
                            fil2_f_ext_mag = 0.0
                       

                    else:
                        fil1_f_ext_mag = 0.0

                        fil2_f_ext_mag = 0.0

                    fil1_df = pd.DataFrame([{'time': float(time),
                                        'motor_id': int(motor_id),
                                        'fil_id': int(fil1_id),
                                        'cos_theta': float(fil1_cos_theta),
                                        'f_e': float(fil1_f_ext_mag),
                                        'f_m': float(force),
                                        'v_m': float(motor1_vel)}])

                    fil2_df = pd.DataFrame([{'time': float(time),
                                        'motor_id': int(motor_id),
                                        'fil_id': int(fil2_id),
                                        'cos_theta': float(fil2_cos_theta),
                                        'f_e': float(fil2_f_ext_mag),
                                        'f_m': float(force),
                                        'v_m': float(motor2_vel)}])
                

                    self.cos_theta_df = pd.concat([self.cos_theta_df, fil1_df, fil2_df], ignore_index=True)
        self.cos_theta_df.to_csv('cos_theta.dat', sep='\t', index=False, mode='w')
        self.fil_pair_angles.to_csv('fil_pair_angles.dat', sep='\t', index=False, mode='w')

    def calc_work_rate_density_per_fil(self):
        for time, time_df in self.cos_theta_df.groupby('time'):
            for fil_id, fil_df in time_df.groupby('fil_id'):
                work_rate_fil = 0.0

                for motor_id, motor_df in fil_df.groupby('motor_id'):
                    f_m = motor_df['f_m'].values[0]
                    f_e = motor_df['f_e'].values[0]
                    cos_theta = motor_df['cos_theta'].values[0]
                    v_m = motor_df['v_m'].values[0]

                    #work_rate_motor = ( f_m - f_e*cos_theta) * v_m * cos_theta
                    work_rate_motor = f_m * v_m * cos_theta

                    work_rate_fil += work_rate_motor

                    motor_df = pd.DataFrame([{'time': time, 'motor_id': motor_id, 'work_rate': work_rate_motor}])
                    self.work_rate_per_motor_df = pd.concat([self.work_rate_per_motor_df, motor_df])
                
                fil_df = pd.DataFrame([{'time': time, 'fil_id': fil_id, 'work_rate': work_rate_fil}])
                self.work_rate_per_fil_df = pd.concat([self.work_rate_per_fil_df, fil_df])

        self.work_rate_per_fil_df.to_csv('work_rate_fil.dat', sep='\t', index=False, mode='w')
        self.work_rate_per_motor_df.to_csv('work_rate_motor.dat', sep='\t', index=False, mode='w')

    def calc_avg_cos_theta(self):
        for time, time_df in self.cos_theta_df.groupby('time'):
            n_fil = len(pd.unique(time_df['fil_id']))
            cos_theta_arr = time_df['cos_theta'].to_numpy(dtype=np.float64)

            #cos_theta_arr = cos_theta_arr[~np.isnan(cos_theta_arr)]
            
            ct_mean = np.mean(cos_theta_arr)
            ct_std  = np.std(cos_theta_arr)

            df = pd.DataFrame({'time': time, 'cos_theta_mean': ct_mean, 'cos_theta_std': ct_std, 'n_fil': n_fil}, index=[0])

            self.avg_cos_theta_df = pd.concat([self.avg_cos_theta_df, df])

        self.avg_cos_theta_df.to_csv('avg_cos_theta.dat', sep='\t', index=False, mode='w')

if __name__=="__main__":
    column_list = ['class','identity','fiber1','abscissa1','pos1X','pos1Y','dirFiber1X','dirFiber1Y','fiber2','abscissa2','pos2X','pos2Y','dirFiber2X','dirFiber2Y','force','cos_angle']
    
    myWRD = WorkRateDensity(column_list)

    myWRD.calc_cos_theta()
    myWRD.calc_work_rate_density_per_fil()
    myWRD.calc_avg_cos_theta()

    del myWRD
