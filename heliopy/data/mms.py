"""
Methods for importing data from the four MMS spacecraft.

All data is publically available at
https://lasp.colorado.edu/mms/sdc/public/data/, and the MMS science data centre
is at https://lasp.colorado.edu/mms/sdc/public/.
"""
from datetime import datetime
import pandas as pd

import heliopy.time as spacetime
from heliopy.data import helper
from heliopy import config

data_dir = config['default']['download_dir']
mms_dir = data_dir + '/mms/'
remote_mms_dir = 'https://lasp.colorado.edu/mms/sdc/public/data/'


def fpi_dis_moms(probe, mode, starttime, endtime):
    """
    Import fpi distribution moment data.

    Parameters
    ----------
        probe : string
            Probe number, must be 1, 2, 3, or 4
        mode : string
            Data mode, must be 'fast' or 'brst'
        starttime : datetime
            Interval start time.
        endtime : datetime
            Interval end time.

    Returns
    -------
        data : DataFrame
            Imported data.
    """
    valid_modes = ['fast', 'brst']
    if mode not in valid_modes:
        raise RuntimeError('Mode must be either fast or brst')
    # Directory relative to main MMS data directory
    relative_dir = 'mms' + probe + '/fpi/' + mode + '/l2/dis-moms/'

    daylist = spacetime.daysplitinterval(starttime, endtime)
    data = []
    for day in daylist:
        date = day[0]
        this_relative_dir = relative_dir + str(date.year) + '/' +\
            str(date.month).zfill(2)
        filename = 'mms' + probe + '_fpi_' + mode + '_l2_dis-moms_' +\
            str(date.year) +\
            str(date.month).zfill(2) +\
            str(date.day).zfill(2) +\
            '000000' + \
            '_v3.1.1.cdf'

        # Absolute path to local directory for this data file
        local_dir = mms_dir + this_relative_dir
        helper.checkdir(local_dir)

        remote_url = remote_mms_dir + this_relative_dir
        # Load cdf file
        cdf = helper.load(filename, local_dir, remote_url)

        probestr = 'mms' + probe + '_'
        # Convert cdf to dataframe
        keys = {'Epoch': 'Time',
                probestr + 'dis_bulkv_gse_fast': ['bulkv_x', 'bulkv_y', 'bulkv_z'],
                probestr + 'dis_heatq_gse_fast': ['heatq_x', 'heatq_y', 'heatq_z'],
                probestr + 'dis_numberdensity_fast': 'n',
                probestr + 'dis_temppara_fast': 'T_par',
                probestr + 'dis_tempperp_fast': 'T_perp'}
        df = helper.cdf2df(cdf, 'Epoch', keys)
        data.append(df)

    data = pd.concat(data)
    data = data[(data['Time'] > starttime) & (data['Time'] < endtime)]
    return data


def fgm_survey(probe, starttime, endtime):
    """
    Import fgm survey mode data.

    Parameters
    ----------
        probe : string
            Probe number, must be 1, 2, 3, or 4
        starttime : datetime
            Interval start time.
        endtime : datetime
            Interval end time.

    Returns
    -------
        data : DataFrame
            Imported data.
    """
    # Directory relative to main MMS data directory
    relative_dir = 'mms' + probe + '/fgm/srvy/l2/'

    daylist = spacetime.daysplitinterval(starttime, endtime)
    data = []
    for day in daylist:
        date = day[0]
        this_relative_dir = relative_dir + str(date.year) + '/' +\
            str(date.month).zfill(2)
        filename = 'mms' + probe + '_fgm_srvy_l2_' +\
            str(date.year) +\
            str(date.month).zfill(2) +\
            str(date.day).zfill(2) +\
            '_v4.18.0.cdf'

        # Absolute path to local directory for this data file
        local_dir = mms_dir + this_relative_dir
        helper.checkdir(local_dir)

        remote_url = remote_mms_dir + this_relative_dir
        # Load cdf file
        cdf = helper.load(filename, local_dir, remote_url)

        # Convert cdf to dataframe
        keys = {'mms' + probe + '_fgm_b_gsm_srvy_l2': ['Bx', 'By', 'Bz', 'Br'],
                'Epoch': 'Time'}
        df = helper.cdf2df(cdf, 'Epoch', keys)
        data.append(df)

    data = pd.concat(data)
    data = data[(data['Time'] > starttime) & (data['Time'] < endtime)]
    return data

if __name__ == '__main__':
    starttime = datetime(2016, 1, 1, 0, 0, 0)
    endtime = datetime(2016, 1, 1, 23, 59, 59)
    data = fpi_dis_moms('2', 'fast', starttime, endtime)
    print(data)
