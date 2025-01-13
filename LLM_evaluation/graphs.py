import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Define parameters for symbolic version results
mean_accuracy = 91.67  # Mean accuracy (%)
std_accuracy = 0.297  # Standard deviation (%)
num_questions = 1100  # Total number of questions per trial
num_trials = 3  # Number of experimental runs

# Generate simulated accuracy results for each trial
symbolic_accuracies = np.random.normal(loc=mean_accuracy, scale=std_accuracy, size=(num_trials, num_questions))

# Flatten the results across all trials (for histogram and KDE)
all_accuracies = symbolic_accuracies.flatten()

# Create the plot
plt.figure(figsize=(10, 6))

# Histogram with KDE, ensure counts match total 3300
sns.histplot(all_accuracies, bins=30, kde=False, color="lightblue", alpha=0.6, edgecolor=None, stat="count")
sns.kdeplot(all_accuracies, color="darkblue", linewidth=2, bw_adjust=0.8, common_norm=False)

# Add Mean ± Std Dev Range
plt.axvline(mean_accuracy, color="gray", linestyle="--", label=f"Mean: {mean_accuracy:.2f} \u00b1 {std_accuracy:.2f}")
plt.axvline(95.0, color="black", linestyle="--", label="GSM8k Baseline: 95.0%")
plt.axvspan(mean_accuracy - std_accuracy, mean_accuracy + std_accuracy, color="blue", alpha=0.1, label="\u00b1 Std Dev")

# Title and Labels
plt.title("GPT-4o Symbolic Accuracy Distribution on GSM8k Dataset", fontsize=16)
plt.xlabel("Symbolic Accuracy (%)", fontsize=14)
plt.ylabel("Frequency (Number of Questions)", fontsize=14)

# Gridlines
plt.grid(alpha=0.3, linestyle="--")

# Legend
plt.legend(fontsize=12)

# Show the plot
plt.tight_layout()
plt.show()
