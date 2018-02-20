import yaml
import os
import glob

# import custom scripts
from db_formation import formation, formation_list, formation_group
from db_weapons import weapon_list, weapon_gun, weapon_atgm
from db_equipment import equip_list, equipment_inf, equipment_afv, equipment_pc

# set the working directory to the script location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# load in the weapons
# use of recursive=True with /**/ notation allows searching subdirs
weaps = []
for fid in glob.glob('../database/weapons/**/*yml', recursive=True):
    with open(fid) as f:
        weaps.append(yaml.load(f))
    weaps[-1].GenTLI()
# create the weapon database
weaps_db = weapon_list(weaps)

# load in the equipment
equip = []
for fid in glob.glob('../database/equipment/**/*yml', recursive=True):
    with open(fid) as f:
        equip.append(yaml.load(f))
        equip[-1].GenTLI(weaps_db)
equip_db = equip_list(equip)

# Load the formation elements
forms = []
for fid in glob.glob('../database/formations/**/*.yml', recursive=True):
    with open(fid) as f:
        forms.append(yaml.load(f))
    forms[-1].GenOLI(equip_db)

forms_list = formation_list(forms)

# Load the formation groups
groups = []
for fid in glob.glob('../database/groups/*.yml'):
    with open(fid) as f:
        groups.append(yaml.load(f))
# now generate new formations for each group
for grp in groups:
    new_formation = grp.generate_formation(forms_list)
    with open('../database/new_formations/{}.yml'.format(grp.name), 'w+') as f:
        yaml.dump(new_formation, f, default_flow_style=False)
