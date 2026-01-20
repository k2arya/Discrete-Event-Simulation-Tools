"""

Utility Functions for Discrete-Event Simulation.

Version : 0.1

MIT License

Copyright (c) 2025  Korhan Kanar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import numpy as np

class IDGenerator():
    """ Generate unique ID number for objects """
    def __init__(self):
        self.next_id = 0
        
    def getID(self):
        """ Get the next available ID """
        next_id = self.next_id
        self.next_id += 1
        return next_id
    

class TArray():
    """ Class for array with time-stamps """
    
    def __init__(self, val_init):
        """
        Initialize time-array

        Parameters
        ----------
        val_init : float
            Value at t = 0

        Returns
        -------
        None.

        """
        self.t = [0.0]
        self.val = [val_init]
        
        
    def add(self, t, val):
        """
        Add new data point to the array.

        Parameters
        ----------
        t : float
            time-stamp of the data point
        val : float
            value of the data.

        Returns
        -------
        None.

        """

        if t == self.t[-1]:
            # Overwrite new value
            self.t[-1] = t
            self.val[-1] = val 
                      
        self.t.append(t)
        self.val.append(val)
        

def segment_metrics(t_arr, val_arr, metrics, period):
    """
    

    Parameters
    ----------
    t_arr : TYPE
        DESCRIPTION.
    val_arr : TYPE
        DESCRIPTION.
    metrics : TYPE
        DESCRIPTION.
    period : TYPE
        DESCRIPTION.

    Returns
    -------
    D : TYPE
        DESCRIPTION.

    """
    
    D = {'segment_start':[], 'segment_end':[]}
    metric_fun = []
    for metric in metrics:
        if metric == 'time_avg':
            metric_fun.append(('time_avg',time_avg))
            D['time_avg']=[]
        elif metric == 'max':
            metric_fun.append(('max', segment_max))
            D['max']=[]
        elif metric == 'min':
            metric_fun.append(('min', segment_min))
            D['min']=[]  
    
    t0 = 0
    dt = min(period, max(t_arr)-t0)
    
    while dt >= 0.5*period:
        
        D['segment_start'].append(t0)
        D['segment_end'].append(t0+dt)
        
        ts, ns = get_segment(t_arr, val_arr, t0, t0+dt)
        
        for metric_name, fun in metric_fun:
            D[metric_name].append(fun(ts, ns))
        
        t0 += period
        dt = min(period, max(t_arr)-t0)

    return D

             
        
def get_segment(t_arr, val_arr, t_start, t_end, indices=None):
    """
    Get slice of time and value arrays.

    Parameters
    ----------
    t_arr : TYPE
        DESCRIPTION.
    val_arr : TYPE
        DESCRIPTION.
    t_start : TYPE
        DESCRIPTION.
    t_end : TYPE
        DESCRIPTION.
    indices : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    t_slice : TYPE
        DESCRIPTION.
    val_slice : TYPE
        DESCRIPTION.

    """


    # TODO : Move outside for faster exec.
    if indices is None:
        indices = np.arange(len(t_arr))

    # Select
    s = (t_arr >= t_start) & (t_arr <= t_end)
    
    # Values bet. start and end times
    t_slice = t_arr[s]
    val_slice = val_arr[s]

    # Add start and end points to the slice
    if s.any():    
        if t_start < t_slice[0]:
            t_slice = np.append(t_start, t_slice)
            val_slice = np.append(val_arr[indices[s].min() - 1], val_slice)
    
        if t_end > t_slice[-1]:
            t_slice = np.append(t_slice, t_end)
            val_slice = np.append(val_slice, val_arr[indices[s].max()])
    else:
        t_slice = np.array([t_start, t_end])
        i = indices[t_arr < t_start].max()
        val_slice = np.array([val_arr[i], val_arr[i]])
    
    return t_slice, val_slice   

# Functions evaluating segment metrics
def time_avg(ts, ns):
    dts = np.diff(ts)
    avg = (dts * ns[0:-1]).sum() / (ts[-1]-ts[0])
    return avg

def segment_max(ts, ns):
    return ns.max()

def segment_min(ts, ns):
    return ns.min()
    
        
