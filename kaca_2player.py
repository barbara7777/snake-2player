import tkinter as tk
import time
from random import randint

# izbira velikosti in barv
sirina, visina = 26, 26
premer = 16
barvaGlave1 = '#f58307'
barvaTelesa1 = '#d68542'
barvaGlave2 = '#769956'
barvaTelesa2 = '#b1e647'
hitrost = 100


width = (sirina+1)*premer
height = (visina+1)*premer

glava1 = [sirina//2, visina//2]
glava2 = [sirina//2, visina//2-2]
polje = [[0 for _ in range(sirina)] for _ in range(visina)]
jabka = []

polje[glava1[0]][glava1[1]] = 1
polje[glava1[0]-1][glava1[1]] = 1
polje[glava1[0]-2][glava1[1]] = 1

polje[glava2[0]][glava2[1]] = 1
polje[glava2[0]-1][glava2[1]] = 1
polje[glava2[0]-2][glava2[1]] = 1


class Kaca:
    def __init__(self, glava, ime):
        self.ime = ime
        self.glava = glava
        self.rep = [[glava[0]-2, glava[1]], [glava[0]-1, glava[1]]]
        self.smer = [0, 0]
        self.ziva = True
    

def narisi_jabolko():
    global jabka
    one = tk.PhotoImage(file=r'japka.png')
    root.one = one
    if jabka:
        x, y = jabka
        x = premer * x + premer/2
        y = premer * y + premer/2
        canvas.create_image(x-2, y-4, image=one, anchor=tk.NW)
    else:
        x = randint(0, sirina-1)
        y = randint(0, visina-1)
        if polje[x][y] == 0:
            polje[x][y] = 3
            jabka = [x, y]
            x = premer/2 + premer*x
            y = premer/2 + premer*y
            canvas.create_image(x-2, y-4, image=one, anchor=tk.NW)
        else:    
            narisi_jabolko()


def narisiRob(canvas):
    canvas.create_rectangle(premer/2, premer/2, width-premer/2, height-premer/2, fill='white', outline="")


def narisi(canvas):
    global kaca1, kaca2
    canvas.delete("all")
    narisiRob(canvas)
    narisi_jabolko()

    x1, y1 = kaca1.glava
    x2, y2 = kaca2.glava
    x1 = premer/2 + premer*x1
    x2 = premer/2 + premer*x2
    y1 = premer/2 + premer*y1
    y2 = premer/2 + premer*y2
    canvas.create_oval(x1, y1, x1+premer, y1+premer , fill=barvaGlave1)
    canvas.create_oval(x2, y2, x2+premer, y2+premer , fill=barvaGlave2)
    for k in kaca1.rep:
        xt, yt = k
        xt = premer/2 + premer*xt
        yt = premer/2 + premer*yt
        canvas.create_oval(xt, yt, xt+premer, yt+premer , fill=barvaTelesa1)
    for k in kaca2.rep:
        xt, yt = k
        xt = premer/2 + premer*xt
        yt = premer/2 + premer*yt
        canvas.create_oval(xt, yt, xt+premer, yt+premer , fill=barvaTelesa2)



def novaIgra():
    global kaca1, kaca2, polje, jabka
    glava1 = [sirina//2, visina//2]
    glava2 = [sirina//2, visina//2-2]
    kaca1 = Kaca(glava1, 1)
    kaca2 = Kaca(glava2, 2)
    kaca1.ziva = True
    kaca2.ziva = True
    polje = [[0 for _ in range(sirina)] for _ in range(visina)]
    jabka = []
    
    polje[glava1[0]][glava1[1]] = 1
    polje[glava1[0]-1][glava1[1]] = 1
    polje[glava1[0]-2][glava1[1]] = 1

    polje[glava2[0]][glava2[1]] = 1
    polje[glava2[0]-1][glava2[1]] = 1
    polje[glava2[0]-2][glava2[1]] = 1
    
    narisi(canvas)
    tocke1.configure(text='ORANZNA kaca : 0')
    tocke2.configure(text='ZELENA kaca : 0')
    frame()


def frame():
    global kaca1, kaca2
    global root
    premakni(kaca1, None)
    premakni(kaca2, None)
    if kaca1.ziva and kaca2.ziva:
        root.after(hitrost, frame)


def premakni(kaca, event):
    if not kaca.ziva:
        return
    if sum(kaca.smer) == 0:
        return
    x0, y0 = kaca.glava
    novo = [x0 + kaca.smer[0], y0 - kaca.smer[1]]
    # pogoji
    if kaca.rep[-1] == novo:
        kaca.smer = [-x for x in kaca.smer]
        return
    if (novo[0]>=sirina or novo[0]<0 or novo[1]>=visina or novo[1]<0):
        print("zabil si se v rob")
        umri(kaca)
        return
    if polje[novo[0]][novo[1]] == 1:
        print("zabil si se sam vase")
        umri(kaca)
        return

    kaca.rep.append(kaca.glava)
    polje[x0][y0] = 1
    kaca.glava = novo
    
    semPojedlaJabko(kaca)

    polje[x0 + kaca.smer[0]][y0 - kaca.smer[1]] = 2 
    xz, yz = kaca.rep[0]
    polje[xz][yz] = 0
    del kaca.rep[0]
    narisi(canvas)


def umri(kaca):
    kaca.ziva = False
    

def semPojedlaJabko(kaca):
    global jabka
    if kaca.glava == jabka:
        jabka = []
        kaca.rep = [kaca.rep[0]] + kaca.rep
        if kaca.ime == 1:
            tocke1.configure(text='ORANZNA kaca: {}'.format(len(kaca.rep)-3))
        else:
            tocke2.configure(text='ZELENA kaca : {}'.format(len(kaca.rep)-3))


def levo1(event):
    global kaca1
    kaca1.smer = (-1,0)
def levo2(event):
    global kaca2
    kaca2.smer = (-1,0)
def desno1(event):
    global kaca1
    kaca1.smer = (1,0)
def desno2(event):
    global kaca2
    kaca2.smer = (1,0)
def gor1(event):
    global kaca1
    kaca1.smer = (0,1)
def gor2(event):
    global kaca2
    kaca2.smer = (0,1)
def dol1(event):
    global kaca1
    kaca1.smer = (0,-1)
def dol2(event):
    global kaca2
    kaca2.smer = (0,-1)


root = tk.Tk()
canvas = tk.Canvas(root, width=width, height=height, borderwidth=0, highlightthickness=0, bg="#2c9c3c")
canvas.grid(column=0, row=0)
tipke = tk.Frame(root, width=width/2, height=40, borderwidth=0, relief=tk.RAISED)
tipke.grid(column=0, row=1, sticky=tk.W)

tipke2 = tk.Frame(root, width=width/2, height=40, borderwidth=0, relief=tk.RAISED)
tipke2.grid(column=0, row=1, sticky=tk.E)

novaIgra = tk.Button(tipke2, text="Nova igra", command=novaIgra, borderwidth=2, relief='groove', bg='white')
novaIgra.pack(side=tk.RIGHT, padx=8, pady=5)
tocke1 = tk.Label(tipke, text='ORANZNA kaca: ')
tocke2 = tk.Label(tipke, text='ZELENA kaca: ')
tocke1.pack(side=tk.RIGHT, fill='x', padx=8)
tocke2.pack(side=tk.LEFT, fill='x', padx=8)


# zdruzimo tipke in funkcije
root.bind('w', gor1)
root.bind('<Up>', gor2)
root.bind('d', desno1)
root.bind('<Right>', desno2)
root.bind('a', levo1)
root.bind('<Left>', levo2)
root.bind('s', dol1)
root.bind('<Down>', dol2)


kaca1 = Kaca(glava1, 1)
kaca2 = Kaca(glava2, 2)
narisi(canvas)
frame()


root.wm_title("Kača klopotača")
root.mainloop()
