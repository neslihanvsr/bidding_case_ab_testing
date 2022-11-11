# Comparison of Bidding Methods using A/B Test

# AB Testing
#
# summary
#
# 1. Set up Hypothesis
# 2. Assumption Check
# - 1. Normality Assumption
# - 2. Variance Homogeneity
# 3. Implementation of the Hypothesis
# - 1. If assumptions are provided, t-test from two independent samples (parametric test)
# - 2. Mannwhitneyu test if absence of assumptions (non-parametric test)
# 4. Interpret results based on p-value


# Case: maximum bidding vs average bidding
#
# As an alternative to the bidding type called "maximum bidding", a new bidding type, "average bidding", is proposed.
# An A/B test will be conducted to see if averagebidding converts more than maximumbidding.
# Purchase metric has been focused for statistical testing.

# Impression: Number of ad views
# Click: Number of clicks on the displayed ad
# Purchase: The number of products purchased after the ads clicked
# Earning: Earnings after purchased products

import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import shapiro, levene, ttest_ind

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

dfA = pd.read_excel(r'C:\ab_testing.xlsx', sheet_name='Control Group')
dfB = pd.read_excel(r'C:\ab_testing.xlsx', sheet_name='Test Group')

dfA.describe().T
dfB.describe().T

dfA["Group"] = "Control"
dfB["Group"] = "Test"

df = pd.concat([dfA, dfB], axis=0)
df.head()


#1. Set up Hypothesis
# H0 : M1 = M2 (There is no statistically significant difference between the control group and test group purchasing averages.)
# H1 : M1!= M2 (There is a statistically significant difference between the purchasing averages of the control group and test group.)

df.groupby("Group").agg({"Purchase": "mean"})

#2. Assumptions Check

## Normality Assumption:
# H0: Normal distribution assumption is provided.
# H1: The assumption of normal distribution is not provided.

test_stat, pvalue = shapiro(df.loc[df['Group'] == 'Control', 'Purchase'])
print('Test Stat = %.4f p-value = %.4f' % (test_stat, pvalue))

# # p-value=0.5891
# # HO cannot be rejected. The values of the Control group provide the assumption of normal distribution.

test_stat, pvalue = shapiro(df.loc[df['Group'] == 'Test', 'Purchase'])
print('Test Stat = %.4f p-value = %.4f' % (test_stat, pvalue))

# # p-value=0.1541
# # HO cannot be rejected. The values of the Control group provide the assumption of normal distribution.

## Variance Homogeneity:
# H0: Variances are homogeneous.
# H1: Variances are not homogeneous.

test_stat, pvalue = levene(df.loc[df['Group'] == 'Control', 'Purchase'],
                           df.loc[df['Group'] == 'Test', 'Purchase'])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value=0.1083
# HO cannot be rejected. The values of the Control and Test group provide the assumption of variance homogeneity.
# Variances are homogeneous.

# 3. Implementation of the Hypothesis
# Parametric test assumptions met: independent two samples t-test (Parametric test assumptions):
test_stat, pvalue = ttest_ind(df.loc[df['Group'] == 'Control', 'Purchase'],
                              df.loc[df['Group'] == 'Test', 'Purchase'],
                              equal_var=True)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value=0.3493
# HO cannot be rejected. # H0 : M1 = M2 (There is no statistically significant difference between the control group and test group purchasing averages.)

# 4. Interpret results based on p-value

# Considering the p_value obtained as a result of the test,
#  it can be said that there is no statistically significant difference between the Control group and Test group purchasing averages.
# There is no meaningful difference between the maximum bidding and average bidding methods for the purchase variable.


