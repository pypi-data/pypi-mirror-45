from larch.io import read_ascii
from larch.math import interp, index_of
import numpy as np


from pymcr.mcr import McrAls
mcrals = McrAls()

d1 = read_ascii('unknown.dat')


i1, i2 = index_of(d1.energy, 11870), index_of(d1.energy, 12030)

dat_energy = d1.energy[i1:i2+1]
dat_array  = d1.munorm[i1:i2+1]

hdat = []
for sname in ('s1.dat', 's2.dat', 's3.dat',
              's4.dat', 's5.dat', 's6.dat'):
    sfile =  read_ascii(sname)
    hdat.append(interp(sfile.energy, sfile.munorm, dat_energy))
#endfor

hdat = np.array(hdat)
npixels, nchan = hdat.shape
print(" H_DAT " , hdat.shape)

conc = np.ones((npixels, 4)) * 0.25

mcrals.fit(hdat, C=conc)

#
#
# # create a parameter group for the fit:
# params = Group(amp1 = param(0.5, min=0, max=1),
#                amp2 = param(0.5, min=0, max=1),
#                amp3 = param(0.0, min=0, max=1),
#                amp4 = param(0.0, min=0, max=1),
#                amp5 = param(0.0, min=0, max=1),
#                amp6 = param(0.0, min=0, max=1))
#
# # define objective function for fit residual
# def sum_standards(pars, data):
#     return (pars.amp1*data.s1 + pars.amp2*data.s2 + pars.amp3*data.s3 +
#             pars.amp4*data.s4 + pars.amp5*data.s5 + pars.amp6*data.s6 )
# #enddef
#
# def resid(pars, data):
#     return (data.mu - sum_standards(pars, data))/data.eps
# #enddef
#
#
# params.amp1.vary = True
# params.amp2.expr = '1 - amp1'
#
# # set uncertainty in data that we'll use to scale the returned residual
# data.eps  = 0.001
#
#
# print(params)
# # # perform fit
# # result = minimize(resid, params, args=(data,))
# # fit = sum_standards(params, data)
# # print fit_report(result)
# #
# #
# # plot(data.energy, data.mu,   label='data', color='blue', marker='+',
# #      markersize=5, show_legend=True, legend_loc='cr', new=True,
# #      xlabel='Energy (eV)', title='Sum S1 and S2 to match data',
# #      xmin=11900, xmax=12000)
# # plot(data.energy, fit,  label='final', color='red')
# #
# # plot(data.energy, 10*(data.mu-fit),  label='resid(x10)', color='black')
# #
# ## end of examples/fitting/doc_example3/fit1.lar
