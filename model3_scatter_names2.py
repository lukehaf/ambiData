# MODEL 3: LOGISTIC MIXED REGRESSION. SCATTERPLOT.
import pandas as pd
from pymer4.models import Lmer
import numpy as np
import matplotlib.pyplot as plt

# read in accuracy.csv as a dataframe
accuracy = pd.read_csv('3b_accuracy.csv')
df = accuracy = accuracy[["accuracy", "names_flag", "nth_participant", "page1_age", "sleep_freshBefore", "sleep_freshBefore_c", "interf"]]

##########################################################################################


model = Lmer("accuracy ~ names_flag + interf + names_flag:interf + (1 + names_flag + interf + names_flag:interf | nth_participant)", data=accuracy, family="binomial")
model.fit()
# print(model_full.summary())

# 3. Extract fixed‐effect estimates
summary = model.summary() # This gets the full model summary as a DataFrame
print(summary[['Estimate']])  # View the fixed-effect estimates
# Extract fixed effects 
beta0 = summary.loc['(Intercept)', 'Estimate']
beta_names = summary.loc['names_flagTRUE', 'Estimate']
beta_interf = summary.loc['interfTRUE', 'Estimate']
beta_names_interf = summary.loc['names_flagTRUE:interfTRUE', 'Estimate']

# 4. Extract participant‐level random effects (BLUPs)
ranef = model.ranef.copy()
ranef = ranef.reset_index(names="nth_participant") # nth_participant was made into an index, and lost its name

# 5. Participant log odds per condition (4 conditions; 35 rows, one per participant.) (add another 2 columns; the average of each participant's trial 1 and trial 2)
logodds = pd.DataFrame(index=ranef.index) # Start with an empty DataFrame, indexed the same as ranef
logodds["nth_participant"] = ranef["nth_participant"]
logodds["obj1"] = beta0 + ranef['X.Intercept.']
logodds["names1"] = beta0 + beta_names + ranef['X.Intercept.'] + ranef["names_flagTRUE"]
logodds["obj2"] = beta0 + beta_interf + ranef['X.Intercept.'] + ranef["interfTRUE"]
logodds["names2"] = beta0 + beta_names + beta_interf + beta_names_interf + ranef['X.Intercept.'] + ranef["names_flagTRUE"] + ranef["interfTRUE"] + ranef["names_flagTRUE.interfTRUE"]
logodds["names_avg"] = (0.5) * (logodds["names1"] + logodds["names2"])
logodds["objects_avg"] = (0.5) * (logodds["obj1"] + logodds["obj2"])

# 6. Convert log-odds to probabilities
prob = pd.DataFrame(index=logodds.index)
prob["nth_participant"] = logodds["nth_participant"]
prob['obj1'] = 1 / (1 + np.exp(-logodds['obj1']))
prob['names1'] = 1 / (1 + np.exp(-logodds['names1']))
prob['obj2'] = 1 / (1 + np.exp(-logodds['obj2']))
prob['names2'] = 1 / (1 + np.exp(-logodds['names2']))
prob['objects_avg'] = 1 / (1 + np.exp(-logodds['objects_avg']))
prob['names_avg'] = 1 / (1 + np.exp(-logodds['names_avg']))



########################### run regression
from scipy.stats import linregress


# Extract values
x = prob['names2']
y = prob['objects_avg']

# Run regression
slope, intercept, r_value, p_value, std_err = linregress(x, y)

# Print regression stats
print("Regression stats:")
print(f"  Slope:      {slope:.3f}")
print(f"  Intercept:  {intercept:.3f}")
print(f"  R-squared:  {r_value**2:.3f}")
print(f"  p-value:    {p_value:.4f}")
print(f"  Std. error: {std_err:.3f}")

# Generate x values for regression line
x_vals = np.linspace(x.min(), x.max(), 100)
y_vals = intercept + slope * x_vals

# generate x values for fixed-effects line
x_fixed = np.linspace(x.min(), x.max(), 100)

# 7. Scatterplot of predicted probabilities
plt.figure(figsize=(6, 6))
plt.scatter(prob['names2'], prob['objects_avg'], alpha=0.7)
plt.plot(x_vals, y_vals, linestyle='--', color='grey', label='Regression line')
plt.xlim(left=0.28, right=1.02)
plt.ylim(bottom=0.18, top=1.02)
plt.xlabel('Predicted P(correct | names2)', fontsize=20)
plt.ylabel('Predicted P(correct | objects)', fontsize=20)
plt.title('Participant‐specific Predicted Accuracy\nNames2 vs Objects1And2', fontsize=20)
plt.tight_layout()
plt.show()

