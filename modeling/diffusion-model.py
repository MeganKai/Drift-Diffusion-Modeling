import pandas as pd
import hddm
import matplotlib.pyplot as plt

def main():
    path = "/home/megan/Desktop/Winter\ 2019/Diffusion-Models/"
 
    data = hddm.load_csv("diffusion-feb.csv")
    print(data.head(10))
    data = hddm.utils.flip_errors(data)

    fig = plt.figure()
    ax = fig.add_subplot(111,xlabel='RT',ylabel='count',title='RT Distributions')
    for i,subj_data in data.groupby('subj_idx'):
        subj_data.rt.hist(bins=20,histtype='step',ax=ax)
    plt.savefig('hddm_demo_fig.pdf')
    models = []
    #for i in range(5):
    m = hddm.HDDM(data,p_outlier=0.05)
    m.find_starting_values()
    m.sample(200,burn=2)

    stats = m.gen_stats()
    stats[stats.index.isin(['a','a_std','a_subj.0','a_subj.1'])]
    m.plot_posteriors(['a','t','v','a_std'])
    #m.savefig('posteriors.pdf')



main()