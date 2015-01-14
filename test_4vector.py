f = open('test_4vectors.rtf', 'r')

def lose_space(s):
    l = len(s)
    a = [-1]
    for i in range(0, l):
        if s[i] == ' ':
            a.append(i)
    a.append(l)
    n = len(a)
    b = []
    for i in range(0, n-1):
        entry = s[a[i]+1 :a[i + 1]]
        b.append(entry)
    return b


def length_file():
    f.seek(0)
    f.read()
    result =  f.tell()
    f.seek(0)
    return result

def multiple_line(n):
    for i in range(0, n):
        f.readline()


def remove_from_end(s, r):
    s = s.replace(r, '')
    return s


length = length_file()
param = f.seek(0)
set_of_events = []
set_of_p= []
while param < length:
    #print(param)
    param = f.tell()
    g = f.readline()
    if "Event" in g:
        multiple_line(2)
        h = f.readline()
        param2 = f.tell()
        if "Event" in h or "EOF" in h:
            f.seek(param)
            #Event no
            entry = lose_space(f.readline())
            set_of_events.append(int(entry[-1][0]))
            #Momenta
            for i in range(0, 2):
                entry = lose_space(f.readline().replace('\\\n', ''))
                set_of_p.append(entry)
              
len_set_e = len(set_of_events)
len_set_p = len(set_of_p)
for i in range(0,len_set_p):
    for j in range(0, len(set_of_p[i])):
        set_of_p[i][j] = float(set_of_p[i][j])


class event:
    def __init__(self,n, p):
        self.n = n
        self.p= p
    def s(self):
        q = 0
        for i in range(1, len(self.p)):
            q += self.p[i]**2
        s = self.p[0]**2 - q
        return s
events = []
k= 0
for i in range(0, len_set_e):
    for j in range(0 ,2):
        events.append(event(set_of_events[i], set_of_p[k]))
        k += 1
    
        print(set_of_events[i])
                

    
