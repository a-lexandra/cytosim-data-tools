

import sys
sys.path.insert(1, '/home/yuqingqiu/erik-emus/EMUS/src')
import numpy as np

from emus import usutils as uu
from emus import emus, avar
import matplotlib.pyplot as plt

T = 1 # Temperature in Kelvin
k_B = 1 # Boltzmann factor in kcal/mol
kT = k_B * T
meta_file = 'k3_cv_meta_tau100_alpha_tau.txt' # Path to Meta File
dim = 1  # 1 Dimensional CV space.
nbins = 30 # Number of Histogram Bins.
period= None
neighbors= None
# Load data?
psis, cv_trajs, neighbors = uu.data_from_meta(
    meta_file, dim, T=T, k_B=k_B, period=None)

# Calculate the partition function for each window
z, F = emus.calculate_zs(psis, neighbors=neighbors)

# Calculate error in each z value from the first iteration.
zerr, zcontribs, ztaus = avar.calc_partition_functions(
    psis, z, F, iat_method='acor')

# Calculate the PMF from EMUS
domain = ((0.1, 3))           # Range of dihedral angle values
pmf, edges = emus.calculate_pmf(
    cv_trajs, psis, domain, z, nbins=nbins, kT=kT, use_iter=False)   # Calculate the pmf


# Calculate z using the MBAR iteration.
z_iter_1, F_iter_1 = emus.calculate_zs(psis, n_iter=1)
z_iter_2, F_iter_2 = emus.calculate_zs(psis, n_iter=2)
z_iter_5, F_iter_5 = emus.calculate_zs(psis, n_iter=5)
z_iter_1k, F_iter_1k = emus.calculate_zs(psis, n_iter=1000)

# Calculate new PMF
iterpmf, edges = emus.calculate_pmf(
    cv_trajs, psis, domain, nbins=nbins, z=z_iter_1k, kT=kT)
# Get the asymptotic error of each histogram bin.
pmf_av_mns, pmf_avars = avar.calc_pmf(
    cv_trajs, psis, domain, z, F, nbins=nbins, kT=kT, iat_method=np.average(ztaus, axis=0))

### Data Output Section ###

# Plot the EMUS, Iterative EMUS pmfs.
pmf_centers = (edges[0][1:]+edges[0][:-1])/2.
plt.figure()
plt.errorbar(pmf_centers, pmf_av_mns, yerr=np.sqrt(
    pmf_avars), label='EMUS PMF w. AVAR')
plt.plot(pmf_centers, iterpmf, label='Iter EMUS PMF')
plt.xlabel('wdot')
plt.ylabel('Unitless FE')
plt.legend()
plt.title('EMUS and Iterative EMUS potentials of Mean Force')
plt.show()

#print("%f,%f,%f" % (pmf_centers, pmf_av_mns,np.sqrt(pmf_avars)))
# Plot the relative normalization constants as fxn of max iteration.
plt.errorbar(np.arange(len(z)), -np.log(z),
             yerr=np.sqrt(zerr)/z, label="Iteration 0")
plt.plot(-np.log(z_iter_1), label="Iteration 1")
plt.plot(-np.log(z_iter_1k), label="Iteration 1k", linestyle='--')
plt.xlabel('Window Index')
plt.ylabel('Unitless Free Energy')
plt.title('Window Free Energies and Iter No.')
plt.legend(loc='upper left')
plt.show()

# Print the C7 ax basin probability
#print("EMUS Probability of C7ax basin is %f +/- %f" % (probC7ax, probC7ax_std))
#print("Iterative EMUS Probability of C7ax basin is %f" % (prob_C7ax_iter))

print("Asymptotic coefficient of variation for each partition function:")
print(np.sqrt(zerr)/z)


###

x_tau100 = pmf_centers
y_tau100  = pmf_av_mns/100
err_tau100 =1/100*np.sqrt(pmf_avars)

###

y_tau100_iter  = iterpmf/100

###

#In this test, use python/cpython-3.8.5 to build the emus
# use meta_data with k = alpha
# tau=100 in exp(tau*wdot*alpha) is included in U
#window center are 0 to N
#do not change any neighbours parameter
# Define Simulation Parameters
T = 1                             # Temperature in Kelvin
k_B = 1                  # Boltzmann factor in kcal/mol
kT = k_B * T
meta_file = 'k3_cv_meta_tau30_alpha_tau.txt'         # Path to Meta File
dim = 1                             # 1 Dimensional CV space.
nbins = 45 # Number of Histogram Bins.
period= None
neighbors= None
# Load data?
psis, cv_trajs, neighbors = uu.data_from_meta(
    meta_file, dim, T=T, k_B=k_B, period=None)

