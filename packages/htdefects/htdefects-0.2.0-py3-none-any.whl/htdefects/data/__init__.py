import os
import json

"""Import properties of elements and assign to a module-level variable."""

ELEM_VOLUMES = {}
current_file_dir = os.path.abspath(os.path.dirname(__file__))
elemental_volumes_file = os.path.join(current_file_dir, 'elemental_volumes.json')
if os.path.isfile(elemental_volumes_file):
    with open(elemental_volumes_file, 'r') as fr:
        ELEM_VOLUMES = json.load(fr)
