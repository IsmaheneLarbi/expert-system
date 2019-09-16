class Player:

    job = "professional tennis player"
    
    def __init__(self, name = "", title = "", grd_slams = "", masters = ""):
        self.name = name
        self.title = title
        self.grd_slams = grd_slams
        self.masters = masters

    def list_achievements(self):
        """"instance methods HAVE access to BOTH class and instance attributes"""
        print("I have won", self.grd_slams, "grand slams and ", self.masters)

    @classmethod
    def incommon(chkil):
        """class methods CAN access class AND instance atributes"""
        print("What we have in common is that we are all ", chkil.job)
    
    @staticmethod
    def msg(msg = "to slay"):
        """static methods DO NOT have access to class OR instance attributes,
        they are merely used to achieve a task with the parameters they receive,
        but we can use a static method from an instance OR a class"""
        print(f'I came {msg}')

roger = Player("Roger Federer", "G.O.A.T", 20, 28)
print("My name is ", roger.name, " and I am nicknamed", roger.title, "ATP masters 1000")
roger.list_achievements()

print()

rafa = Player("Rafael Nadal", "Geronimo", 19, 35)
print("My name is ", rafa.name, " and I am nicknamed", rafa.title, "ATP masters 1000")
rafa.list_achievements()

novak = Player()

print()

roger.incommon()
roger.msg()