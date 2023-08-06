# -*- coding:utf-8 -*-
# @Author: Niccolò Bonacchi
# @Date: Thursday, February 21st 2019, 6:42:55 pm
# @Last Modified by: Niccolò Bonacchi
# @Last Modified time: 21-02-2019 07:12:43.4343
import json
import ibllib.io.raw_data_loaders as raw
import matplotlib.pyplot as plt
import numpy as np


def get_port_events(events: dict, name: str = '') -> list:
    out: list = []
    for k in events:
        if name in k:
            out.extend(events[k])
    out = sorted(out)

    return out


if __name__ == '__main__':
    root = '/mnt/s0/IntegrationTests/Subjects_init/'
    session = 'ZM_1085/2019-02-12/002/'
    file = 'raw_behavior_data/_iblrig_taskData.raw.jsonable'

    session_data_file = root + session + file

    data = raw.load_data(root + session)
    unsynced_trial_count = 0
    frame2ttl = []
    sound = []
    camera = []
    trial_end = []
    for trial_data in data:
        tevents = trial_data['behavior_data']['Events timestamps']
        ev_bnc1 = get_port_events(tevents, name='BNC1')
        ev_bnc2 = get_port_events(tevents, name='BNC2')
        ev_port1 = get_port_events(tevents, name='Port1')
        if not ev_bnc1 or not ev_bnc2 or not ev_port1:
            unsynced_trial_count += 1
        frame2ttl.extend(ev_bnc1)
        sound.extend(ev_bnc2)
        camera.extend(ev_port1)
        trial_end.append(trial_data['behavior_data']['Trial end timestamp'])
    print(f'Found {unsynced_trial_count} trials with bad sync data')

    f = plt.figure()  # figsize=(19.2, 10.8), dpi=100)
    ax = plt.subplot2grid((1, 1), (0, 0), rowspan=1, colspan=1)

    ax.plot(camera, np.ones(len(camera)) * 1, '|')
    ax.plot(sound, np.ones(len(sound)) * 2, '|')
    ax.plot(frame2ttl, np.ones(len(frame2ttl)) * 3, '|')
    [ax.axvline(t, alpha=0.5) for t in trial_end]
    ax.set_ylim([0, 4])
    ax.set_yticks(range(4))
    ax.set_yticklabels(['', 'camera', 'sound', 'frame2ttl'])
    plt.show()


# fpath = '/home/nico/Projects/IBL/IBL-github/scratch/assertEqual_fail_after_this_trial.jsonable'  # noqa


# with open(fpath) as f:
#     trial = json.load(f)


# print(trial)

# behavior_data = trial[0]['behavior_data']

# correct = ~np.isnan(behavior_data['States timestamps']['correct'][0][0])
# error = ~np.isnan(behavior_data['States timestamps']['error'][0][0])
# no_go = ~np.isnan(behavior_data['States timestamps']['no_go'][0][0])
# assert correct or error or no_go
