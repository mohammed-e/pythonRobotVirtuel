from robosim import *
import networkx as nx
from math import sqrt
import time
import numpy as np


init('robot_obstacles_invisibles')



def aller(x,y):
    if(x > position(entiers=True)[0]):
        if(y > position(entiers=True)[1]):
            oriente(45);
            while(x > position(entiers=True)[0] and y > position(entiers=True)[1]):
                avance();
            if(x > position(entiers=True)[0]):
                oriente(0);
                while(x > position(entiers=True)[0]):
                    avance();
            if(y > position(entiers=True)[1]):
                oriente(90);
                while(y > position(entiers=True)[1]):
                    avance();
        elif(y < position(entiers=True)[1]):
            oriente(-45);
            while(x > position(entiers=True)[0] and y < position(entiers=True)[1]):
                avance();
            if(x > position(entiers=True)[0]):
                oriente(0);
                while(x > position(entiers=True)[0]):
                    avance();
            if(y < position(entiers=True)[1]):
                oriente(-90);
                while(y < position(entiers=True)[1]):
                    avance();
        else:
            oriente(0);
            while(x > position(entiers=True)[0]):
                avance();

    elif(x < position(entiers=True)[0]):
        if(y > position(entiers=True)[1]):
            oriente(135);
            while(x < position(entiers=True)[0] and y > position(entiers=True)[1]):
                avance();
            if(x < position(entiers=True)[0]):
                oriente(180);
                while(x < position(entiers=True)[0]):
                    avance();
            if(y > position(entiers=True)[1]):
                oriente(90);
                while(y > position(entiers=True)[1]):
                    avance();
        elif(y < position(entiers=True)[1]):
            oriente(-135);
            while(x < position(entiers=True)[0] and y < position(entiers=True)[1]):
                avance();
            if(x < position(entiers=True)[0]):
                oriente(180);
                while(x < position(entiers=True)[0]):
                    avance();
            if(y < position(entiers=True)[1]):
                oriente(-90);
                while(y < position(entiers=True)[1]):
                    avance();
        else:
            oriente(180);
            while(x < position(entiers=True)[0]):
                avance();

    else:
        if(y > position(entiers=True)[1]):
            oriente(90);
            while(y > position(entiers=True)[1]):
                avance();
        elif(y < position(entiers=True)[1]):
            oriente(-90);
            while(y < position(entiers=True)[1]):
                avance();


def create_carre(g,x,y):
     g.add_edge((x,y), (x+30,y), weight = sqrt((x+30-x)*(x+30-x) + (y-y)*(y-y)));
     g.add_edge((x,y), (x,y+30), weight = sqrt((x-x)*(x-x) + (y+30-y)*(y+30-y)));
     g.add_edge((x,y), (x+30,y+30), weight = sqrt((x+30-x)*(x+30-x) + (y+30-y)*(y+30-y)));

     g.add_edge((x,y+30), (x+30,y), weight = sqrt((x+30-x)*(x+30-x) + (y-y+30)*(y-y+30)));
     g.add_edge((x,y+30), (x+30,y+30), weight = sqrt((x+30-x)*(x+30-x) + (y+30-y+30)*(y+30-y+30)));
     g.add_edge((x+30,y), (x+30,y+30), weight = sqrt((x+30-x+30)*(x+30-x+30) + (y+30-y)*(y+30-y)));

def create_graph():
    g = nx.Graph();
    x = 80; y = 80;
    while(x < 440):
        y = 80;
        while(y < 440):
            create_carre(g,x,y);
            y = y+30;
        x = x+30;
    return g;

def draw_graph(g):
    efface();
    for (x1,y1),(x2,y2) in g.edges():
        line(x1,y1,x2,y2);

def prune_graph(g, k):
    for x in list(g.nodes()):
        if(x not in k):
            g.remove_node(x);
    return g;



def testeArete(g=None):
    # On verifie de droite a gauche
    a = 90;
    while(a >= -90):
        # Si le telemtre tire dans la meme direction que le robot (division par 0)
        if(a == 0):
            # Le robot est en diagonale
            if(orientation() == 45 or orientation() == 135 or orientation() == -135 or orientation() == -45):
                if 11+30*sqrt(2) >= telemetre(from_center=True, rel_angle=0):
                    return False;
            # Le robot est vertical ou horizontal
            else:
                if 11+30 >= telemetre(from_center=True, rel_angle=0):
                    return False;
        elif(a > 0):
		# Les autres cas en diagonale
            if(orientation() == 45 or orientation() == 135 or orientation() == -135 or orientation() == -45):
                if ((11/cos((90-a)*pi/180)) >= telemetre(from_center=True, rel_angle=a)) and (11+30*sqrt(2) >= telemetre(from_center=True, rel_angle=a)) :
                    return False;
            # Les autres cas vertical ou horizontal
            else:
                if ((11/cos((90-a)*pi/180)) >= telemetre(from_center=True, rel_angle=a)) and (11+30 >= telemetre(from_center=True, rel_angle=a)) :
                    return False;
        # a < 0
        else:
            # Les autres cas en diagonale
            if(orientation() == 45 or orientation() == 135 or orientation() == -135 or orientation() == -45):
                if ((11/cos((90+a)*pi/180)) >= telemetre(from_center=True, rel_angle=a)) and (11+30*sqrt(2) >= telemetre(from_center=True, rel_angle=a)) :
                    return False;
            # Les autres cas vertical ou horizontal
            else:
                if ((11/cos((90+a)*pi/180)) >= telemetre(from_center=True, rel_angle=a)) and (11+30 >= telemetre(from_center=True, rel_angle=a)) :
                    return False;
        a = a-1;
    return True;

