
res=18   #symulacja odbywa się na kawadracie o boku długości res
         #simulation runs on the square of size res by res
size=15  #size określa ile na ile pikseli ma komórka
         #cell is size by size square of pixels
leng=120 #określa długość symulacji
         #leng is lenght of simulation (amount of frames)
sta='noise'

#sta określa stan początkowy:
#sta='noise' generuje szum
#sta='turtle' generuje żółwia
#sta='copperhead' generuje miedzianą głowę
#sta='eight' generuje ósemkę
#sta=n dla liczby naturalnej n generuje "odcinek" długości n
#sta defines initial state:
#sta='noise' generates noise
#sta='turtle' generates turtle
#sta='copperhead' generates copperhead
#sta='eight' generates figure eight
#sta=n for natural number n generates "segment" of lenght n

#https://conwaylife.com/wiki/Turtle
#https://conwaylife.com/wiki/Copperhead
#https://conwaylife.com/wiki/Figure_eight

#oczywiście łatwo można wbudować więcej ciekawych stanów początkowych
#ofc more initial states may be inbuilt easily

from imageio.v2 import imread,mimsave
from PIL.Image import fromarray 
from numpy import array,uint8
from random import randint
from math import floor,ceil

##############################################################################

#tworzymy sobie funkcję przerzucającą jeden stan w kolejny
#we make a function calculating new state of a cell

#określamy sąsiedztwo
#we define neighbourhood
NEI=[[i,j] for i in [-1,0,1] for j in [-1,0,1]]
NEI.pop(4)

def ev(y):
    if y==1:
        return 1
    else:
        return 0

#określamy funkcję rzucającą stan komórki i sąsiedztwa w stan komórki w następnej klatce symulacji
#we define a function taking state of cell and it's neigbourhood, giving state of cell in next frame as an output
def it(M,i,j):
    if M[i][j]==2:
        return 2
    else:
        ż=sum([ev(M[i+k[0]][j+k[1]]) for k in NEI])
        if (M[i][j]==1) and ((ż==2) or (ż==3)):
            return 1
        elif (M[i][j]==0) and (ż==3):
            return 1
        else:
            return 0

#określamy funkcję rzucającą jedną klatkę symulacji w kolejną
#we define a function turning frame to a next one
def ite(M):
    return [[it(M,i,j) for j in range(res)] for i in range(res)]

##############################################################################

#tu zajmujemy się częścią graficzną
#here we're becoming to deal with graphic stuff

#określamy funkcję rzucającą stan komórki w kolor w RGB
#we define a function converting state of cell to color in RGB format
def fRGB(n):
    if n==0:
        return [0,0,0];
    if n==1:
        return [184,174,0] #yellow good
    if n==2:
        return [255,255,255]

#określamy funkcję przetwarzającą listę list stanów na array [R,G,B]ów
#we define a function converting list of lists of states to array of [R,G,B]s
def arrayRGB(L):
    return array([array(list(map(fRGB,L[i]))) for i in range(len(L))],dtype=uint8)

##############################################################################

#tu tworzymy funkcję przeskalowującą (funkcje wbudowane w PIL rozmazują obraz)
#we define a function making image bigger (inbuilt PIL's functions blurs image)
def rescale(M):
    return [[M[floor(i/size)][floor(j/size)] for j in range(res*size)] for i in range(res*size)]

#tu tworzymy funkcję rzucającą stan początkowy w listę przeskalowanych klatek
#we define a function that makes a list of rescaled frames out from initial state
def gra(M):
    K=[M]
    for i in range(leng):
        K.append(ite(K[-1]))
    return [rescale(k) for k in K]

#tu tworzymy funkcję przerabiającą powyższą listę na listę grafik, pamiętając ich nazwy
#we define a function converting above list to list of graphics, remembering each's name
names=[]
def graf(K):
    for i in range(len(K)):
        names.append('sym'+str(i)+'.png')
        fromarray(arrayRGB(K[i]),'RGB').save('sym'+str(i)+'.png')

#tu tworzymy funkcję przerabiającą listę grafik na .gif
#we define a function converting list of graphics to .gif file
def gif(L):
    mimsave('movie.gif',[imread(l) for l in L])

#powyższa metoda zapewne jest dość nieoptymalna:
#pierwotnie próbowałem zrobić tak, by grafiki były podawane bezpośrednio do mimsave,
#a nie były zapisywane wszystkie "na zewnątrz"
#probably above method isn't optimal:
#firstly I tried to upload graphics directly to mimsave
#instead of being stored somewhere "outside"

##############################################################################

#tworzymy sobie miejsce akcji
#we create a place of action

#funkcja tworząca przestrzeń na symulację oraz ramkę ograniczającą
#0 oznacza nieżywą komórkę, 1 żywą, 2 oznacza ramkę
#function creating space for simulation and a border
#0 means dead cell, 1 means living one, 2 means border cell
def ram(i,j):
    if i*j*(i-res+1)*(j-res+1)==0:
        return 2
    else:
        return 0

M=[[ram(i,j) for j in range(res)] for i in range(res)]

#wstawiamy coś ciekawego
#we insert something nice

if sta=='noise':
    for i in range(1,res-1):
        for j in range(1,res-1):
            M[i][j]=randint(0,1)

T=[[1,1,0,0,0,0,0,0,1,1],
   [0,1,1,1,1,1,1,1,1,0],
   [0,0,0,0,0,0,0,0,0,0],
   [0,1,0,0,0,0,0,0,1,0],
   [0,1,0,0,0,0,0,0,1,0],
   [0,0,0,1,0,0,1,0,0,0],
   [0,1,1,0,1,1,0,1,1,0],
   [0,0,1,1,0,0,1,1,0,0],
   [1,0,1,0,0,0,0,1,0,1],
   [1,1,0,0,0,0,0,0,1,1],
   [1,1,0,1,0,0,1,0,1,1],
   [0,0,0,0,1,1,0,0,0,0]]

if sta=='turtle':
    for i in range(12):
        for j in range(10):
            M[i+2][j+ceil(res/2-5)]=T[i][j]
  
C=[[0,0,0,1,1,0,0,0],
   [0,0,0,1,1,0,0,0],
   [0,0,0,0,0,0,0,0],
   [0,0,1,1,1,1,0,0],
   [0,1,1,0,0,1,1,0],
   [1,0,0,0,0,0,0,1],
   [0,0,0,0,0,0,0,0],
   [1,0,0,0,0,0,0,1],
   [1,0,1,0,0,1,0,1],
   [0,0,0,1,1,0,0,0],
   [0,0,0,1,1,0,0,0],
   [0,1,1,0,0,1,1,0]]

if sta=='copperhead':
    for i in range(12):
        for j in range(8):
            M[i+2][j+ceil(res/2-4)]=C[i][j]

E=[[0,0,0,1,1,1],
   [0,0,0,1,1,1],
   [0,0,0,1,1,1],
   [1,1,1,0,0,0],
   [1,1,1,0,0,0],
   [1,1,1,0,0,0]]

if sta=='eight':
    for i in range(6):
        for j in range(6):
            M[i+ceil(res/2-3)][j+ceil(res/2-3)]=E[i][j]
 
if type(sta)==int:
    for i in range(sta):
        M[ceil(res/2)][ceil((res-sta)/2)+i]=1

##############################################################################

#wywołujemy wszystko
#we call everything

graf(gra(M))
gif(names)

##############################################################################
