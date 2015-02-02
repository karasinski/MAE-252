import matplotlib
matplotlib.use('TkAgg')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, leastsq


d = [
    [5, 29.552000999450684, 0.15203570251174794],
    [10, 21.974592208862305, 0.20147586240901158],
    [15, 18.020273208618164, 0.15533600598304825],
    [20, 14.75779104232788, 0.14961478466752048],
    [25, 12.339763641357422, 0.18965008933596814],
    [30, 10.786501407623291, 0.17148053192776219],
    [35, 9.604451179504395, 0.41159082031020905],
    [40, 8.611880874633789, 0.41967344420326835],
    [45, 7.596048831939697, 0.12306773746301523],
    [50, 6.966182351112366, 0.10410091844055704],
    [60, 5.936443448066711, 0.13907385631828154],
    [80, 4.295474410057068, 0.1025552369444663],
    [100, 3.3682428002357483, 0.17492293263668218]
    # [150, 1.828736573457718, 0.23423177790521874]
]


d = pd.DataFrame(d)
d.columns = ['distance', 'radius', 'error']

d.plot(kind='scatter', x='distance', y='radius', yerr='error')


def exp_fit(x, a, b, c):
    return a * np.exp(-b * x) + c

popt, pcov = curve_fit(exp_fit, d.distance, d.radius)

fitfunc = lambda p, x: p[0] * np.exp(-p[1] * x) + p[2]
errfunc = lambda p, x, y, err: (y - fitfunc(p, x)) / err

p_init = [32, 0.05, 4]
out = leastsq(errfunc, p_init, args=(d.distance, d.radius, d.error), full_output=1)

x = np.linspace(0, 105, 105)
fit = exp_fit(x, *out[0])
plt.plot(d.distance, d.radius, 'ko', label="Original Data")
plt.plot(x, fit, 'r-', label="Fitted Curve")
plt.xlim(0, 105)
plt.legend()
plt.show()