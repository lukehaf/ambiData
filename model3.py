# MODEL 3: LOGISTIC MIXED REGRESSION.
import pandas as pd
from pymer4.models import Lmer
from scipy.stats import chi2

# read in accuracy.csv as a dataframe
accuracy = pd.read_csv('3b_accuracy.csv')
df = accuracy = accuracy[["accuracy", "names_flag", "nth_participant", "page1_age", "sleep_freshBefore", "interf"]]


# PRELIMINARY SCREENING. DROP AGE.
# For continuous predictors, e.g. age
# df.groupby(df['accuracy'])[ 'page1_age' ].describe()

# df.groupby(df['accuracy'])[ 'sleep_freshBefore' ].describe()
# df["sleep_freshBefore"].unique()

# for (binary) interference flag
# pd.crosstab(df['interf'], df['accuracy'], normalize='index') # same as a groupby
# df.groupby('interf')["accuracy"].mean()
##########################################################################################

# FIRST TRY ADDING INTERF

model_full = Lmer("accuracy ~ names_flag + interf + names_flag:interf + (1 + names_flag + interf + names_flag:interf | nth_participant)", data=accuracy, family="binomial")
model_reduced = Lmer("accuracy ~ names_flag + (1 + names_flag | nth_participant)", data=accuracy, family="binomial")
model_full.fit(); model_reduced.fit()

print(model_full.summary())
print(model_reduced.summary())

# Extract log‐likelihoods
ll_full = model_full.logLike
ll_red  = model_reduced.logLike


# χ² = 2 * (logL_full − logL_reduced)
chi2_stat = 2 * (ll_full - ll_red)

# Degrees of freedom = # of parameters added in the full model
# Here, full adds one variance term (the random slope variance)
df = 1

# p‐value from the χ² distribution
p_value = chi2.sf(chi2_stat, df)

print(f"χ²({df}) = {chi2_stat:.3f}, p = {p_value:.4f}")
if p_value < 0.05:
    print("→ The fixed effect significantly improves fit.")
else:
    print("→ No significant improvement from adding the fixed effect.")