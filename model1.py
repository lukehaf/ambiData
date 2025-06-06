# MODEL 1: SIMPLE LINEAR REGRESSION.
# BREAK IT DOWN BY PARTICIPANT. SCATTERPLOT OF EACH PARTICIPANT'S % ACCURATE ON NAMES VS OBJECTS.

import pandas as pd
# read in accuracy.csv as a dataframe
accuracy = pd.read_csv('3b_accuracy.csv')

# accuracy by test type (names or objects) and by nth_participant
accuracy_type_nth = (
    accuracy.groupby(['names_or_objects', 'nth_participant'])['accuracy'].sum()
    .unstack('names_or_objects')
    .rename_axis(columns=None)  # Flatten column index. Unstack & Pivot create a Multi-column Index, trying to keep names_or_objects as an overarching name for names and objects
)

########################### run regression
import numpy as np
from scipy.stats import linregress


# Extract values
x = accuracy_type_nth['names']
y = accuracy_type_nth['objects']

# Run regression
slope, intercept, r_value, p_value, std_err = linregress(x, y)

# Print regression stats
print("Regression stats:")
print(f"  Slope:      {slope:.3f}")
print(f"  Intercept:  {intercept:.3f}")
print(f"  R-squared:  {r_value**2:.3f}")
print(f"  p-value:    {p_value:.4f}")
print(f"  Std. error: {std_err:.3f}")

# Generate x values for line
x_vals = np.linspace(x.min(), x.max(), 100)
y_vals = intercept + slope * x_vals


############################# scatterplot + regression line
import matplotlib.pyplot as plt

# Create the scatterplot
plt.figure(figsize=(6,6))
plt.scatter(
    accuracy_type_nth['names'],
    accuracy_type_nth['objects'],
    alpha=0.7
)
plt.plot(x_vals, y_vals, linestyle='--', color='grey', label='Regression line')

# Set axis limits
plt.xlim(0, 10)
plt.ylim(0, 14)

# Labels and title
plt.xlabel('# Correct on Echo Tasks (0–10)', fontsize=20)
plt.ylabel('# Correct on Stories Tasks (0–14)', fontsize=18)
plt.title('# Correct by Participant, Echo vs Stories', fontsize=24)
#plt.title('Scatterplot: Participant Accuracy', fontsize=24)
plt.xlim(right=10.3)
plt.ylim(top=14.3)

# Optional grid
plt.grid(True, linestyle='--', alpha=0.5)

# Show the plot
plt.tight_layout()
plt.show()


