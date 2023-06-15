from data_class import Data
import numpy as np
import pandas as pd
import sys

class BindingTime(Data):
    def __init__(self, column_list, argv=sys.argv[1:]):
        super().__init__(column_list=column_list,argv=argv)

        self.output_df = pd.DataFrame()


if __name__=="__main__":
    column_list = ['identity']
    # Need to implement reading multiple frames from single input file

    # Prototype code
    with open("links.txt", 'r') as input_file:

        temp_file = open("temp.txt", 'w')

        data_list = []
        frame_dict = {}

        for line in input_file:

            if not "% end" in line:
                if not (line.isspace() or ("%" in line and (not column_list[-1] in line))):
                    temp_file.write(line.replace("%",""))
                if "time" in line:
                    frame_dict['time'] = np.float64(line.split()[-1])
                if "frame" in line:
                    frame_dict['frame'] = np.float64(line.split()[-1])
            else:
                # Stop writing to temp file
                temp_file.close()

                # Process frame
                argv = ['-i', 'temp.txt']

                myBindingTime = BindingTime(column_list, argv=argv)

                bound_couples_list = myBindingTime.temp_dataframe.identity.tolist()

                frame_dict['data'] = bound_couples_list

                data_list.append(frame_dict)

                frame_dict = {}
                # Start new temp file for next frame
                temp_file = open("temp.txt", 'w')
        temp_file.close()

        ### Process all frame data - calculate bind time

        # get all unique couple ids


        all_couples = []
        frame_t = []

        for frame in data_list:
            all_couples.append(frame['data'])
            frame_t.append(frame['time'])

        all_couples_flat = [item for sublist in all_couples for item in sublist]
        
        unique_couples = np.unique(np.array(all_couples_flat))

        # Calculate time step between frames

        #dt = sorted(frame_t)[-1]-sorted(frame_t)[-2]

        dt = np.float64(sys.argv[1]) # time between frames

        # find in which frames each of the ids appears
        # make sure frames are in correct order!

        all_bind_times = []

        for cid in unique_couples:
            cid_list = []
            for frame in data_list:            
                if cid in frame['data']:
                    cid_list.append([frame['time'], 1.0])
                else:
                    cid_list.append([frame['time'], 0.0])

            roll_call_str = ''
            for frame in sorted(cid_list):
                if frame[-1] == 1.0:
                    roll_call_str += '1'
                else: roll_call_str += '0'

            # split roll_call at 0s
            bind_seq_list = list(filter(None, roll_call_str.split('0')))

            cid_bind_times = []

            # calculate binding times for each id
            for bind_seq in bind_seq_list:
                bind_len = len(bind_seq)
                bind_time = bind_len*dt

                cid_bind_times.append(bind_time)
                all_bind_times.append(bind_time)

            # calculate average per id
            cid_bind_time_mean = np.array(cid_bind_times).mean()
            cid_bind_time_std = np.array(cid_bind_times).std()

            # print(cid, cid_bind_time_mean, cid_bind_time_std)

        # calculate overall average
        bind_time_mean = np.array(all_bind_times).mean()
        bind_time_std = np.array(all_bind_times).std()
        bind_time_median = np.median(np.array(all_bind_times))

        import matplotlib.pyplot as plt

        counts, bins = np.histogram(np.array(all_bind_times), bins=100)

        csum = np.float64(np.sum(counts))
        counts = np.float64(counts) /csum
        plt.stairs(counts, bins)

        t0 = 0.0
        c0 = 1.0

        t = bins[:-1]

        counts_nonzero = np.array([ c if c>0 else np.nan for c in counts])

        t = np.insert(t, 0, t0)
        counts_nonzero = np.insert(counts_nonzero, 0, c0)

        y = np.array([ np.log(c) if (c != np.nan) else np.nan for c in counts_nonzero])

        idx = np.isfinite(t) & np.isfinite(y)

        K, A_log= np.polyfit(t[idx], y[idx], 1)

        A = np.exp(A_log)

        plt.plot(t, A*np.exp(K*t))

        plt.show()

        print(f"Number of bind times: N = %d" % (len(all_bind_times)))
        print(f"Number of frames: Nf = %d\n" % (len(data_list)))
        print(f"Exponential fit parameters: K = %f, A = %f" % (-1*K, A))
        print(f"Distribution stats: mean = %f, std = %f, med=%f" % (bind_time_mean, bind_time_std, bind_time_median))
        print(f"Calculated mean: 1/K = %f" % (-1/K))
        print(f"Calculated median: ln2/K = %f" % (-np.log(2)/K))


        