# Renvoie la direction (angle en degres) ou se trouve le point (x,y) par rapport au robot
def conversion(x,y):
    rx, ry = position(entiers=True);
    if x > rx: #vers la droite
        if y == ry: #droite
            return 0;
        elif y > ry: #en bas a droite
            return 45;
        else: #en haut a droite
            return -45;
    elif x < rx: #vers la gauche
        if y == ry: #gauche
            return 180;
        elif y > ry: #en bas a gauche
            return 135;
        else: #en haut a gauche
            return -135;
    else: #vers le haut ou le bas
        if y > ry: #en bas
            return 90;
        elif y < ry: #en haut
            return -90;

def effaceLesAretesBloquees(g):
    x,y = position(entiers=True);
    for i,j in list(g.neighbors((x,y))):
        oriente(conversion(i,j));
        if not testeArete():
            g.remove_edge((i,j),(x,y));



def explore_random(g,k):
    x,y = position(entiers=True);
    voisins = list(g.neighbors((x,y)));
    voisinsNk = [];
    # On recupere les voisins non connus s'ils existent
    for i in voisins:
        if(i not in k):
            voisinsNk.append(i);
    # Si tous les voisins sont connus, le robot choisi une arete au hasard parmi toutes celles disponibles
    if(len(voisinsNk) == 0):
        l = len(voisins);
        r = np.random.randint(l);
        dx,dy = voisins[r];
        aller(dx,dy);
    # Si il y a des voisins inconnus, le choix et aleatoire parmi ceux-la
    else:
        l = len(voisinsNk);
        r = np.random.randint(l);
        dx,dy = voisinsNk[r];
        aller(dx,dy);


def explore_pluscourchemin(g, k):
    # On determine le noeud inconnu le plus proche du robot ainsi que le pcc
    minL = 100;
    pcc = [];
    for (i,j) in nx.node_connected_component(g,position(entiers=True)):
        if((i,j) not in set(k)):
            sp = nx.shortest_path(g, (position(entiers=True)[0], position(entiers=True)[1]), (i,j), weight = 'weight');
            if(len(sp) < minL):
                minL = len(sp);
                pcc = sp;
    # Le robot se rend au noeud inconnu le plus proche ou s'arrete s'il tombe sur un noeud inconnu
    for x in pcc:
        if(x not in set(k)):
            aller(x[0],x[1]);
            break;
        else:
            aller(x[0],x[1]);


def explore_ameliore(g,k):
    f = [];
    # On recupere les noeuds inconnus ayant au moins un voisin connu = noeuds frontieres
    for (i,j) in nx.node_connected_component(g,position(entiers=True)):
        if((i,j) not in set(k)):
            for (x,y) in g.neighbors((i,j)):
                if (x,y) in set(k):
                    f.append((i,j));
                    break;
    # On determine le noeud frontiere le plus proche du robot ainsi que le pcc
    minL = 100;
    pcc = [];
    for (a,b) in f:
        sp = nx.shortest_path(g, (position(entiers=True)[0], position(entiers=True)[1]), (a,b), weight = 'weight');
        if(len(sp) < minL):
            minL = len(sp);
            pcc = sp;
    # Le robot se rend au noeud frontiere le plus proche ou s'arrete s'il tombe sur un noeud inconnu (par mesure de precaution)
    for x in pcc:
        if(x not in set(k)):
            aller(x[0],x[1]);
            break;
        else:
            aller(x[0],x[1]);


def main():
    g = create_graph();
    k = [];
    # On fait en sorte que le robot soit sur un sommet du graph
    aller(80,80);
    # Mapping
    while sorted(k) != sorted(nx.node_connected_component(g,position(entiers=True))):
        if(position(entiers=True) not in k):
            effaceLesAretesBloquees(g);
            k.append(position(entiers=True));
            if sorted(k) == sorted(nx.node_connected_component(g,position(entiers=True))):
                break;
        #explore_random(g,k);
        #explore_pluscourchemin(g,k);
        explore_ameliore(g,k);

    return g;
