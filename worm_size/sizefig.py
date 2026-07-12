import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

from scipy import stats

def size_bar(data, output_dir):
    df = pd.read_csv(data)
    parameters = {'volume': ['Volume', 'µm^3'],
            'length': ['Length', 'µm'],
            'middleWidth': ['Middle Width', 'µm'],
            'meanWidth': ['Mean Width', 'µm'],
            'surfaceArea': ['Surface Area', 'µm^2']}

    df_filtered = df[df['pass'] == True]

    conditions = ['/0h', '/1h', '/4h', '/12h', '/20h', '/40h']
    for key in parameters.keys():
        fig, ax = plt.subplots(figsize=(12, 7))
        means, errors, labels, positions = [[] for i in range(4)]
        data = dict()
        for i in range(len(conditions)):
            y = []
            for j in range(len(df_filtered)):
                if conditions[i] in df_filtered['imageFile'].iloc[j]:
                    y.append(df_filtered[key].iloc[j])
            mean = np.mean(y)
            means.append(mean)
            error = stats.sem(y)
            errors.append(error)
            data[conditions[i]] = y
            labels.append(f"{conditions[i][1:]} \nn = {len(y)} \n{mean:.1f} ± {error:.0f} {parameters[key][1]}")
            positions.append(((i * 4) / 10) + 0.1)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        t = stats.ttest_ind(data['/0h'], data['/40h'], equal_var=True)

        ax.bar(positions, means, yerr=errors, width=0.3, color='#D5A6BD', capsize=5)
        ax.set_ylabel(f'{parameters[key][0]} ({parameters[key][1]})', fontsize=15)
        maximum = max(np.array(means) + np.array(errors))
        ax.set_ylim(0, maximum + maximum * 0.3)
        ax.set_xlim(-0.1, 2.3)
        ax.set_xticks(positions, labels)

        fig.savefig(f'{output_dir}worm_{key}_p={t[1]:.4f}.png', transparent=True)
    return


if __name__ == "__main__":
    import sys
    data = sys.argv[1]
    output_dir = sys.argv[2]
    size_bar(data, output_dir)