# Calculate the partition function for each window
z, F = emus.calculate_zs(psis, neighbors=neighbors)

# Calculate error in each z value from the first iteration.
zerr, zcontribs, ztaus = avar.calc_partition_functions(
    psis, z, F, iat_method='acor')

# Calculate the PMF from EMUS
domain = ((0, 4.5))           # Range of dihedral angle values
pmf, edges = emus.calculate_pmf(
    cv_trajs, psis, domain, z, nbins=nbins, kT=kT, use_iter=False)   # Calculate the pmf


# Calculate z using the MBAR iteration.
z_iter_1, F_iter_1 = emus.calculate_zs(psis, n_iter=1)
z_iter_2, F_iter_2 = emus.calculate_zs(psis, n_iter=2)
z_iter_5, F_iter_5 = emus.calculate_zs(psis, n_iter=5)
z_iter_1k, F_iter_1k = emus.calculate_zs(psis, n_iter=1000)

# Calculate new PMF
iterpmf, edges = emus.calculate_pmf(
    cv_trajs, psis, domain, nbins=nbins, z=z_iter_1k, kT=kT)
# Get the asymptotic error of each histogram bin.
pmf_av_mns, pmf_avars = avar.calc_pmf(
    cv_trajs, psis, domain, z, F, nbins=nbins, kT=kT, iat_method=np.average(ztaus, axis=0))

### Data Output Section ###

# Plot the EMUS, Iterative EMUS pmfs.
pmf_centers = (edges[0][1:]+edges[0][:-1])/2.
plt.figure()
plt.errorbar(pmf_centers, pmf_av_mns, yerr=np.sqrt(
    pmf_avars), label='EMUS PMF w. AVAR')
plt.plot(pmf_centers, iterpmf, label='Iter EMUS PMF')
plt.xlabel('wdot')
plt.ylabel('Unitless FE')
plt.legend()
plt.title('EMUS and Iterative EMUS potentials of Mean Force')
plt.show()

#print("%f,%f,%f" % (pmf_centers, pmf_av_mns,np.sqrt(pmf_avars)))
# Plot the relative normalization constants as fxn of max iteration.
plt.errorbar(np.arange(len(z)), -np.log(z),
             yerr=np.sqrt(zerr)/z, label="Iteration 0")
plt.plot(-np.log(z_iter_1), label="Iteration 1")
plt.plot(-np.log(z_iter_1k), label="Iteration 1k", linestyle='--')
plt.xlabel('Window Index')
plt.ylabel('Unitless Free Energy')
plt.title('Window Free Energies and Iter No.')
plt.legend(loc='upper left')
plt.show()

# Print the C7 ax basin probability
#print("EMUS Probability of C7ax basin is %f +/- %f" % (probC7ax, probC7ax_std))
#print("Iterative EMUS Probability of C7ax basin is %f" % (prob_C7ax_iter))

print("Asymptotic coefficient of variation for each partition function:")
print(np.sqrt(zerr)/z)

###

x_tau30 = pmf_centers
y_tau30  = pmf_av_mns/30
err_tau30 =1/30*np.sqrt(pmf_avars)

###

y_tau30_iter  = iterpmf/30

###

#xwham30 = np.loadtxt("./wham-tau30.txt", usecols=(0))
xwham30 = np.loadtxt("wham-30/rate_func.dat", usecols=(0))
ywham30 = np.loadtxt("wham-30/rate_func.dat", usecols=(1))

#xwham100 = np.loadtxt("./wham-tau100.txt", usecols=(0))
xwham100 = np.loadtxt("wham-100/rate_func.dat", usecols=(0))
ywham100 = np.loadtxt("wham-100/rate_func.dat", usecols=(1))

k_2_5_xwham100 = np.loadtxt("./new_k2.5_wham_ratefunc", usecols=(0))
k_2_5_ywham100 = np.loadtxt("./new_k2.5_wham_ratefunc", usecols=(1))

#xdirect30=np.loadtxt("./rate_func_unbiased_tau30.dat", usecols=(0))
xdirect30=np.loadtxt("/home/yuqingqiu/erik-emus/test/k3_direct_ratefunc/ratefunc_30tau_0-1dt.dat", usecols=(0))
ydirect30=np.loadtxt("/home/yuqingqiu/erik-emus/test/k3_direct_ratefunc/ratefunc_30tau_0-1dt.dat", usecols=(1))

#xdirect100=np.loadtxt("./rate_func_unbiased_tau100.dat", usecols=(0))
xdirect100=np.loadtxt("/home/yuqingqiu/erik-emus/test/k3_direct_ratefunc/ratefunc_100tau_0-1dt.dat", usecols=(0))
ydirect100=np.loadtxt("/home/yuqingqiu/erik-emus/test/k3_direct_ratefunc/ratefunc_100tau_0-1dt.dat", usecols=(1))

