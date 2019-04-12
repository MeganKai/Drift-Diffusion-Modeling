import pandas as pd
import hddm
import matplotlib.pyplot as plt

def GelmanRubinModel(data):
    models = []
    for i in range(5):
        m = hddm.HDDM(data,p_outlier=0.05)
        m.find_starting_values
        m.sample(5000,burn=100)
        models.append(m)
        m.plot_posterior_predictive(figsize=(14,10))
        plt.show()
    stats = hddm.analyze.gelman_rubin(models)
    print(stats)

# Model incudes outlier prob.
def modelFitDrift(data):
    print("Fitting model...")
    m_stim = hddm.HDDM(data,p_outlier=0.05,depends_on={'z':'stim','v':'stim','a':'stim'},include=('z','sv','st','sz'))
    m_stim.find_starting_values()
    m_stim.sample(10000,burn=1000)
    #m_stim.print_stats()

    v_Pos,v_Neg = m_stim.nodes_db.node[['v(1)','v(2)']]
    hddm.analyze.plot_posterior_nodes([v_Pos,v_Neg])
    plt.xlabel("drift rate")
    plt.ylabel('Posterior Probability')
    plt.title("Posterior of drift-rate group means")
    plt.savefig("hddm_posteriors_v4.pdf")

    #a_Pos,a_Neg = m_stim.nodes_db.node[['a(1)','a(2)']]
    #hddm.analyze.plot_posterior_nodes([a_Pos,a_Neg])
    #plt.xlabel("boundary threshold")
    #plt.ylabel("Posterior of boundary threshold group means")
    #plt.savefig("hddm_posteriors_a2.pdf")

    z_Pos,z_Neg = m_stim.nodes_db.node[['z(1)','z(2)']]
    hddm.analyze.plot_posterior_nodes([z_Pos,z_Neg])
    plt.xlabel("Starting Point")
    plt.ylabel('Posterior Probability')
    plt.title("Posterior of starting-point group means")
    plt.savefig("hddm_posteriors_z.pdf")

    print("Print fitted parameters and model stats")
    m_stim.print_stats()

    # Significance testing on the posteriors
    print("P(vPos > vNeg) = ",(v_Pos.trace() > v_Neg.trace()).mean())
    print("P(zPos > tNeg) = ",(z_Pos.trace()>z_Neg.trace()).mean())
    # Deviance Information Criterion
    print("Stimulus model DIC: ", m_stim.dic)

# Simple model build; using gradient ascent optimization
# Draws posterior samples
def simpleModel(data):
    print("Fitting model...")
    m = hddm.HDDM(data)
    m.find_starting_values()
    m.sample(7000,burn=100)

    print("Fitted parameters and model stats")
    #m.print_stats()
    stats = m.gen_stats()
    print(stats)

    print("Plotting posterior distributions and theoretical RT distributions")
    m.plot_posteriors(['a','t','v','a_std'])
    plt.show()
    print("Lumped model DIC: ", m.dic)

def visualizeRT(data):
    # Load the data
    data = hddm.utils.flip_errors(data)

    # RT Distribuitions of individual subjects
    # Two possible responses, using accuracy encoding
    fig = plt.figure()
    ax = fig.add_subplot(111,xlabel='RT',ylabel='count',title='RT Distributions')
    for i,subj_data in data.groupby('subj_idx'):
        subj_data.rt.hist(bins=20,histtype='step',ax=ax)
    plt.savefig('hddm_RT_Dist.pdf')

def outlierModel(data):
    m_outlier = hddm.HDDM(data,p_outlier=0.05,depends_on={'v':'stim'})
    m_outlier.find_starting_values()
    m_outlier.sample(10000,burn=100)
    m_outlier.plot_posterior_predictive()
    plt.xlabel('RT')
    plt.ylabel("Probability Density")
    plt.savefig("No-Outlier-model-v2.pdf")

def main():

    path = "/home/megan/Desktop/Drift-Diffusion/data"
 
    data = hddm.load_csv("/home/megan/Desktop/Drift-Diffusion/modeling/diffusion-nov-cutoff.csv")
    #visualizeRT(data)
    #simpleModel(data)
    #GelmanRubinModel(data)
    modelFitDrift(data)
    #outlierModel(data)

main()