class switch():
    def __init__(self,**kwargs):
        self.something = kwargs['something']
    def get_interfaces(self):
        print("p")

class sub_switch(switch):
    def __init__(self,**kwargs):
        self.something_else = kwargs['something_else']

