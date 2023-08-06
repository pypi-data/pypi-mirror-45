from __future__ import print_function

import os

import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate
import emcee
import corner

from platon.fit_info import FitInfo
from platon.combined_retriever import CombinedRetriever
from platon.constants import R_sun, R_jup, M_jup


#data=np.genfromtxt('/Users/nicolewallack/desktop/525K/R37500.txt', delimiter=",", comments='#')
data=np.genfromtxt('/Users/nicolewallack/Desktop/low_res_J0722.csv', delimiter=",", comments='#')

count=0 
w=[]
f=[]
for i in range(len(data[:,0])-1): 
    if data[i,0]-data[i+1, 0]<.0000001: 
        count+=1 
    else: 
        w.append(data[i,0]) 
        f.append(data[i,1]) 
print(count)       

edges=np.array(w)*1e-6
depths=np.array(f)*1e-16
errors=depths/10
plt.plot(edges, depths)
plt.show()
# depths=depths[:-1]
# errors=errors[:-1]
print(edges)
bins= [[w-0.0095e-6, w+0.0095e-6] for w in edges]
# bins=np.array([edges[0:-1], edges[1:]]).T

#250, 290, 0.4, .9, 1e-3, 1700

# bins=bins[0:100]
# depths=depths[0:100]
# errors=errors[0:100]

R_guess = 1. * R_jup

#create a Retriever object
retriever = CombinedRetriever()

#create a FitInfo object and set best guess parameters
# fit_info = retriever.get_default_fit_info(
#     Rs=0.75 * R_sun, Mp=11. * M_jup, Rp=R_guess,
#     logZ=0, CO_ratio=0.53, log_cloudtop_P=np.inf,
#     log_scatt_factor=0, scatt_slope=4, error_multiple=1, T_star=500,
#     T0=420, log_P1=2.4, alpha1=.4, alpha2=2, log_P3=4, T3=1295,
#     profile_type="parametric" #"isothermal" for isothermal fitting
#     )
fit_info = retriever.get_default_fit_info(
    Rs=0.75 * R_sun, Mp=11. * M_jup, Rp=R_guess,
    logZ=0, CO_ratio=0.53, log_cloudtop_P=np.inf,
    log_scatt_factor=0, T_star=500,
    T0=420, log_P1=2.4, alpha1=.4, alpha2=2, log_P3=4, T3=1295,
    profile_type="parametric" #"isothermal" for isothermal fitting
    )
fit_info.add_uniform_fit_param('Mp',9*M_jup, 25*M_jup)

fit_info.add_uniform_fit_param('Rp', 0.9*R_guess, 1.1*R_guess)
fit_info.add_uniform_fit_param("logZ", -1, 3)
fit_info.add_uniform_fit_param('CO_ratio', 0.1, 1.5)
fit_info.add_uniform_fit_param("T0", 200, 600)
fit_info.add_uniform_fit_param("log_P1", 1, 4)
fit_info.add_uniform_fit_param("alpha1", 0.1, 4)
fit_info.add_uniform_fit_param("alpha2", 0.1, 4)
fit_info.add_uniform_fit_param("log_P3", -3, 7)
fit_info.add_uniform_fit_param("T3", 1000, 3000)

# Uncomment below for isothermal fitting

#Use Nested Sampling to do the fitting
result = retriever.run_multinest(None, None, None,
                                 bins, depths, errors,
                                 fit_info, plot_best=True)

plt.savefig("best_fit.png")

np.save("samples.npy", result.samples)
np.save("weights.npy", np.exp(result.logwt))
np.save("logp.npy", result.logp)

fig = corner.corner(result.samples, weights=np.exp(result.logwt),
                    range=[0.99] * result.samples.shape[1],
                    labels=fit_info.fit_param_names)
fig.savefig("multinest_corner.png")

plt.show()
