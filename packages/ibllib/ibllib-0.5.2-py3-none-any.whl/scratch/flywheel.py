#!/usr/bin/env python
from pathlib import Path
import flywheel
import ibllib.io.raw_data_loaders as raw

fw = flywheel.Flywheel('jhu.flywheel.io:JuKWDoTS8VDu2MVXKL')
root_path = '/home/nico/Projects/IBL/iblrig/scratch/test_iblrig_data/Subjects'
sess_path = Path().joinpath(root_path, 'ZM_1085/2019-02-12/002')
sess_meta = raw.load_settings(sess_path)

# session = fw.lookup('test/Example Data/ZM_1085/002')
# session = fw.lookup('test/mainenlab/ZM_1085/2019-02-12_002')

project = fw.lookup('test/mainenlab')

subject = project.add_subject(code=sess_path.parent.parent.name)
# subject.update_info()
session = subject.add_session(label=f'{sess_path.parent.name}_{sess_path.name}')
session.update_info()

acq_name = sess_meta['PYBPOD_PROTOCOL']
acquisition = session.add_acquisition(label=f'{acq_name}')

# analysis = session.add_analysis(label='extraction', inputs=[file_ref])
analysis = session.add_analysis(label='extraction')
#acquisition.update_info({'key': 'value'})


# acquisition = fw.lookup('test/Example Data/ZM_1085/002/[behavior, video]')
# print(acquisition)

# file_ref = acquisition.get_file('link.md').ref()
# analysis = fw.lookup('test/Example Data/ZM_1085/002/analyses/Extraction')
# analysis.upload_output([
#     '/home/nico/Projects/IBL/iblrig/scratch/test_iblrig_data/Subjects/ZM_1085/2019-02-12/002/extraction_link.md',
#     '/home/nico/Projects/IBL/iblrig/scratch/test_iblrig_data/Subjects/ZM_1085/2019-02-12/002/extract_register.log')
