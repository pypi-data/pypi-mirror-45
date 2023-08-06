# flake8: noqa
# # Create conditional poop_count.flag from POOP_COUNT = True or False
# Find poop_count.flag for day='today' ['all']
# open settings file for session
# ask for poop count and update POOP_COUNT in settings dict
# save patched settings file
# create session (this should delete create_me.flag)
# delete poop_count.flag

#
# from pathlib import Path
# import matplotlib.pyplot as plt
# import numpy as np
# import json
# from dateutil import parser

# from ibllib.misc import pprint
# from oneibl.one import ONE
# from ibllib.misc import pprint
# from ibllib.io import raw_data_loaders as raw
# from alf.folders import find_sessions


# from dateutil import rrule, parser
# date_range = ['2019-01-17', '2019-01-24']
# date1 = date_range[0]
# date2 = date_range[1]
# dates = list(rrule.rrule(rrule.DAILY, dtstart=parser.parse(
#     date1), until=parser.parse(date2)))
# dates = [str(x.date()) for x in dates]
# local_folder = Path('/mnt/s1/shared-mainen/IBL/iblrig_data/Subjects/')
# local_sessions = find_sessions(local_folder)

# date_sessions = [x for x in local_sessions for y in dates if y in x]

# date_sessions = ['/'.join(Path(x).parts[-3:]) for x in date_sessions]


# # one = ONE()
# one = ONE()

# sess, det = one.search(users='ines', details=True, date_range=date_range)
# idx = ['_iblrig_' in x['task_protocol'] for x in det]
# det = np.array(det)[idx].tolist()
# sessions = [json.loads(x['json'])['SESSION_FOLDER'] for x in det]
# sessions = ['/'.join(Path(x.replace('\\', '/')).parts[-3:]) for x in sessions]


# if len(date_sessions) > len(sessions):
#     missing = set(date_sessions) - set(sessions)



# sessions, det = one.search(users='valeria', details=True, date_range=[
#                            '2019-01-28'], subjects='IBL_36')

# dtypes = ['_iblrig_taskData.raw',
#           '_iblrig_taskSettings.raw']

# ses_data, md = one.load(sessions[0], dataset_types=dtypes, clobber=False)

# ses_duration_secs = ses_data[-1]['behavior_data']['Trial end timestamp'] - \
#     ses_data[-1]['behavior_data']['Bpod start timestamp']

# for sd in ses_data:
#     print(sd['behavior_data']['Trial end timestamp'])

# #

# # Alyx login


# from pathlib import Path
# import ibllib.io.params as params
# import oneibl.params
# from alf.one_iblrig import create

# pfile = Path(params.getfile('one_params'))
# if not pfile.exists():
#     oneibl.params.setup_alyx_params()

# create()


# from ibllib.misc import login
# from oneibl.webclient import AlyxClient

# one_params = params.read('one_params')





# [usr, pwd] = login.login()


# ac = AlyxClient(base_url='https://alyx.internationalbrainlab.org',
#                 username=usr, password=pwd)

# all_subjects = ac.rest('subjects', 'list')
# details_on_one_subject = ac.rest('subjects', 'read', 'IBL_30')

def init_var3(obj):
    obj.var3 = 33
    return obj


class test(object):
    def __init__(self):
        init_var3(self)
        self.var = 1
        self.var2 = 2




t = test()
