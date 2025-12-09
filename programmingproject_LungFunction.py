import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import animation
DATAFILE = r"C:\Users\gmorr\OneDrive\Desktop\Programming_Project_Data_REALSheet1.csv"      #/Users/uzma/Desktop/Programming_Project_Data_REAL(Sheet1).csv
def load_data(path):
    df = pd.read_csv(path)
    df = df[['PatientID', 'Time', 'Volume', 'Flow']]
    df = df.dropna(subset=['PatientID', 'Time', 'Volume', 'Flow'])
    return(df)

def compute_lung_metrics(df):
   metrics_list = []
   # Loop over each patient
   for patient in df['PatientID'].unique():
        patient_data = df[df['PatientID'] == patient]

        # FEV1: max volume at or before 1 second
        fev1 = patient_data[patient_data['Time'] <= 1]['Volume'].max()

        # FVC: total volume exhaled
        fvc = patient_data['Volume'].max()

        # FEV1/FVC ratio
        ratio = fev1 / fvc if fvc != 0 else np.nan

        # PEF: peak expiratory flow
        pef = patient_data['Flow'].max()

        # Append results
        metrics_list.append([patient, fev1, fvc, ratio, pef])

    # Convert to DataFrame
   metrics_df = pd.DataFrame(
        metrics_list,
        columns=['PatientID', 'FEV1', 'FVC', 'FEV1_FVC', 'PEF']
    )
   return metrics_df  # <--- MUST return!

def create_plots(metrics, df):
# Volume-Time curve
    plt.figure(figsize=(7,4))
    sns.lineplot(data=df, x="Time", y="Volume", hue="PatientID", legend=False)
    plt.title("Volume-Time Curve")
    plt.xlabel("Time (s)")
    plt.ylabel("Volume (L)")
    plt.savefig(r"volume_time_curve.png")
    plt.show()
    plt.close()

 # Flow-Volume curve
    plt.figure(figsize=(7,4))
    sns.lineplot(data=df, x="Volume", y="Flow", hue="PatientID", legend=False)
    plt.title("Flow-Volume Curve")
    plt.xlabel("Volume (L)")
    plt.ylabel("Flow (L/s)")
    plt.savefig(r"flow_volume_curve.png")
    plt.show()
    plt.close()

    # Histogram of FEV1
    plt.figure(figsize=(7,5))
    sns.histplot(data=metrics, x="FEV1", bins=10, kde=True)
    plt.title("Histogram of FEV1")
    plt.xlabel("FEV1 (L)")
    plt.savefig(r"hist_fev1.png")
    plt.show()
    plt.close()

    #boxplot of FEV1/FVC
    plt.figure(figsize=(6,4))
    sns.boxplot(data=metrics, y="FEV1_FVC")
    plt.title("Boxplot of FEV1/FVC Ratio")
    plt.ylabel("FEV1/FVC")
    plt.savefig(r"box_fev1_fvc.png")
    plt.show()
    plt.close()

    # make animation (function code is missing here)

def animate_breathing(df, patient_id): # define function to animate breathing data for one patient
    patient_data= df[df["PatientID"] == patient_id] # filter the dataframe to only keep rows for the chosen patient
    t = patient_data["Time"].values # extract time values as NumPy array
    v = patient_data["Volume"].values # extract volume values as NumPy array

    fig, ax = plt.subplots(figsize=(6,4)) # create figure and axis for the plot
    ax.set_xlim(min(t), max(t)) # set x-axis limits based on minimum and maximum time values
    ax.set_ylim(min(v), max(v)) # set y-axis limits based on minimum and maximum volume values
    ax.set_xlabel("Time (s)") # label the x-axis
    ax.set_ylabel("volume (L)") # label the y-axis
    ax.set_title(f"Breathing Curve Over time - {patient_id}") # set title showing patient ID

    line, = ax.plot([], [], lw=2) # create an empty line object to be updated during animaton
    print(line) # print the line onject for debugging

    def animate(i): # define animation fucntion that updates line data for each frame
        x = t[:i] # use time values from start to the i-th point
        y = v[:i] # use volume values from start to the i-th point
        line.set_data(x,y) # update the line with the new data
        return line, # return the updated line so FuncAnimation knows what to redraw

    anim = animation.FuncAnimation( #create the animation object
        fig, # figure to animate
        animate, # animation function that updates the plot each frame
        frames=len(t),  # number of frames equal to number of time points
        interval = 200 # Delay between frames in milliseconds (controls speed)
        ) 
    anim.save(r"/Users/peterkolovos/Desktop/Programming_Project_Data_REALSheet1.gif", writer="pillow") # save the animation
    plt.show() # display the animation
    plt.close() # close the plot

def export_summary(metrics):
    metrics.to_csv("Lung_summary.csv", index=False)

if __name__ == "__main__":
    df = load_data(DATAFILE)  
    print(df)          
    metrics = compute_lung_metrics(df)
    print(metrics)

    create_plots(metrics, df)
    export_summary(metrics)
    animate_breathing(df, "P01")
