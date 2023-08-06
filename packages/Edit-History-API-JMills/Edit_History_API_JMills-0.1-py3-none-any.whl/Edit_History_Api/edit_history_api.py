"""
    Edits classes & helpers
    ~~~~~~~~~~~~~~~~~~~~~~
"""
import os
import json


class EditManager(object):
    """A very simple edit Manager, that saves it's data as json."""
    def __init__(self, path):
        self.file = os.path.join(path, 'edits.json')

    def read(self):
        if not os.path.exists(self.file):
            return {}
        with open(self.file) as f:
            data = json.loads(f.read())
        return data

    def write(self, data):
        with open(self.file, 'w') as f:
            f.write(json.dumps(data, indent=2))

    def add_edit(self, date_time, page, user):
        edits = self.read()
        if edits.get(date_time):
            return False
        new_edit = {
            'page': page,
            'user': user
        }
        edits[date_time] = new_edit
        self.write(edits)
        edit_data = edits.get(date_time)
        return Edit(self, date_time, edit_data)

    def get_edit(self, date_time):
        edits = self.read()
        edit_data = edits.get(date_time)
        if not edit_data:
            return None
        return Edit(self, date_time, edit_data)

    def get_edit_list(self):
        edits = self.read()
        edit_list = list()
        for edit in edits:
            edit_list.add(str(edit.data_time) + ", " + str(edit.data))
        return edit_list


class Edit(object):
    def __init__(self, manager, date_time, data):
        self.manager = manager
        self.date_time = date_time
        self.data = data

    def get(self, option):
        return self.data.get(option)

    def set(self, option, value):
        self.data[option] = value
        self.save()

    def save(self):
        self.manager.update(self.name, self.data)

    def get_date_time(self):
        return self.date_time
