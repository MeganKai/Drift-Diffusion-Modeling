import pandas as pd
import numpy as np
from glob import glob
import matplotlib as plt
from matplotlib import pyplot
import sys
import os
# High Tone Stim = 1
# Low Tone Stim = 2print("hi")

def getPercentCorrect(data):
    for subj_num,subject in data.groupby('subj_idx'):
        totalLP = len(subject)
        print(subj_num,totalLP)
        sum = 0
        for index,row in subject.iterrows():
            if row['response'] == 1:
                sum+=1
        perc = (sum  / totalLP)
        print(perc)


def main():
    data = pd.read_csv("/home/megan/Desktop/Drift-Diffusion/modeling/diffusion-feb-final.csv")
    getPercentCorrect(data)

main()