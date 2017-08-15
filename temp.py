# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import matplotlib.pyplot as plt
import pandas as pd


def stats(x):
    return pd.Series(
        [x.count(), x.mean(), x.median(), x.quantile(.9), x.quantile(.95), x.quantile(.99), x.min(), x.max(), x.std()],
        index=['Count', 'Average', 'Median', '90%', '95%', '99%', 'Min', 'Max', 'Std'])


filename = r'getVouchersAgain-50.jtl'
try:
    log = pd.read_csv(filename)
    http = log[log.label != 'MD5']
    success = http[http.failureMessage.isnull()]
    print stats(success['Latency'])
    plt.plot(success['timeStamp'], success['Latency'], label="$sin(x)$", color="red", linewidth=1)
    plt.legend()
    plt.show()
    fail = http[http.failureMessage.notnull()]
    # print fail
    print stats(fail['Latency'])
    print fail.groupby(['responseCode']).count()['timeStamp']
except IOError:
    print 'File %s does not exist!' % filename
