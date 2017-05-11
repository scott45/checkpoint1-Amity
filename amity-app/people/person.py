__author__ = 'scotty'


class Person(object):
    def __init__(self, f_name, l_name, person_label):
        self.f_name = f_name.strip().title()
        self.l_name = l_name.strip().title()
        self.person_lable = person_label.strip().title()
        self.accomodate = 'N'

    def get_all_names(self):
        all_names = self.f_name + ' ' + self.l_name
        self.all_names = all_names

    def assign_qualifier(self, qualifier):
        self.qualifier = qualifier
