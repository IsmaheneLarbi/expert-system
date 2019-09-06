import sys

def expert_system():
    if (len(sys.argv) != 2):
        return (1)
    f = open(sys.argv[1], "r+")
    lines = f.readlines()
    for line in lines:
        if (line[0] != "#"):
            print(line[0:line.find('#')])
if __name__ == "__main__" :
    expert_system()