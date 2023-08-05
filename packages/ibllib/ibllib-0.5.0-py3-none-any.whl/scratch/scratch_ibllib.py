
from ibllib.graphic import login
from oneibl.webclient import AlyxClient

[usr, pwd] = login()


ac = AlyxClient(base_url='https://alyx.internationalbrainlab.org', username=usr, password=pwd)

all_subjects = ac.rest('subjects', 'list')
details_on_one_subject = ac.rest('subjects', 'read', 'IBL_30')
