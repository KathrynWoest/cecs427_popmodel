import matplotlib.pyplot as plt

def plot(stats_history):
    """
    Plots the number of new infections per day when the simulation completes.

    Parameters:
        stats_history ([]): A list of integers representing new infections at each step.
    """

    plt.figure(figsize=(8, 5))
    plt.plot(range(len(stats_history)), stats_history, marker='o', color='red', linestyle='-')
    plt.title("New Infections Per Day")
    plt.xlabel("Time Step (Day)")
    plt.ylabel("Count")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()