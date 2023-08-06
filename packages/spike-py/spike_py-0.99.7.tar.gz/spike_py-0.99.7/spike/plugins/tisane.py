#!/usr/bin/env python 
# encoding: utf-8

"""
Tisane : Parallelized Sane
"""

from __future__ import print_function
from spike import NPKError
from spike.NPKData import NPKData_plugin
import os
import numpy as np
from numpy.fft import fft, ifft
from time import time
from spike.Algo.sane import sane, OPTK
import multiprocessing as mp
import logging
#from plot_bokeh import BOKEH_PLOT
from spike.util.signal_tools import findnoiselevel

########################################################################

#bplt = BOKEH_PLOT()

def local_sane(xarg, debug=0):
    '''
    Makes Sane on the shorted buffer
    Returns a denoised short buffer and the corresponding interval
    ###
    buf : numpy array with signal
    interv : list of the bounds
    rank : rank for Sane
    iterations : number of time that Tisane is applied
    '''
    buf, interv, rank, iterations, above_noise, thresh_level = xarg
    if debug>1 : print("rank is {0} ".format(rank))
    if not rank:
        if debug>1 : print('######## Using optimisation !!!!')
        optrk = OPTK(buf, orda = buf.size//2, sane_optk=True, above_noise=above_noise, thresh_level=thresh_level,  debug=False)          # instantiate the class                    
        rank = optrk.find_best_rank()                                              # automatic optimal rank estimation.   
        if debug>1 : print('optimal rank found is {0} '.format(rank))
    #rank = 10
    denbuf = fft(sane(ifft(buf), k = rank, iterations = iterations))

    return denbuf, interv


def find_thresh(spec, above_noise, debug=False):
    '''
    Finding a general threshold on the whole dataset.
    '''
    noiselev = np.abs(findnoiselevel(spec, nbseg = 10))                           # finds noise level
    ###
    nbseg = 20
    less = len(spec)%nbseg     # rest of division of length of data by nb of segment
    restpeaks = spec[less:]   # remove the points that avoid to divide correctly the data in segment of same size.
    mean_level = np.abs(restpeaks.mean())
    noiselev += mean_level
    if debug:
        print("noiselevel found is ", noiselev) 
    thresh_level = above_noise*noiselev
    return thresh_level
 

def tisane(npkd, rank = None, nbinterv = 400, above_noise=3, threshold=False, slice_bounds = None,  nbcores = 1, mixing=False, iterations=1, debug=1):
    """
    Algorithm for an application of Sane by parts.
    tisane stands for Tilded Integration for Sane
    Ti-Sane denoises the spectrum on tilded truncks.. half of each denoised interval is superposed on left and right on neighbours intervals. 
    The algorithm uses Multiprocessing. It works on complex spectrum. 
    ###
    npkd : NPKData object
    rank :  rank for Sane, if no rank is given, it uses OPTK
    nbinterv : number of intervals
    above_noise : number of time the threshold is above the noise level. 
    threshold : if True, calculate a threshold applied to the whole dataset when processed with Sane. 
    slice_bounds : interval used.
    nbcores : number of cores used for parallelization
    mixing : used for giving a correct weight to each denoised interval
    iterations = nb of times that sane is repeated inside tisane
    """
    print('############ Entering in Tisane  !!!!!')

    if slice_bounds:
        npkd.extract(slice_bounds[0], slice_bounds[1])
    delta = npkd.get_buffer().size//nbinterv        # /2 only to go fast for petroleomics dataset !!!!!

    subd = delta//2    # recovering interval (width delta), denoising made on [delta-subd, delta+subd], normally subd = delta/2

    if False:                                                   
        if debug>1 : print("delta*nbinterv ", delta*nbinterv)
        if debug>1 : print("delta  ", delta)
    npkdmax = npkd.copy()  
    spec = npkdmax.modulus().get_buffer()[:delta*nbinterv]                 # Spectrum modulus for finding the heaviest segment (mixing mode)
    if debug>1 : print("spec.size ", spec.size)
    lspec = np.array_split(spec, nbinterv)[10:-10]                         # list of the intervals of width delta, takes the middle intervals
    ll = [l.sum() for l in lspec]                                          # list of the integral on each interval
    maxinterv = lspec[ll.index(max(ll))]                                   # interval with maximum energy

    if debug>1 :
        print("maxinterv.size ", maxinterv.size)
        print("lspec[100].size ",lspec[100].size)
        print("lspec[150].size ",lspec[150].size)
        print("ll.index(max(ll) ", ll.index(max(ll)))
        print("lspec length is ", len(lspec))

    def iterarg(p, delta, rank, iterations, above_noise, thresh_level, debug= 1):
        '''
        Iterator for making Sane on slices
        input: 
            p : full spectrum
            delta : width of intervals
            rank : rank for Sane
        output:
            buf : spectrum interval as numpy array
            interv : list of the interval limits
            rank : Sane rank
        '''
        for i in range(nbinterv):
            limd = max(0, i*delta-subd)                             # interval limit inf
            limu = min((i+1)*delta+subd, (nbinterv)*delta)          # interval limit sup
            buf = p.get_buffer()[limd:limu]                         # spectrum numpy array on the interval
            if mixing:
                buf = np.concatenate((maxinterv, buf))              # mixing for normalizing the signal
            interv = [limd, limu]
            yield (buf, interv, rank, iterations, above_noise, thresh_level)
    
    #thresh_level = None # find_thresh(spec, above_noise)
    if threshold:
        thresh_level = find_thresh(spec, above_noise)
        print("#########  Threshold found is ", thresh_level)
    else:
        thresh_level = None # 
    #print("#########  Threshold found is ", tt)
    pool = mp.Pool(nbcores)                                         # Must be placed after the functions called !!!
    xarg = iterarg(npkd, delta, rank, iterations, above_noise, thresh_level)      # Iterator returning buffer, interval and rank
    t0 = time()
    res = pool.imap(local_sane, xarg)                               # map with iterator
    npkdz = npkd.copy() # 
    npkdz.set_buffer(np.zeros(npkdz.get_buffer().size)*(1+1j))      # Makes a null vector
    valpercent = 0
    percent_step = 10
    for i,result in enumerate(res):                                 # Filling the zero spectrum with denoised trunks
        if debug>1 : print(i)
        percent = int(i/float(nbinterv)*100)
        if percent % percent_step == 0 and percent > valpercent:
            logging.info("Done : {0}%".format(percent))
            valpercent += percent_step
        denbuf, interv = result

        ###
        if False:
            if i in range(nbinterv//3-10, nbinterv//3+10):
                if debug>1 : print("i used is ", i)
                if debug>1 : print("interval is ", interv)
                bplt.xlim(interv[0], interv[1])
                bplt.plot(np.arange(interv[0], interv[1]),  np.abs(denbuf.copy()))
                bplt.show()
                bplt.savefig('plot_interv_{0}-{1}.html'.format(interv[0], interv[1]))

        ###

        if mixing:
            denbuf = denbuf[delta:]
        buf = npkdz.get_buffer()
        if False:
            if debug>1 : print("buf[interv[0]:interv[1]].size ", buf[interv[0]:interv[1]].size)
            if debug>1 : print("denbuf.size ", denbuf.size)
        buf[interv[0]:interv[1]] += denbuf                          # adds the denoised interval in the full spectrum
        npkdz.set_buffer(buf) # 
    buf = npkdz.get_buffer()
    npkd.set_buffer(buf/2)                                         # replace spectrum by the denoised result
    pool.close()
    pool.terminate()
    pool.join()

NPKData_plugin("tisane", tisane)
