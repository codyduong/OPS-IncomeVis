#This runs the final viz pass on the csv
import seaborn as sns
import pandas
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")
plt.figure(figsize=(8,11), dpi=300)
plt.gcf().subplots_adjust(left=0.3)
income = pandas.read_csv('income.csv')
ax = sns.violinplot(x="income", y="category", data=income, scale="count", inner="quartile", cut=0, width=1.3)
#ax = sns.stripplot(x="income", y="category", data=income, alpha=.5)
ax.set_xlim(xmin=0)
fig = ax.get_figure()
fig.savefig('income.png')