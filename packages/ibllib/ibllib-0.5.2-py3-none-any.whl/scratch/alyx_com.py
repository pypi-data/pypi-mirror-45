# -*- coding: utf-8 -*-
# @Author: nico
# @Date:   2018-03-28 15:26:16
# @Last Modified by:   nico
# @Last Modified time: 2018-04-09 14:32:51

# import os
# import subprocess
import requests
import uuid
import json

ACT = 'GET'
ALYX = 'http://alyx.champalimaud.pt:8000'
COMMAND = ''
AUTH = "-H '{Authorization: Token 4aab2b946ee6b55ab94162584e5bec702a481e1f,  Accept: application/vnd.alyx.v1+json}'"

# s = "curl -X {0} {1}{2} {3}".format(ACT, ALYX, COMMAND, AUTH)

# # print(s)
# # curl -X GET http://alyx.champalimaud.pt:8000/sessions -H 'Authorization: Token 4aab2b946ee6b55ab94162584e5bec702a481e1f'

# p = subprocess.Popen(s, shell=True,
#                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

# for line in p.stdout.readlines():
#     print(line)

# data = json.loads(line.decode('utf-8'))

user = {'id': 6, 'subjects_responsible': ['test_subject'], 'username': 'test_REST_user_input', 'email': 'None'}
suuid = '4cf90801-e4a6-4575-aaa3-b2fbce159169'  # uuid.uuid4()
subject = {
    'nickname': 'test_post',
    'url': 'http://alyx.champalimaud.pt:8000/subjects/test_post',
    'id': suuid,
    'responsible_user': 'nico',
    'birth_date': '2018-03-30',
    'age_weeks': 1,
    'projects': ['IBL'],
    'death_date': None,
    'species': 'mouse',
    'sex': 'U',
    'litter': None,
    'strain': 'C57BL/6',
    'source': 'CCU-Vivarium',
    'line': None,
    'description': '',
    'actions_sessions': [],
    'weighings': [],
    'water_administrations': [],
    'genotype': [],
    'water_requirement_total': 0,
    'water_requirement_remaining': 0
}

sub2 = {
        "nickname": "template_subject_post",
        "responsible_user": "root",
        "birth_date": None,
        "death_date": None,
        "species": None,
        "sex": "U",
        "litter": None,
        "strain": None,
        "line": None,
        "description": "",
        "genotype": [],
        "alive": True
    }

#     {
#     "nickname": "",
#     "responsible_user": null,
#     "birth_date": null,
#     "death_date": null,
#     "species": null,
#     "sex": null,
#     "litter": null,
#     "strain": null,
#     "line": null,
#     "description": "",
#     "genotype": []
# }

COMMAND = '/users'

url = ALYX + COMMAND

users = requests.get(ALYX + '/users')


headers = {
    'Authorization': 'Token 4aab2b946ee6b55ab94162584e5bec702a481e1f',
    'Accept': 'application/json',
    'Content-Type': 'application/json',

}

data = {'strain': 'C57BL/6'}
data = {'strain': 'VGlut-2-ChR2-het'}

s4577 = requests.get(ALYX + '/subjects/4577', headers=headers)
subjects = requests.get(ALYX + '/subjects', headers=headers)
p4577 = requests.patch(ALYX + '/subjects/4577', headers=headers, data=data)
template_subject = requests.get(ALYX + '/subjects/template_subject',
                                headers=headers)

jsubject = json.dumps(subject)
jsub2 = json.dumps(sub2)
test_post = requests.post(ALYX + '/subjects', data=jsub2, headers=headers)


# TEST all RESTful API commands

# HTTP Verb     CRUD
# ------------  -------------
# POST          Create
# GET           Read
# PUT           Update/Replace
# PATCH         Update/Modify
# DELETE        Delete
# OPTIONS       ????

endpoints = ['/subjects', '/water-restricted-subjects', '/weighings',
             '/data-repository', '/dataset-types', '/exp-metadata',
             '/data-formats', '/users', '/subjects', '/data-repository-type',
             '/datasets', '/files', '/timescales', '/sessions',
             '/water-administrations', ]

test_options = []
for endpoint in endpoints:
    test_options.append(requests.options(ALYX + endpoint, headers=headers))

options_errs = [x for x in test_options if ~x.ok]
jendpoint_options = [x.json() if x.ok else x for x in test_options]

endpoint_get = []
for endpoint in endpoints:
    endpoint_get.append(requests.get(ALYX + endpoint, headers=headers))

jendpoint_get = [x.json() if x.ok else x for x in jendpoint_options]





