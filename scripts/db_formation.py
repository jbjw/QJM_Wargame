from collections import Counter
# future work I want to do here is to combine the formation_group and 
# formation objects such that any formation can have sub-formations

# generic formation class
class formation():
    def __init__(self, name, equipment, personnel):
        self.name = name
        self.equipment = equipment
        self.personnel = personnel

    def __repr__(self):
        return 'formation({} @{:,.0f})'.format(self.name, self.OLI)

    def GenOLI(self, equipment_list):
        self.OLI = 0
        for equip, qty in self.equipment.items():
            try:
                equip_entry = equipment_list.equip_by_name(equip)
                equip_TLI = equip_entry.TLI
            except BaseException:
                #print('No equipment entry for {}\n'.format(equip))
                equip_TLI = 0
                pass
            self.OLI += qty * equip_TLI

            
# class that allows a list of formations to be searched
class formation_list():
    def __init__(self, formations):
        self.names = list()
        self.forms = list()
        for form in formations:
            self.names.append(form.name)
            self.forms.append(form)

    def formation_by_name(self, name_to_find):
        return self.forms[self.names.index(name_to_find)]

    def __repr__(self):
        return 'formation_list({})'.format(self.names)

        
# class that allows formations to be combined
class formation_group():
    def __init__(self, name, formations):
        self.name = name
        self.formations = formations

    def __repr__(self):
        return 'formation_group({})'.format(self.name)

    def generate_formation(self, form_list):
        # creates a formation from the group definition
        # run through the list of formations
        equipment = dict()
        personnel = 0
        for name in self.formations:
            form = form_list.formation_by_name(name)
            equipment = Counter(equipment) + Counter(form.equipment)
            personnel += form.personnel
        new_formation = formation(self.name, dict(equipment), personnel)
        return new_formation