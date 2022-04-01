import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from utils import *
import os
import argparse
from  pathlib import Path
from collections import Counter
    
class kMeansClustering:
    def __init__(self):
        #define variable names
        self.dict_data = {   "1":"Sports" ,
                        "2":"Religious",
                        "3":"Theatre",
                        "4":"Shopping",
                        "5":"Picnic",}
        


    def process_kMeans(self,n_clusters, data):

        kmeans = KMeans(n_clusters=int(n_clusters)).fit(data)
        return kmeans

    def read_and_select_data(self, data_path):
        #read data
        df = pd.read_csv(data_path)

        #get variable from user
        print("selectable variables:\n1-Sports\n2-Religious\n3-Theatre\n4-Shopping\n5-Picnic\n")
        x, y = input("Select x and y variable: ").split()
        n_clusters = input("Select cluster number:")

        # filter selected variables from dataset
        data = df[[self.dict_data[x], self.dict_data[y]]]

        return data, x, y, n_clusters

    
    def visualize(self, kmeans, data, labels, x, y, save_path):

        #visualize results
        fig, ax = plt.subplots(figsize=(6.4, 6.4))

        sns.scatterplot( x=data[data.columns[0]], y=data[data.columns[1]], hue=labels)
        plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], 
                    marker="X", c="r", s=80, label="centroids")



        ax.set(
                title=self.dict_data[x] +" - "+ self.dict_data[y],
                facecolor='white'
            )
        # plt.legend()
        # plt.show()

        canvas = FigureCanvas(fig)
        canvas.draw()       
        buf = canvas.buffer_rgba()
        image = np.asarray(buf) 
        plt.imsave(save_path, image)
        plt.close("all")

    def calculate_evalualion_metrics(self, data, kmeans, save_results_path):

        dunn_index = calcDunnIndex(data.values, kmeans.cluster_centers_)

        # wcss = kmeans.inertia_

        wcss = calculateWCSS(data.values, kmeans.cluster_centers_, kmeans.labels_)

        bcss = calculateBCSS(kmeans.cluster_centers_)



        evaluation_metrics= ["dunn_index", "wcss", "bcss"]
        evaluation_values = [dunn_index, wcss, bcss]

        classes = [ "Class_"+str(cluster) for cluster in kmeans.labels_ ]

        records = [ "Record_"+str(cluster) for cluster in range(1, len(data)+1) ]

        
        count_dict = Counter(kmeans.labels_)
        count_dict_ordered = dict(sorted(count_dict.items(), key=lambda x: x[0]))
        c_names = ["Class_"+str(cluster) for cluster in count_dict_ordered.keys()]

        c_counts = [str(cluster)+" Records" for cluster in count_dict_ordered.values()]

        df_1 = pd.DataFrame(zip(records, classes))
        df_2 = pd.DataFrame(zip(c_names, c_counts))

        df_3 = pd.DataFrame(zip(evaluation_metrics, evaluation_values))

        result_df = pd.concat([df_1, df_2, df_3])
        result_df.to_csv(save_results_path)

        

    def process(self, data_path, save_dir):

        data, x, y, n_clusters = self.read_and_select_data(data_path)

        kmeans = self.process_kMeans(n_clusters, data)

        save_img_path = os.path.join(save_dir,"result.png")

        self.visualize(kmeans, data, kmeans.labels_, x, y, save_img_path)

        save_results_path = os.path.join(save_dir,"result.csv")

        self.calculate_evalualion_metrics(data, kmeans, save_results_path)



if __name__ == '__main__':

    # get arguments
    parser = argparse.ArgumentParser(description="K Means Clustering")
    parser.add_argument(
        "--i",
        dest="input",
        help="input data path",
        default="Final-data.txt",
        type=str,
    )
    parser.add_argument("--o", 
                        dest="output", 
                        help="output folder path", 
                        default="outputs", 
                        type=str)

    args = parser.parse_args()

    kMeans = kMeansClustering()
    
    #create output folder 
    Path(args.output).mkdir(parents=True, exist_ok=True)

    kMeans.process(args.input, args.output)








