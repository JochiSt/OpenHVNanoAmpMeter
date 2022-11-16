import matplotlib.pyplot as plt
from matplotlib import cm, ticker
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
                C = C*1e-12
                I_FS = 0.96 * VREF * C / T_INT
                I_FS_divider = np.append(I_FS_divider, I_FS)

    I_FS_array = np.append(I_FS_array, I_FS_divider)
    T_INT_array = np.append(T_INT_array, T_INT_divider)
    divider_array = np.append(divider_array, divider_divider)

def color_calc(cf):
    return -np.log(cf/np.max(CF))/3

T_INT_array = T_INT_array * 1e6     # using us
I_FS_array = I_FS_array * 1e6     # using uA
I_FS_array = I_FS_array.reshape(int(I_FS_array.size/CF.size), CF.size)

fig, ax = plt.subplots(1, 1, figsize=(6, 6))
graph_array = []

for index, x in np.ndenumerate(T_INT_array):
    graph_array = []
    for index_CF, y in np.ndenumerate(I_FS_array[index]):
        graph, = ax.plot(x, y, marker='.',
                                   label="%5.1f pF"%(CF[index_CF]),
                                   c=cm.viridis( color_calc(CF[index_CF])  ) )
        graph_array.append(graph)

ax.set_xscale('log')
ax.set_yscale('log')

ax.set_ylabel(r'full scale input current (\textmu A)')
ax.set_xlabel(r'integration time (\textmu s)')

###############################################################################

ax2 = ax.twiny()
ax2.set_xscale('log')
new_tick_locations = T_INT_array

def tick_function(X):
    V = divider_array
    return ["%d" % np.log2(z) for z in V]

ax2.set_xlim(ax.get_xlim())
ax2.set_xticks(new_tick_locations)
ax2.set_xticklabels(tick_function(new_tick_locations), rotation=90, ha='center')
ax2.set_xlabel(r"10MHz divider setting $2^n$")

ax2.get_xaxis().set_tick_params(which='minor', size=0)
ax2.get_xaxis().set_tick_params(which='minor', width=0)

###############################################################################

ax3 = ax.twinx()
ax3.set_yscale('log')
new_tick_locations = np.logspace(-4, 0, 5)

def tick_functionY(X):
    V = X/(np.power(2,20)-1)*1e9 # from uA to fA
    label = []
    for z in V:
        if z > 100:
            label.append("%.1f" % z)
        elif z > 10:
            label.append("%.2f" % z)
        elif z > 1:
            label.append("%.3f" % z)
        elif z > 0.1:
            label.append("%.3f" % z)
        elif z > 0.01:
            label.append("%.4f" % z)

    return label

print(new_tick_locations)
print(tick_functionY(new_tick_locations))

ax3.set_ylim(ax.get_ylim())
ax3.set_yticks(new_tick_locations)
ax3.set_yticklabels(tick_functionY(new_tick_locations))#, rotation=90, ha='center')
ax3.set_ylabel(r"20-bit LSB size (fA)")

ax3.get_yaxis().set_tick_params(which='minor', size=0)
ax3.get_yaxis().set_tick_params(which='minor', width=0)

###############################################################################

ax3.legend(handles=graph_array, loc="upper right")

plt.savefig("IFS_vs_Tint_vs_CF.png")
plt.show()