k_2_5_xdirect100=np.loadtxt("./k2.5_direct_ratefunc", usecols=(0))
k_2_5_ydirect100=np.loadtxt("./k2.5_direct_ratefunc", usecols=(1))

#xclone=np.loadtxt("./clone-data", usecols=(0))
xclone=np.loadtxt("/home/yuqingqiu/erik-emus/test/k3_clone_CGF/tau30", usecols=(0))
yclone=np.loadtxt("/home/yuqingqiu/erik-emus/test/k3_clone_CGF/tau30", usecols=(1))

#xclone100=np.loadtxt("./clone-data-tau100", usecols=(0))
xclone100=np.loadtxt("/home/yuqingqiu/erik-emus/test/k3_clone_CGF/tau100", usecols=(0))
yclone100=np.loadtxt("/home/yuqingqiu/erik-emus/test/k3_clone_CGF/tau100", usecols=(1))

k_2_5_xclone100=np.loadtxt("./k2.5_cgf_ratefunc", usecols=(2))
k_2_5_yclone100=np.loadtxt("./k2.5_cgf_ratefunc", usecols=(3))

###

f =plt.figure()


plt.plot(xdirect100, ydirect100, label=r'$\tau$ = 100 s, direct sampling')
plt.plot(xwham100, ywham100, label=r'$\tau$ = 100 s, wham')

plt.errorbar(x_tau100, y_tau100, yerr= err_tau100, label=r'$\tau$ = 100 s, regular EMUS all $\alpha$')
#plt.errorbar(x_tau100, y_tau100_iter-0.01, yerr= err_tau100, label=r'$\tau$ = 100 s, iter EMUS all $\alpha$')

plt.xlabel(r'$\dot w$')
plt.ylabel(r'$I(\dot w)$')
plt.legend()
plt.title(r'direct sampling vs. EMUS')
plt.show()

###

f =plt.figure()


plt.plot(xdirect30, ydirect30, label=r'$\tau$ = 30 s, direct sampling')
plt.errorbar(x_tau30, y_tau30, yerr= err_tau30, label=r'$\tau$ = 30 s, regular EMUS all $\alpha$')
plt.plot(xwham30, ywham30, label=r'$\tau$ = 30 s, wham')
#plt.plot(x_tau30, y_tau30_iter, label=r'$\tau$ = 30 s, iterative EMUS')
plt.xlabel(r'$\dot w$')
plt.ylabel(r'$I(\dot w)$')
plt.legend()
plt.title(r'direct sampling vs. EMUS')
plt.show()

###

f =plt.figure()


plt.plot(xdirect30, ydirect30, label=r'$\tau$ = 30 s, direct sampling')
plt.plot(xdirect100, ydirect100, label=r'$\tau$ = 100 s, direct sampling')

#plt.plot(xclone, yclone, marker = 'o', label=r'$\tau$ = 30 s, $I(\dot w)$ computed from CGF')
#plt.errorbar(x_tau100_positive ,y_tau100_positive , yerr= err_tau100_positive, label=r'$\tau$ = 100 s, EMUS positive $\alpha$')
#plt.errorbar(x_tau30, y_tau30, yerr= err_tau30, label=r'$\tau$ = 30 s, EMUS all $\alpha$')
#plt.errorbar(x_tau100, y_tau100, yerr= err_tau100, label=r'$\tau$ = 100 s, EMUS all $\alpha$')

plt.plot(x_tau30, y_tau30_iter, label=r'$\tau$ = 30 s, iterative EMUS')
plt.plot(x_tau100, y_tau100_iter, label=r'$\tau$ = 100 s, iterative EMUS')

#plt.xlim([0, 2.5])
#plt.ylim([-0.01, 0.12])
plt.xlabel(r'$\dot w$')
plt.ylabel(r'$I(\dot w)$')
plt.legend()
plt.title(r'direct sampling vs. EMUS with all $\alpha$')
plt.show()

###

f =plt.figure()


plt.plot(xdirect30, ydirect30-min(ydirect30), label=r'$\tau$ = 30 s, direct sampling')
#plt.plot(xdirect100, ydirect100, label=r'$\tau$ = 100 s, direct sampling')
#plt.plot(xclone, yclone, marker = 'o', label=r'$\tau$ = 30 s, $I(\dot w)$ computed from CGF')
#plt.errorbar(x_tau100_positive ,y_tau100_positive , yerr= err_tau100_positive, label=r'$\tau$ = 100 s, EMUS positive $\alpha$')
plt.plot(xwham30, ywham30-min(ywham30), label=r'$\tau$ = 30 s, wham')
#plt.plot(xwham100, ywham100, label=r'$\tau$ = 100 s, wham')
#plt.plot(xclone100, yclone100, marker = 'o', label=r'$\tau$ = 100 s, $I(\dot w)$ computed from CGF')

