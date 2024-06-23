import numpy as np
import matplotlib.pyplot as plt

def read_and_plot(filename):
    # Load data from .npy file
    data = np.load(filename)
    
    # Check if the shape of the data is as expected
    if data.shape[1] != 7:
        raise ValueError("Expected data with 7 columns, but got data with shape: {}".format(data.shape))
    
    # Set up the matplotlib figure and subplots
    fig, axs = plt.subplots(7, 1, figsize=(10, 20))  # 7 subplots, one for each column
    
    # Plot data from each column in a separate subplot
    for i in range(7):
        axs[i].plot(data[:, i])
        axs[i].set_title(f'Column {i+1}')
        axs[i].set_xlabel('Sample Index')
        axs[i].set_ylabel('Value')
    
    # Adjust layout to prevent overlap
    plt.tight_layout()
    
    # Show the plot
    plt.show()

# Example usage
filename = 'records.npy'  # Replace 'your_data.npy' with the path to your .npy file
read_and_plot(filename)
