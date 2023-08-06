import os
import json
from pathlib import Path

# self.ROOT_DATA_FOLDER = "/mnt/s1/mainen/shared/IBL/dev_iblrig_data/Subjects"
# self.BOARD = 'box0'


# def self.get_subfolder_paths(folder):
#     out = [os.path.join(folder, x) for x in os.listdir(folder)
#             if os.path.isdir(os.path.join(folder, x))]
#     return out


# rdf = Path(self.ROOT_DATA_FOLDER)
# cal = rdf / '_iblrig_calibration'
# if not cal.exists():
#     return None

# cal_session_folders = []
# for date in self.get_subfolder_paths(str(cal)):
#     cal_session_folders.extend(self.get_subfolder_paths(date))

water_cal_files = []
for session in cal_session_folders:
    session = Path(session) / 'raw_behavior_data'
    water_cal_files.extend(list(session.glob(
        '_iblrig_calibration_water_function.csv')))

water_cal_files = sorted(water_cal_files,
                         key=lambda x: int(x.parent.parent.name))

if not water_cal_files:
    return

water_cal_settings = [x.parent / "_iblrig_taskSettings.raw.json"
                      for x in water_cal_files]
same_board_cal_files = []
for fcal, s in zip(water_cal_files, water_cal_settings):
    if s.exists():
        with open(str(s), 'r') as f:
            settings = json.loads(f.readline())
        if settings['PYBPOD_BOARD'] == self.BOARD:
            same_board_cal_files.append(fcal)

same_board_cal_files = sorted(same_board_cal_files,
                              key=lambda x: int(x.parent.parent.name))
