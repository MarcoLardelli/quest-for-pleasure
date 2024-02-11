# My quest for pleasure: unraveling the secrets of stellar happiness and sex
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

# ------- end of configuration ------

def run_simulation(c1,c2,p1,p2,i1,i2,P1ProperRaw,P2ProperRaw,STEPS):
    P1Social = 0 # Social pleasure always starts with 0 (need perception to build up)
    P2Social = 0
    P1Proper = math.tanh(P1ProperRaw)
    P2Proper = math.tanh(P2ProperRaw)
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

    return P1,P2

        


results = []
for sim_no in range(NO_OF_SIMULATIONS):
    c1 = random.uniform(0,1)
    c2 = random.uniform(0,1)
    p1 = random.uniform(0.001,1)
    p2 = random.uniform(0.001,1)
    i1 = random.uniform(-0.5,0.5)
    i2 = random.uniform(-0.5,0.5)
    P1ProperRaw = random.uniform(0,1)
    P2ProperRaw = random.uniform(0,1)

    P1,P2 = run_simulation(c1,c2,p1,p2,i1,i2,P1ProperRaw,P2ProperRaw,SIMULATION_STEPS)

    results.append([c1,c2,p1,p2,i1,i2,P1ProperRaw,P2ProperRaw,P1,P2])


# make a dataframe from the results for convenience
np_results = np.array(results)
df_results = pd.DataFrame(np_results,
                   columns=['c1', 'c2', 'p1','p2','i1','i2','P1ProperRaw','P2ProperRaw','P1','P2'])

#print summary statistics
print(df_results.mean())

# create some scatterplots
cmap = plt.cm.rainbow
norm = matplotlib.colors.Normalize(df_results['P2'].min(), df_results['P2'].max())


df_results.plot.scatter('P1','P2',s=1,color="#000000")

df_results.plot.scatter('c1','c2',s='P1',color=cmap(norm(df_results['P2'].values)))
df_results.plot.scatter('p1','p2',s='P1',color=cmap(norm(df_results['P2'].values)))
df_results.plot.scatter('i1','i2',s='P1',color=cmap(norm(df_results['P2'].values)))
df_results.plot.scatter('P1ProperRaw','P2ProperRaw',s='P1',color=cmap(norm(df_results['P2'].values)))

"""
# now select the best
selection = df_results[(df_results["P1"] > 20) | (df_results["L2"] > 20)]
norm_selection = matplotlib.colors.Normalize(selection['P2'].min(), selection['P2'].max())
selection.plot.scatter('i1','i2',s='P1',color=cmap(norm_selection(selection['P2'].values)))

#print summary statistics for best
print(selection.mean())
"""

plt.show()

