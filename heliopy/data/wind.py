import pyspace.time as spacetime
from pyspace.data import helper
from pyspace import config
import pandas as pd
import os

'''
Methods for importing data from the WIND spacecraft
All data is publically available at ftp://spdf.gsfc.nasa.gov/pub/data/wind
'''
data_dir = config['default']['download_dir']
wind_dir = data_dir + '/wind'
remote_wind_dir = 'ftp://spdf.gsfc.nasa.gov/pub/data/wind'


def threedp_pm(startTime, endTime):
    # Directory relative to main WIND data directory
    relative_dir = '/3dp/3dp_pm'

    daylist = spacetime.daysplitinterval(startTime, endTime)
    data = []
    for day in daylist:
        date = day[0]
        filename = 'wi_pm_3dp_' +\
            str(date.year) +\
            str(date.month).zfill(2) +\
            str(date.day).zfill(2) +\
            '_v05.cdf'
        this_relative_dir = relative_dir + '/' + str(day[0].year)
        # Absolute path to local directory for this data file
        local_dir = wind_dir + this_relative_dir
        helper.checkdir(local_dir)

        remote_url = remote_wind_dir + this_relative_dir

        cdf = helper.load(filename, local_dir, remote_url)
        df = helper.cdf2df(cdf)
        data.append(df)

    return pd.concat(data)
