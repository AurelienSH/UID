from scipy.stats import pearsonr
import pandas as pd
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt
import math
import sys
if len(sys.argv)>1:
     bin = sys.argv[1]
else:
     bin="no"

def sign(x):
    return int(math.copysign(1, x))

df = pd.read_csv("scores_gpt_gum_nofrac.tsv", sep="\t", index_col=0)
data_dict = df.to_dict(orient='index')
scores = defaultdict(list)

for sent in data_dict.keys():
     for scoretype in data_dict[sent].keys():
          scores[scoretype].append(data_dict[sent][scoretype])

bin_scores = defaultdict(list)
for sent in data_dict.keys():
     for scoretype in data_dict[sent].keys():
          if scoretype!='jaeger':
               bin_scores[scoretype].append(sign(data_dict[sent][scoretype]))
correldict = {}

# for scoretype1 in scores.keys():
#      correldict[scoretype1] = {}
#      for scoretype2 in scores.keys():
#           print(f"{scoretype1} and {scoretype2}")
#           corr, p_value = pearsonr(scores[scoretype1], scores[scoretype2])
#           correldict[scoretype1][scoretype2]= corr

# corr_df = pd.DataFrame.from_dict(data=correldict, orient='index')
# corr_df.to_csv("correlation_scores_nonbinary.tsv", sep="\t")

scores_df = pd.DataFrame.from_dict(data=scores)
bin_scores_df = pd.DataFrame.from_dict(data=bin_scores)

# Compute the correlation matrix
if bin == "bin":
     corr_matrix = bin_scores_df.corr()
else:
     corr_matrix = scores_df.corr()

# Plot the heatmap
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')

plt.show()
# print(f"Pearson correlation coefficient: {corr:.2f}")
# print(f"P-value: {p_value:.2f}")




