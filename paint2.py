# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

# example data
samples = [10, 20]
files = [r'./prd/infoquery-%r.jtl' % time for time in samples]

try:
    xmax = 0
    for nums, file in zip(samples, files):
        log = pd.read_csv(file, low_memory=False)
        http = log[log.label != 'MD5']
        success = http[http.failureMessage.isnull()]
        # success = http
        num_bins = 300
        data = success.loc[:, ('timeStamp', 'Latency')]
        f = lambda x: pd.to_datetime(x, unit='ms')
        min_time = min(data['timeStamp'])
        max_time = max(data['timeStamp'])
        step = 6000
        basetime = range(min_time, max_time + step, step)
        time = map(f, basetime)
        basetime = [(i - basetime[0]) / 1000 for i in basetime]
        data['timeStamp'] = data['timeStamp'].map(f)
        mid_data = [0] * len(time)
        for i, k in enumerate(time):
            if i != 0:
                mid_data[i - 1] = [data[data['timeStamp'] < k]['Latency'].count(),
                                   data[data['timeStamp'] < k]['Latency'].sum()]
        mid_data = mid_data[:-1]
        y = []
        mid = [0, 0]
        for temp in mid_data:
            if temp[0] - mid[0]:
                y.append(float(temp[1] - mid[1]) / float(temp[0] - mid[0]))
            else:
                y.append(y[-1])
            if y[-1] > 25000:
                print file
            mid = temp
        # the histogram of the data
        print len(y)
        plt.plot(basetime[:-1], y, label='Load %r' % nums)
        xmax = max(xmax, basetime[-1])
    # add a 'best fit' line
    plt.xlim(basetime[0] - xmax / 12, xmax * 17 / 12)
    # plt.ylim(min(y)-1500,max(y)+500)
    plt.grid(True)
    plt.ylabel('Latency(ms)')
    plt.xlabel('Time(s)')
    plt.title('Lantency by time')
    plt.legend(loc=7)

    # Tweak spacing to prevent clipping of ylabel
    plt.show()
except IOError:
    print 'File %s does not exist!' % file
