import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

plt.rcParams['text.usetex'] = True

BASE_FREQUENCY = 10e6   # 10 MHz
VREF = 4.096            # V

# capacity in pF
CEXT = 240
CF = np.array([ 12.5, 25, 37.5, 50, 62.5, 75, 87.5, CEXT])

divider_array = np.array([])
T_INT_array = np.array([])
I_FS_array = np.array([])

# all possible divider settings
bits_cnt = np.linspace(1,32,32).reshape(4,8)

for divider in bits_cnt:

    divisions = np.power(2,divider)

    divider_divider = np.array([])
    I_FS_divider = np.array([])
    T_INT_divider = np.array([])
    for division in divisions:

        F_INT = BASE_FREQUENCY / division
        T_INT = 1 / F_INT

        # page 15 of DDC112 datasheet (continuous mode)
        if T_INT > 500e-6 and T_INT < 1000000e-6:
            T_INT_divider = np.append(T_INT_divider, T_INT)
            divider_divider = np.append(divider_divider, division)
            for C in CF:
                I_FS = 0.96 * VREF * C / T_INT

                I_FS_divider = np.append(I_FS_divider, I_FS)

    I_FS_array = np.append(I_FS_array, I_FS_divider)
    T_INT_array = np.append(T_INT_array, T_INT_divider)
    divider_array = np.append(divider_array, divider_divider)

def color_calc(cf):
    return -np.log(cf/np.max(CF))/3

T_INT_array = T_INT_array * 1e6     # using us
I_FS_array = I_FS_array.reshape(int(I_FS_array.size/CF.size), CF.size)

fig, ax = plt.subplots()
graph_array = []

for index, x in np.ndenumerate(T_INT_array):
    graph_array = []
    for index_CF, y in np.ndenumerate(I_FS_array[index]):
        graph, = ax.plot(x, y, marker='.',
                                   label="%.1f pF"%(CF[index_CF]),
                                   c=cm.viridis( color_calc(CF[index_CF])  ) )
        graph_array.append(graph)

ax.legend(handles=graph_array)

ax.set_xscale('log')
ax.set_yscale('log')

ax.set_ylabel(r'full scale input current (\mu A)')
ax.set_xlabel(r'integration time (\mu s)')

plt.show()