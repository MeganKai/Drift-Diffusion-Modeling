import pandas as pd
import hddm
import matplotlib.pyplot as plt

# Simple model build; using gradient ascent optimization
# Draws posterior samples
def simpleModel(data):
    
    m = hddm.HDDM(data,p_outlier=0.05)
    m.find_starting_values()
    m.sample(20,burn=1)


    fig = plt.figure()
    ax = fig.add_subplot(111,xlabel='RT',ylabel='count',title='RT Distributions')
    for i,subj_data in data.groupby('subj_idx'):
        subj_data.rt.hist(bins=20,histtype='step',ax=ax)
    plt.savefig('hddm_demo_fig.pdf')
    models = []

    stats = m.gen_stats()
    stats[stats.index.isin(['a','a_std','a_subj.0','a_subj.1'])]
    m.plot_posteriors(['a','t','v','a_std'])
    plt.savefig("test.pdf")

def main():

    path = "/home/megan/Desktop/Drift-Diffusion/data"
 
    data = hddm.load_csv("/home/megan/Desktop/Drift-Diffusion/data/diffusion-feb.csv")

    simpleModel(data)


main()