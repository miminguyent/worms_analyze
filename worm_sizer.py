import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import math
from scipy import stats

def plot_data(data, output_dir):
    df = pd.read_csv(data)
    colors = ['#B25D91FF', '#CB87B4FF', '#EFC7E6FF', '#1BB6AFFF', '#088BBEFF', '#172869FF']

    df_filtered = df[df['pass'] == True]

    conditions = ['/0h', '/1h', '/4h', '/12h', '/20h', '/40h']
    fig, ax = plt.subplots(figsize=(12, 7))
    data = ()
    labels, positions = [[] for i in range(2)]
    for i in range(len(conditions)):
        lengths = []
        for j in range(len(df_filtered)):
            if conditions[i] in df_filtered['imageFile'].iloc[j]:
                lengths.append(df_filtered['length'].iloc[j])
        data = data + (lengths,)
        yscale = np.linspace((i * 4) / 10, ((i * 4) / 10) + 0.2, len(lengths))
        ax.scatter(x=np.array(yscale), y=np.array(lengths), s=30, color=colors[i], alpha=0.8)
        labels.append(conditions[i][1:] + "\nn=" + str(len(lengths)))
        positions.append(((i * 4) / 10) + 0.1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.boxplot(data, widths=0.3, sym='', whis=[5, 95], vert=True, positions=positions, manage_ticks=True)
    ax.set_ylabel('Length (µm)', fontsize=15)
    ax.set_xlim(-0.1, 2.3)
    ax.set_ylim(0, 2000)
    ax.set_xticks(positions, labels)

    fig.savefig(output_dir + 'worm_length.png')
    return


if __name__ == "__main__":
    import sys
    data = sys.argv[1]
    output_dir = sys.argv[2]
    plot_data(data, output_dir)