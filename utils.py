import matplotlib.pyplot as plt
import numpy as np

def plot_series(series, trend = True, seasonality = True, X_label = "Date", Y_label = "Profit", title = "Simulated DGP of Company Profits", save = False):
    plt.figure(figsize=(10, 6))
    plt.plot(series["date"], series["value"], label="Total Profit", marker = 'o')
    if trend:
        plt.plot(series["date"], series["trend"], label="Trend", linestyle='--')
    if seasonality:
        plt.plot(series["date"], series["seasonality"], label="Seasonality", linestyle='-.')
    plt.xlabel(X_label)
    plt.ylabel(Y_label)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if save:
        plt.savefig(f'figures/{title}_{int(np.random.uniform()*10000)}')
    plt.show()