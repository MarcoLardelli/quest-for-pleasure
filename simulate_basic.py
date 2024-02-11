
# My quest for pleasure: unraveling the secrets of stellar happiness and sex
# My hobbyist experiments in „computational quantitative psychology“
# (c) Marco Lardelli
# MIT License

import math


STEPS = 10000  # e.g. seconds

PRINT_AT_STEPS = [0,20,100,500,2000,10000]

# compassion fraction
c1 = 0.9
c2 = 0.9

# perception rates
p1 = 0.05
p2 = 0.05

# action influence
i1 = 0.5
i2 = 0.3

# initial values for proper pleasure
P1ProperRaw = 1  # in % of max. inner lust
P2ProperRaw = 0

# ------- end of configuration ------

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

    if i in PRINT_AT_STEPS:
        print(i,"P1",P1,"P1Proper",P1Proper,"P1Social",P1Social)
        print(i,"P2",P2,"P2Proper",P2Proper,"P2Social",P2Social)
