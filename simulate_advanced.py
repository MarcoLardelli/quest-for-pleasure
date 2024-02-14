# My quest for pleasure: unraveling the secrets of heavenly joy
# My hobbyist experiments in „computational quantitative psychology“
# (c) Marco Lardelli
# MIT License

import matplotlib.pyplot as plt

import math
import random
import numpy as np
import pandas as pd
import matplotlib.colors

NO_OF_SIMULATIONS = 10000
SIMULATION_STEPS = 1200  # if 1 step = 1 second -> 20minutes

EPSILON_CONVERGENCE = 0.001

# ------- end of configuration ------


def size_scaler(col):
    #return np.transpose(np.array([(col - col.min()) / (col.max() - col.min())]))  # min-max scaler
    #return np.transpose(np.array([(col - col.min())/10.0]))  # make positive and smaller
    return np.transpose(np.array([np.absolute(col)]))  # absolute value

def run_simulation(c1,c2,p1,p2,i1,i2,P1ProperRaw,P2ProperRaw,STEPS):
    P1Social = 0 # Social pleasure always starts with 0 (need perception to build up)
    P2Social = 0
    P1Proper = math.tanh(P1ProperRaw)
    P2Proper = math.tanh(P2ProperRaw)

    converged = SIMULATION_STEPS*10  # like this wee see those clearly which could not converge in SIMULATION_STEPS steps
    P1_old = STEPS
    for i in range(STEPS):
        # Total pleasure is proper pleasure plus social pleasure felt according to compassion c
        # But we feel only a fraction c a of the partners pleasure
        P1 = P1Proper + c1 * P1Social  
        P2 = P2Proper + c2 * P2Social

        # The pleasure perceived by 1 is slowly approaching the pleasure of 2 (perception needs time)
        # The rate of following is described by the perception rate p
        P1Social +=  p1 * (P2 - P1Social)  # P1Social is always slowly moving towards P2
        P2Social +=  p2 * (P1 - P2Social)  # P2Social is always slowly moving towards P1
        # The proper pleasure changes, depending on pleasure driven actions of partner
        # this depends on the action influence rate i of the partner (can be negative!)
        # if you are in pain, you cannot execute actions -> change is 0 for P < 0
        P1ProperRaw += i2 * max(0,P2)
        P2ProperRaw += i1 * max(0,P1)
        # proper pleasure is limited to a max. of 1 (100%) -> use tanh
        P1Proper = math.tanh(P1ProperRaw)
        P2Proper = math.tanh(P2ProperRaw)
        # a simpler way to limit the values to -1,..,1
        #P1Proper = max(-1,min(1.0,P1ProperRaw))
        #P2Proper = max(-1,min(1.0,P2ProperRaw))
        if abs(P1 - P1_old)<EPSILON_CONVERGENCE:
            converged = i
            break
        else:
            P1_old = P1

    return P1,P2,P1Proper,P2Proper,converged

        

def scatter_plot(data, x, y, circle_size, color, title, selection_descr=""):
    cmap = plt.cm.rainbow
    norm = matplotlib.colors.Normalize(data[color].min(), data[color].max())
    t = title
    has_sel = len(selection_descr)>0
    if has_sel:
        t = selection_descr+", "+title
    else:
        t = title
    data.plot.scatter(x, y, s = circle_size, color = cmap(norm(data[color].values)), title=t)

    if has_sel:
        print(selection_descr)
        print(selection)
        print(selection.mean())


results = []
for sim_no in range(NO_OF_SIMULATIONS):
    c1 = random.uniform(0,1)
    c2 = random.uniform(0,1)
    p1 = random.uniform(0.001,0.1)
    p2 = random.uniform(0.001,0.1)
    i1 = random.uniform(-0.1,0.1)
    i2 = random.uniform(-0.1,0.1)
    P1ProperRaw = random.uniform(0,1)
    P2ProperRaw = random.uniform(0,1)

    P1,P2,P1Proper,P2Proper,converged = run_simulation(c1,c2,p1,p2,i1,i2,P1ProperRaw,P2ProperRaw,SIMULATION_STEPS)

    results.append([c1,c2,p1,p2,i1,i2,P1ProperRaw,P2ProperRaw,P1,P2,P1Proper,P2Proper,converged])



