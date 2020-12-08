from scipy.stats import shapiro, chi2_contingency, ttest_rel, mannwhitneyu, wilcoxon, kruskal, friedmanchisquare
import statistics as s
from scipy import stats

#https://machinelearningmastery.com/statistical-hypothesis-tests-in-python-cheat-sheet/
#https://www.inf.ufsc.br/~andre.zibetti/probabilidade/teste-de-hipoteses.html
#https://statisticsbyjim.com/hypothesis-testing/comparing-hypothesis-tests-data-types/

#Test15: 
#Test0:
#Test18:
#Test17:
#Test12:


#data1 = Hybrid
#data2 = Real

data1 = [
98.89,
94.44,
98.89,
97.78,
95.56,
97.78,
84.81,
98.52,
96.67,
98.89
]

data2 = [
0.37,
0,
1.48,
0.37,
0,
0,
0,
0,
0,
0
]

media_data1 = s.mean(data1)
media_data2 = s.mean(data2)

std_dev_data1 = s.stdev(data1) 
std_dev_data2 = s.stdev(data2)

sem_data1 = stats.sem(data1) 
sem_data2 = stats.sem(data2)

print("\n")
print("Média Data1: ", media_data1)
print("Média Data2: ", media_data2)
print("\n")
print("Desvpad Data1: ", std_dev_data1)
print("Desvpad Data2: ", std_dev_data2)
print("\n")
print("SE Média Data1: ", sem_data1)
print("SE Média Data2: ", sem_data2)
print("\n")
print("Diferença médias: ", abs(media_data1-media_data2))


'''
print("\n")
stat, p = ttest_rel(data1, data2)
print("T-Student Test")
print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.05:
	print('Probably the same distribution')
else:
	print('Probably different distributions')
'''

'''
print("\n")
stat, p = mannwhitneyu(data1, data2)
print("Mann-Whitney U Test")
print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.05:
	print('Probably the same distribution')
else:
	print('Probably different distributions')	
'''
print("\n")
stat, p = wilcoxon(data1, data2)
print("Wilcoxon Signed-Rank Test")
print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.05:
	print('Probably the same distribution')
else:
	print('Probably different distributions')	

'''
print("\n")
stat, p = kruskal(data1, data2)
print("Kruskal-Wallis H Test")
print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.05:
	print('Probably the same distribution')
else:
	print('Probably different distributions')	
'''
'''
print("Gaussian...")
data = data1
stat, p = shapiro(data)
print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.05:
	print('Probably Gaussian')
else:
	print('Probably not Gaussian')


print("\n")
stat, p = ttest_rel(data1, data2)
print("T-Student Test")
print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.05:
	print('Probably the same distribution')
else:
	print('Probably different distributions')
'''

'''
table = [data1, data2]
stat, p, dof, expected = chi2_contingency(table)
print("Chi-Squared Test")
print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.05:
	print('Probably independent')
else:
	print('Probably dependent')
'''




'''
print("\n")
stat, p = mannwhitneyu(data1, data2)
print("Mann-Whitney U Test")
print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.5:
	print('Probably the same distribution')
else:
	print('Probably different distributions')	


print("\n")
stat, p = wilcoxon(data1, data2)
print("Wilcoxon Signed-Rank Test")
print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.05:
	print('Probably the same distribution')
else:
	print('Probably different distributions')	

print("\n")
stat, p = kruskal(data1, data2)
print("Kruskal-Wallis H Test")
print('stat=%.3f, p=%.3f' % (stat, p))
if p > 0.05:
	print('Probably the same distribution')
else:
	print('Probably different distributions')	

'''