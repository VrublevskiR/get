from matplotlib import pyplot
import numpy
from textwrap import wrap
import matplotlib.ticker as ticker



file = open('data.txt', 'r')
file = open('settings.txt', 'r')

with open('settings.txt') as file:
    settings=[float(i) for i in file.read().split('\n')]


data=numpy.loadtxt('data.txt', dtype=int) * settings[1]
data_time=numpy.array([i*settings[0] for i in range(data.size)])

fig, ax=pyplot.subplots(figsize=(16, 10), dpi=500)

ax.axis([data.min(), data_time.max()+1, data.min(), data.max()+0.1])


ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.5))
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))

ax.set_title("\n".join(wrap('Процесс заряда и разряда конденсатора в RC цепи', 50)), loc = 'center',fontsize=18)

ax.grid(which='major', color = 'k')
ax.minorticks_on()
ax.grid(which='minor', color = 'gray', linestyle = ':')

ax.set_ylabel("Напряжение U, В", fontsize=17)
ax.set_xlabel("Время T, с",fontsize=17)

ax.plot(data_time, data, color='black', linewidth=2, label = '$U_C(t)$', marker='o', markerfacecolor='red', linestyle='-',
    markersize=7, markevery = 10)

textstr = '\n'.join((
    r'              Время зарядки T = 5.21 c',
    r'              Время разрядки T = 6.79 c' ))


ax.text(0.545, 0.972, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top')


ax.legend(fontsize = 23)


fig.savefig('graph.png')
fig.savefig('graph.svg')
