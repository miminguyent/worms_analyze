import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import os

from scipy import stats

def velocity_box(input_dir, output_dir):

    conditions = ['control', '1h', '4h', '12h', '20h', '40h']
    tracks = os.listdir(input_dir)
    colors = ['#1BB6AFFF', '#B25D91FF', '#CB87B4FF', '#EFC7E6FF', '#088BBEFF', '#172869FF']

    fig, ax = plt.subplots(figsize=(12, 7))
    for i in range(len(conditions)):
        mean_tracks = []
        for file in tracks:
            df = pd.read_csv(f"{input_dir}/{file}")
            df = df.dropna(how='any')
            if conditions[i] in file:
                mean_tracks.append(np.array(df['TRACK_MEAN_SPEED'][2:,]).astype(float) * 18)

        mean_tracks = np.concatenate(np.array(mean_tracks))
        mean_tracks = mean_tracks[(mean_tracks > 0.04) & (mean_tracks < 0.3)]

        if conditions[i] == 'control':
            mean_control = mean_tracks
            sns.kdeplot(mean_tracks, color=colors[i], label=f"{conditions[i]} (tracks={len(mean_tracks)})", ax=ax, linewidth=4)
        elif conditions[i] == '40h':
            mean_40h = mean_tracks
            sns.kdeplot(mean_tracks, color=colors[i], label=f"{conditions[i]} (tracks={len(mean_tracks)})", ax=ax, linewidth=4)
        else:
            sns.kdeplot(mean_tracks, color = colors[i], label=f"{conditions[i]} (tracks={len(mean_tracks)})", ax=ax)

    ks_test = stats.ks_2samp(mean_control, mean_40h)
    ax.legend()
    ax.set_xlabel('Mean Velocity (mm/second)')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    fig.savefig(f'{output_dir}velocity_p={ks_test[1]:.10f}.png', transparent=True)



    return


if __name__ == "__main__":
    import sys
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    velocity_box(input_dir, output_dir)