from simulation_class import Simulation
from data_class import Data

import pandas as pd
import numpy as np

class KeffData(Simulation):
    def __init__(self,argv=[], column_list=[]):
            super().__init__(argv=argv, column_list=column_list)

            # Need to round f_ext data to 3 decimal points (to match reportF data)
            self.f_ext_df = self.simulation_df.round({'time': 3})

            self.motor_df = self.calculate_motor_states()

            # appends columns with k_eff related data to self.motor_df
            self.calculate_k_eff()

            self.write_output()

    def __delete__(self):
        super().__delete__()

    def calculate_motor_states(self):

        motor_df = pd.DataFrame(columns=['time', 'dir', 'force', 'length', 'fil_id', 'couple_id'])

        for frame in self.frame_data_list:
            frame_df = frame.temp_dataframe

            print(frame.time)
            
            for couple_id, df_couple in frame_df.groupby('identity'):
                dir_vec1 = np.array( [ df_couple['pos2X'] - df_couple['pos1X'] , \
                                    df_couple['pos2Y'] - df_couple['pos1Y'] ] ).flatten()

                dir_vec2 = np.array( [ df_couple['pos1X'] - df_couple['pos2X'] , \
                                    df_couple['pos1Y'] - df_couple['pos2Y'] ] ).flatten()

                length1 = np.linalg.norm(dir_vec1)
                length2 = np.linalg.norm(dir_vec2)

                angle1 = np.arctan2(dir_vec1[1], dir_vec1[0])
                angle2 = np.arctan2(dir_vec2[1], dir_vec2[0])

                x1_force = np.cos(angle1)*df_couple['force'].values[0]
                y1_force = np.sin(angle1)*df_couple['force'].values[0]

                force_vec1 = np.array([x1_force, y1_force])

                x2_force = np.cos(angle2)*df_couple['force'].values[0]
                y2_force = np.sin(angle2)*df_couple['force'].values[0]

                force_vec2 = np.array([x2_force, y2_force])

                fiber1_id = df_couple['fiber1'].values[0]
                fiber2_id = df_couple['fiber2'].values[0]

                f_motor1_dict = {'time': frame.time, \
                                 'dir': dir_vec1, \
                                 'force': force_vec1, \
                                 'length': float(length1), \
                                 'fil_id': int(fiber1_id), \
                                 'couple_id': int(couple_id) }
                
                f_motor2_dict = {'time': frame.time, \
                                 'dir': dir_vec2, \
                                 'force': force_vec2, \
                                 'length': float(length2), \
                                 'fil_id': int(fiber2_id), \
                                 'couple_id': int(couple_id) }

                motor_df = pd.concat([ motor_df, \
                                       pd.DataFrame([f_motor1_dict]), \
                                       pd.DataFrame([f_motor2_dict]) ])
        
        motor_df.sort_values(by=['time'], inplace=True)

        return motor_df

    def calculate_k_eff(self):

        self.motor_df = self.motor_df.reindex(columns=self.motor_df.columns.tolist() + ['f_net', 'f_net_mag', 'n', 'k_eff'])

        # need to set to 0 instead of default NaN
        # otherwise will not be able to assign valency (n) as int
        # (NaN cannot be converted to int, all values in col must be same type)
        self.motor_df['n'] = self.motor_df['n'].apply(lambda x: int(0))

        for time, time_df in self.motor_df.groupby('time'):
            print(time)
            for fil_id, fil_df in time_df.groupby('fil_id'):
                valency = fil_df.shape[0]

                f_ext_time_mask = self.f_ext_df['time'] == time
                f_ext_fil_id_mask = self.f_ext_df['fil_id'] == fil_id

                fil_f_ext_df = self.f_ext_df[ f_ext_time_mask & f_ext_fil_id_mask ]

                motor_time_mask = self.motor_df['time'] == time
                motor_fil_id_mask = self.motor_df['fil_id'] == fil_id

                time_fil_df = self.motor_df[motor_time_mask & motor_fil_id_mask]

                for couple_id, couple_df in time_fil_df.groupby('couple_id'):
                    f_ext_vec = np.array([fil_f_ext_df['f_x'].values, fil_f_ext_df['f_y'].values]).flatten()

                    f_net_vec = couple_df['force'].values[0] + f_ext_vec/valency

                    f_net_mag = np.linalg.norm(f_net_vec)

                    if couple_df['length'].values[0] > 0:
                        k_eff = f_net_mag / couple_df['length'].values[0]
                    else:
                        k_eff = float('nan')

                    motor_couple_id_mask = self.motor_df['couple_id'] == couple_id

                    all_masks = motor_time_mask & motor_fil_id_mask & motor_couple_id_mask

                    # need to finish !!!
                    self.motor_df.loc[all_masks, 'f_net'] = \
                        self.motor_df.loc[all_masks,'f_net'].apply(lambda x: f_net_vec)

                    self.motor_df.loc[all_masks, 'n'] = \
                        self.motor_df.loc[all_masks, 'n'].apply(lambda x: int(valency))

                    self.motor_df.loc[all_masks, 'f_net_mag'] = \
                        self.motor_df.loc[all_masks, 'f_net_mag'].apply(lambda x: float(f_net_mag))

                    self.motor_df.loc[all_masks, 'k_eff'] = \
                        self.motor_df.loc[all_masks, 'k_eff'].apply(lambda x: float(k_eff))

    def write_output(self):
        # need to append '#' to header row for compatibility with gnuplot and np.loadtxt()
        notna_mask = self.motor_df['k_eff'].notna()

        last_time = self.motor_df['time'].to_numpy().max()
        time_mask = self.motor_df['time']==last_time
        print(self.args.ofile)
        self.motor_df.loc[ notna_mask & time_mask, 'k_eff' ].to_csv(self.args.ofile, header=True, index=None, sep="\t")

if __name__=="__main__":
    argv = ['--prefixframe', 'report', \
            '--suffixframe', '', \
            '--extframe', 'txt', \
            '--ifilesimulation', 'forces.dat', \
            '--ifilecolnames', 'forces.cols' ]

    column_list = ['identity', \
                   'fiber1', 'pos1X', 'pos1Y', \
                   'fiber2', 'pos2X', 'pos2Y',\
                   'force']

    mySim = KeffData(argv=argv, column_list=column_list)

    del mySim