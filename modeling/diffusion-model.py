import pandas as pd
import hddm
import matplotlib.pyplot as plt

# Simple model build; using gradient ascent optimization
# Draws posterior samples
def GelmanRubinModel(data):
    models = list()
    for i in range(5):
        m = hddm.HDDM(data,p_outlier=0.05)
        m.find_starting_values
        m.sample(5000,burn=20)
        models.append(m)
    hddm.analyze.gelman_rubin(models)

def simpleModel(data):
    print("Fitting model...")
    m = hddm.HDDM(data,p_outlier=0.05,depends_on={'v':'stim'})
    m.find_starting_values()
    m.sample(2000,burn=20)

    print("Print fitted parameters and model stats")
    m.print_stats()

    # RT Distribuitions of individual subjects
    fig = plt.figure()
    ax = fig.add_subplot(111,xlabel='RT',ylabel='count',title='RT Distributions')
    for i,subj_data in data.groupby('subj_idx'):
        subj_data.rt.hist(bins=20,histtype='step',ax=ax)
    plt.savefig('hddm_demo_fig.pdf')
    models = []

    print("Plotting posterior distributions and theoretical RT distributions")
    stats = m.gen_stats()
    stats[stats.index.isin(['a','a_std','a_subj.0','a_subj.1'])]
    m.plot_posteriors(['a','t','v','a_std'])
    plt.savefig("test")

def main():

    path = "/home/megan/Desktop/Drift-Diffusion/data"
 
    data = hddm.load_csv("/home/megan/Desktop/Drift-Diffusion/data/diffusion-feb.csv")

    #simpleModel(data)
    GelmanRubinModel(data)

main()