# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import matplotlib.pyplot as plt
import pandas as pd

# example data
file = r'./prd/infoquery-160.jtl'
try:
    log = pd.read_csv(file, low_memory=False)
    http = log[log.label != 'MD5']
    success = http[http.failureMessage.isnull()]
    success = success[success['Latency']<1500]
    fig, ax = plt.subplots()
    num_bins = 300
    # the histogram of the data
    n, bins, patches = ax.hist(success['Latency'], num_bins, normed=1)
    # add a 'best fit' line
    ax.set_xlabel('Latency(ms)')
    ax.set_ylabel('Probability density')
    ax.set_title(r'The distribution of response times')

    # Tweak spacing to prevent clipping of ylabel
    fig.tight_layout()
    plt.show()
except IOError:
    print 'File %s does not exist!' % file
