import matplotlib
import matplotlib.pylab as plt

from SecretColors.palette import Palette, ColorMap

p = Palette("clarity")
c = ColorMap(matplotlib, p)

x = p.red(no_of_colors=5)

for i, v in enumerate(x):
    plt.bar(i, 1, color=v)

plt.show()
