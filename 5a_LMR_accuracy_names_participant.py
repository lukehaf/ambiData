# MODEL 2: LOGISTIC MIXED REGRESSION.
import pandas as pd
from pymer4.models import Lmer
from scipy.stats import chi2

# read in accuracy.csv as a dataframe
accuracy = pd.read_csv('3b_accuracy.csv')
accuracy = accuracy[["accuracy", "names_flag", "nth_participant", "question_k"]]
# print(accuracy[['accuracy', 'names_flag', 'nth_participant', 'question_k']].isnull().sum())
# print(accuracy['accuracy'].value_counts())  # Should show both 0 and 1
# print(accuracy['names_flag'].value_counts())
# print(accuracy['nth_participant'].nunique())  # Should be more than 1
# print(accuracy['question_k'].nunique())

# accuracy bool
# names_flag bool
# nth_participant unique integers but not an index
# question_k unique integers

model_full = Lmer("accuracy ~ names_flag + (1 + names_flag | nth_participant)", data=accuracy, family="binomial")
model_reduced = Lmer("accuracy ~ names_flag + (1 | nth_participant)", data=accuracy, family="binomial")
model_full.fit(); model_reduced.fit()

# anova just does F tests within model, not between models.
# lrt_result = model_full.anova(model_reduced)
# print(lrt_result.to_string(index=False))

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
    print("→ The random slope significantly improves fit.")
else:
    print("→ No significant improvement from adding the random slope.")

#######################################################

