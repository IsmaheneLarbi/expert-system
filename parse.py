import sys

def load_file(f):
    f = open(sys.argv[1], "r+")
    lines = f.readlines()
    return(lines)

def ignore_comments(lines):
    new_lines = []
    for i, line in enumerate(lines):
        if (lines[i][0] != "#"):
            new_lines.append(line[0:line.find("#")])
    return new_lines

def expert_system():
    if (len(sys.argv) != 2):
        return (1)
    lines = load_file(sys.argv[1])
    new_lines = ignore_comments(lines)
    for i, line in enumerate(new_lines):
        print("[", i, "]",  line)

if __name__ == "__main__" :
    expert_system()