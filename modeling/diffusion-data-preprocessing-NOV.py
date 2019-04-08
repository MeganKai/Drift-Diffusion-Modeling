import hddm
import pandas as pd
import numpy as np
from glob import glob
import sys
import os
def main():
    all_data = pd.DataFrame()
    path = "/home/megan/Desktop/Drift-Diffusion/data/data-nov"
    files = glob(path +'/*.txt')
    all_data = pd.DataFrame()
    for each_file in files:
        b = 0
        k = 0
        t = 0
        with open(each_file,"r") as input:
            index=0
            for line in input:
                if 'B:' in line and index!=0:
                    b=index
                    o=index-b
                if 'K:' in line and index!=0:
                    k=index
                if 'T:' in line and index!=0:
                    t=index
                index+=1
            sum=index
        input.close()
    
        date = each_file[50:60]
        print(date)
        subj_name=each_file[76:79]
        print(subj_name)
        master = pd.read_csv(each_file)
        file = open(each_file,"r")

        #correct_df = pd.DataFrame(columns=['date','subj_idx','stim','rt','response'])
        df2 = pd.read_fwf(file,index=False,nrows=50,skiprows=b+1,names=['ig1','ig2','trialnum','stim','FirstLP','ig3','ig4','ig5','ig6','ig7','CorrectResponses','ig8','Total#Incorrect','Omissions','Lat_First_Incorrect_LP','FirstIncorrectHE'])
        # Add column with response
        #print(df2)

        df2.insert(0,'subj_idx',subj_name)
        df2.insert(1,'date',date)
        #df2["temp"] = (df2["Lat_First_Incorrect_LP"] > 0) | (df2['LeverPress1'] > 0)
        df = df2[df2['Omissions'] != 1]
        #print(df)
        #df = df2[df2["temp"] != False]
        df["response"] = (df['FirstLP'] > df['Lat_First_Incorrect_LP']).astype(int)
        #df["rt"] = df[['FirstLP','Lat_First_Incorrect_LP']].min(axis=1)
        df["rt"] = ""
        df["FirstLP_val"] = (df['FirstLP'] > 0).astype(int)
        df["IncLP_val"] = (df['Lat_First_Incorrect_LP']>0).astype(int)
        for i,row in df.iterrows():
            if row['FirstLP_val'] == 1 and row['IncLP_val'] == 1:
                min = np.minimum(row["FirstLP"],row["Lat_First_Incorrect_LP"])
                df.at[i,'rt'] = min
            elif row["FirstLP_val"] > row['IncLP_val']:
                df.at[i,'rt'] = row["FirstLP"]
            else:
                df.at[i,'rt'] = row["Lat_First_Incorrect_LP"]
        #print(df)

        #correct_df = df.drop(['ig1','ig2','FirstLP','ig3','ig4','ig5','ig6','ig7','CorrectResponses','ig8','Total#Incorrect','Omissions','Lat_First_Incorrect_LP','FirstIncorrectHE'],axis=1)
        correct_df = df[['subj_idx','date','trialnum','stim','response','rt']].copy()
        print(correct_df)
        all_data = pd.concat([all_data,correct_df],0)
    all_data = all_data.sort_values(['subj_idx','date'],ascending=[True,True])
    all_data.to_csv('diffusion-nov-final.csv',index=False)
main()
  

        #print(df))
        #master_df = master[['Trial Type','Lever press lat.']].dropna()
        #master_df=master_df.rename(columns={'Trial Type':'stim','Lever press lat.':'rt'})
        #master_df = master_df[:-1]
        #master_df.insert(0,'date',date,True)
        #master_df.insert(1,'subj_idx',subject_names[0],True)
        #master_df.insert(2,'response',1,True)
        #print(date)
        
        
     #   all_data = pd.concat([all_data,master_df],0)
    #all_data = all_data.sort_values(['subj_idx','date'],ascending=[True,True])
   # all_data.to_csv('diffusion-data-feb.csv',index=False)