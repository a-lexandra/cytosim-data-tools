from data_class import Data

if __name__=="__main__":
   column_list = ['cluster', 'nb_fibers', 'fiber_id']

   myData = Data(column_list=column_list)

   print(myData.largest_cluster_id)

   del myData
