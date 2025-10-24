import random
import networkx as nx
from copy import deepcopy

matrice_essai = [[1,0,1,1,0],
                 [0,1,0,1,0],
                 [1,0,0,1,1],
                 [1,1,0,0,0]]

# Fonction qui génère 2 entier aléatoire différents entre 0 et n-1 (afin de pouvoir choisir 2 lignes aléatoire de la matrice pour le trade)
def generate_2(n):
    x=random.randint(0,n-1)
    y=random.randint(0,n-1)
    while y==x: 
        y=random.randint(0,n-1)

    return x,y

# Fonction qui va retourner les listes des index des éléments des 2 listes sur lequels ils n'ont pas de d'occurences de 1 en commum 
# + la liste des index pour lequel ils ont un élément en commum
# On suppose que les 2 listes ont la même taille 
def no_equal(l1,l2,verbose=False): 
    res1=[]
    res2=[]
    taille=len(l1)
    for i in range(0,taille):
        if l1[i]==1:
            if l2[i]!=1:
                res1.append(i)
        if l2[i]==1:
            if l1[i]!=1:
                res2.append(i)
    if(verbose):
        print("l1 vaut "+str(l1))
        print("l2 vaut "+str(l2))
        print("--------")
        print("res1 vaut "+str(res1))
        print("res2 vaut "+str(res2))
    return res1,res2

def no_link(l1,l2,x,y):
    res1=[]
    res2=[]
    taille=len(l1)
    for i in range(0,taille):
        if l1[i]==1:
            if i!=y :
                res1.append(i)
        if l2[i]==1:
            if i!=x:
                res2.append(i)
    return res1,res2

# Algo des trades ou curveball dans la doc
#On suppose que M contient au moins une liste pour son premier élément
def curveball(M):
    res=M
    taille_ligne=len(res)
    #Etape 1 : obtenir 2 listes aléatoires dans la matrice 
    l1=[]
    l2=[]
    while len(l1)==0 or len(l2)==0:
        i_1,i_2=generate_2(taille_ligne)
        l1=M[i_1]
        l2=M[i_2]
    #Etape 2 : on prive de ces 2 listes les occurrences d'index qui donnent tout les 2 un élément différent de 0 dans les listes
    L1,L2=no_equal(l1,l2,False)
    # Si L1 ou L2 sont vides, on ne peut pas faire d'échange
    if len(L1) == 0 or len(L2) == 0:
        return res
    #Etape 3 : on échange un élément d'une des listes obtenus dans l'étape 2 
    x=random.randint(0,len(L1)-1)
    y=random.randint(0,len(L2)-1)
    print("valeur de L1 qui va être échangé : "+str(L1[x]), 'i_1 = ', i_1)
    print("valeur de L2 qui va être échangé : "+str(L2[y]), 'i_2 = ', i_2)
    del1=L1[x] #ancienne valeur qui va devoir être mis à 0 lors de la mise à jour de la liste 
    del2=L2[y] #same
    #échange
    tmp=L2[y]
    L2[y]=L1[x]
    L1[x]=tmp
    #changement sur la matrice principal
    l1[del1]=0
    l2[del2]=0
    l1[L1[x]]=1
    l2[L2[y]]=1
    res[i_1]=l1
    res[i_2]=l2
    return res 

#Algorithme des trades sur 1 itération 
def iterate_trades(M,verbose=False): # renvoie false si le trading a échoué, true sinon 
    res=M
    taille_ligne=len(res)
    #Etape 1 : obtenir 2 listes aléatoires dans la matrice 
    l1=[]
    l2=[]
    while len(l1)==0 or len(l2)==0:
        i_1,i_2=generate_2(taille_ligne)
        l1=M[i_1]
        l2=M[i_2]
    #On enlève le potentiel lien direct entre les 2 points du graphe 
    L1,L2=no_link(l1,l2,i_1,i_2)
    # Si L1 ou L2 sont vides, on ne peut pas faire d'échange
    if len(L1) == 0 or len(L2) == 0:
        return res,False
    numb_trades=min(len(L1),len(L2))
    for i in range(numb_trades):
        x=random.randint(0,len(L1)-1)
        y=random.randint(0,len(L2)-1)
        if(verbose):
            print("valeur de L1 qui va être échangé : "+str(L1[x]), 'i_1 = ', i_1)
            print("valeur de L2 qui va être échangé : "+str(L2[y]), 'i_2 = ', i_2)
        del1=L1[x] #ancienne valeur qui va devoir être mis à 0 lors de la mise à jour de la liste 
        del2=L2[y] #same
        #échange
        tmp=L2[y]
        L2[y]=L1[x]
        L1[x]=tmp
        #changement sur la matrice principal
        l1[del1]=0
        l2[del2]=0
        l1[L1[x]]=1
        l2[L2[y]]=1
        res[i_1]=l1
        res[i_2]=l2
    
    return res,True

def trades_randomization(G, num_trials=1000, copy_graph=True, verbose=False):

    if copy_graph:
        G = deepcopy(G)

    M=nx.to_numpy_array(G)
    n_trades = 0
    trades_log = []

    for _ in range(num_trials):
      M,has_echange=iterate_trades(M,verbose)
      if(has_echange):
          n_trades+=1


    return nx.from_numpy_array(M)
    