np_results = np.array(results)

# add scaled variants for some columns (for circle size: avoid negative values)
np_results = np.hstack((np_results,size_scaler(np_results[:, 8])))
np_results = np.hstack((np_results,size_scaler(np_results[:, 9])))


# make a dataframe from the results for convenience
df_results = pd.DataFrame(np_results,
                   columns=['c1', 'c2', 'p1','p2','i1','i2',
                            'P1ProperRaw','P2ProperRaw',
                            'P1','P2','P1Proper','P2Proper','Converged',
                            'P1Norm','P2Norm'])

#print summary statistics
print('Mean:')
print(df_results.mean())
print('Min:')
print(df_results.min())
print('Max:')
print(df_results.max())

# export the dataframe as csv file for analysis with other tools
df_results.to_csv('results.csv')

# create some scatterplots
cmap = plt.cm.rainbow
norm1 = matplotlib.colors.Normalize(df_results['P1'].min(), df_results['P1'].max())
norm2 = matplotlib.colors.Normalize(df_results['P2'].min(), df_results['P2'].max())


scatter_plot(df_results,'P1','P2',1,'Converged',"Size = 1, Color = #Steps")

scatter_plot(df_results,'c1','c2','P1Norm','P1',"Size = |P1|, Color = P1")
scatter_plot(df_results,'p1','p2','P1Norm','P1',"Size = |P1|, Color = P1")
scatter_plot(df_results,'i1','i2','P1Norm','P1',"Size = |P1|, Color = P1")
scatter_plot(df_results,'P1ProperRaw','P2ProperRaw','P1Norm','P1',"Size = |P1|, Color = P1")
scatter_plot(df_results,'P1Proper','P2Proper','P1Norm','P1',"Size = |P1|, Color = P1")
scatter_plot(df_results,'P1Proper','P2Proper','P1Norm','i1',"Size = |P1|, Color = i1")

# and some interesting ones other way round (P2 instead of P1)
scatter_plot(df_results,'c1','c2','P2Norm','P2',"Size = |P2|, Color = P2")
scatter_plot(df_results,'i1','i2','P2Norm','P2',"Size = |P2|, Color = P2")
scatter_plot(df_results,'P1Proper','P2Proper','P2Norm','i2',"Size = |P2|, Color = i2")


# now select the BEST interactions
quantile = df_results['P1'].quantile(0.95)
selection = df_results[df_results["P1"] > quantile]
norm_selection = matplotlib.colors.Normalize(selection['P1'].min(), selection['P1'].max())
scatter_plot(selection,'i1','i2','P1Norm','P1',"Size = |P1|, Color = P1", "BEST P1")


# now select the WORST interactions
quantile = df_results['P1'].quantile(0.01)
selection = df_results[df_results["P1"] < quantile]
scatter_plot(selection,'i1','i2','P1Norm','P1',"Size = |P1|, Color = P1", "WORST P1")


# now select asymmetric interactions (P1 doing poorly, P2 doing well)
quantile_min1 = df_results['P1'].quantile(0.3)
quantile_max2 = df_results['P2'].quantile(0.7)
selection = df_results[(df_results["P1"] < quantile_min1) & (df_results["P2"] > quantile_max2)]
scatter_plot(selection,'i1','i2','P1Norm','P1',"Size = |P1|, Color = P1", "ASYM P1<<P2")


# now select small P values
quantile_max1 = df_results['P1'].quantile(0.99)
quantile_max2 = df_results['P2'].quantile(0.99)
quantile_min1 = df_results['P1'].quantile(0.01)
quantile_min2 = df_results['P2'].quantile(0.01)
selection = df_results[(df_results["P1"] < quantile_max1) & (df_results["P1"] > quantile_min1) & (df_results["P2"] < quantile_max2) & (df_results["P2"] > quantile_min2)]
scatter_plot(selection,'P1','P2',1,'c1',"Color = c1", "Small P1,P2")



plt.show()

