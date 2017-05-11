__author__ = 'scotty'

class Person():

    def __init__(self, f_name, l_name, person_lable):
        self.f_name = f_name.strip().title()
        self.l_name = l_name.strip().title()
        self.person_lable = person_lable.strip().title()
        self.accomodate = 'N'

        