plt.plot(x_tau30, y_tau30_iter-min(y_tau30_iter), label=r'$\tau$ = 30 s, iterative EMUS')
#plt.plot(x_tau100, y_tau100_iter, label=r'$\tau$ = 100 s, iterative EMUS')

#plt.xlim([0, 2.5])
#plt.ylim([-0.01, 0.12])
plt.xlabel(r'$\dot w$')
plt.ylabel(r'$I(\dot w)$')
plt.legend()
plt.title(r'direct sampling vs. EMUS vs. WHAM')
plt.show()

###

f =plt.figure()


#plt.plot(xdirect30, ydirect30, label=r'$\tau$ = 30 s, direct sampling')
plt.plot(xdirect100, ydirect100 - min(ydirect100), label=r'$\tau$ = 100 s, direct sampling')
#plt.plot(xclone, yclone, marker = 'o', label=r'$\tau$ = 30 s, $I(\dot w)$ computed from CGF')
#plt.errorbar(x_tau100_positive ,y_tau100_positive , yerr= err_tau100_positive, label=r'$\tau$ = 100 s, EMUS positive $\alpha$')
#plt.plot(xwham30, ywham30, label=r'$\tau$ = 30 s, wham')
plt.plot(xwham100, ywham100 - min(ywham100), label=r'$\tau$ = 100 s, wham')
#plt.plot(xclone100, yclone100, marker = 'o', label=r'$\tau$ = 100 s, $I(\dot w)$ computed from CGF')

#plt.plot(x_tau30, y_tau30_iter, label=r'$\tau$ = 30 s, iterative EMUS')
plt.plot(x_tau100, y_tau100_iter - min(y_tau100_iter), label=r'$\tau$ = 100 s, iterative EMUS')

#plt.xlim([0, 2.5])
#plt.ylim([-0.01, 0.12])
plt.xlabel(r'$\dot w$')
plt.ylabel(r'$I(\dot w)$')
plt.legend()
plt.title(r'direct sampling vs. EMUS with all $\alpha$')
plt.show()

###

f =plt.figure()


plt.plot(xdirect30, ydirect30-min(ydirect30), label=r'$\tau$ = 30 s, direct sampling')
#plt.plot(xdirect100, ydirect100, label=r'$\tau$ = 100 s, direct sampling')
#plt.plot(xclone, yclone, marker = 'o', label=r'$\tau$ = 30 s, $I(\dot w)$ computed from CGF')
#plt.errorbar(x_tau100_positive ,y_tau100_positive , yerr= err_tau100_positive, label=r'$\tau$ = 100 s, EMUS positive $\alpha$')
plt.plot(xwham30, ywham30-min(ywham30), label=r'$\tau$ = 30 s, wham')
#plt.plot(xwham100, ywham100, label=r'$\tau$ = 100 s, wham')
#plt.plot(xclone100, yclone100, marker = 'o', label=r'$\tau$ = 100 s, $I(\dot w)$ computed from CGF')

plt.plot(x_tau30, y_tau30_iter-min(y_tau30_iter), label=r'$\tau$ = 30 s, iterative EMUS')
#plt.plot(x_tau100, y_tau100_iter, label=r'$\tau$ = 100 s, iterative EMUS')


plt.plot(xdirect100, ydirect100 - min(ydirect100), label=r'$\tau$ = 100 s, direct sampling')
#plt.plot(xclone, yclone, marker = 'o', label=r'$\tau$ = 30 s, $I(\dot w)$ computed from CGF')
#plt.errorbar(x_tau100_positive ,y_tau100_positive , yerr= err_tau100_positive, label=r'$\tau$ = 100 s, EMUS positive $\alpha$')
#plt.plot(xwham30, ywham30, label=r'$\tau$ = 30 s, wham')
plt.plot(xwham100, ywham100 - min(ywham100), label=r'$\tau$ = 100 s, wham')
#plt.plot(xclone100, yclone100, marker = 'o', label=r'$\tau$ = 100 s, $I(\dot w)$ computed from CGF')

#plt.plot(x_tau30, y_tau30_iter, label=r'$\tau$ = 30 s, iterative EMUS')
plt.plot(x_tau100, y_tau100_iter - min(y_tau100_iter), label=r'$\tau$ = 100 s, iterative EMUS')


#plt.xlim([0, 2.5])
#plt.ylim([-0.01, 0.12])
plt.xlabel(r'$\dot w$')
plt.ylabel(r'$I(\dot w)$')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.title(r'direct sampling vs. EMUS vs. WHAM')
plt.show()
