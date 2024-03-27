import pandas as pd
import numpy as np

#df = pd.read_excel("GPT/summary_Final.xlsx")
df = pd.read_excel("GPT/summary.xlsx")



index = ['setting', 'focus', 'application', 'context', 'objectives', 'methods', 'results', 'rateofSuccess']


for i in range(len(index)):

    
    fl = df[index[i]].dropna(ignore_index=True)

    countAll = fl.value_counts()
    #count.to_csv("Summary/all_"+str(index[i])+'_final.csv')
    countAll.to_excel("Summary/all_"+str(index[i])+'_final.xlsx')

    
    
    #input()
    splitData = []
    for j in range(len(fl)):               
        temp = fl[j]
        temp = temp.split(', ')    

        for k in range(len(temp)):
            splitData.append(temp[k])    

    se = pd.Series(splitData)

    countSplit = se.value_counts()
    #count.to_csv("Summary/summ_"+str(index[i])+'_final.csv')
    countSplit.to_excel("Summary/split_"+str(index[i])+'_final.xlsx')
    #print(count)

print("done")