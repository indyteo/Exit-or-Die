######################################
# Rappel concernant les cases :      #
#                                    #
# Dec  Bin     Connexions            #
#      ENWS                          #
# 0  : 0000 => Empty                 #
# 1  : 0001 => South                 #
# 2  : 0010 => West                  #
# 3  : 0011 => South-West            #
# 4  : 0100 => North                 #
# 5  : 0101 => North-South           #
# 6  : 0110 => North-West            #
# 7  : 0111 => North-West-South      #
# 8  : 1000 => East                  #
# 9  : 1001 => East-South            #
# 10 : 1010 => East-West             #
# 11 : 1011 => East-West-South       #
# 12 : 1100 => East-North            #
# 13 : 1101 => East-North-South      #
# 14 : 1110 => East-North-West       #
# 15 : 1111 => East-North-West-South #
#                                    #
######################################

import pickle as pi
from random import choice

# Vérification de la présence du module "PyGame" et importation le cas échéant.
try:
	import pygame as pg
	pg.init()
except ModuleNotFoundError:
	print("Erreur : Vous ne disposez pas du module \"PyGame\".")
	exit()

def str_set(Str, Index, Char):
	Str = list(Str)
	Str[Index] = Char
	return "".join([str(s) for s in Str])

def actualiser(case):
	root.blit(pieces[cases[case]], ((case[0] - 1) * 64, (case[1] - 1) * 64))
	pg.display.flip()

def has_near_ok(Case):
	W = (Case[0] - 1, Case[1])
	E = (Case[0] + 1, Case[1])
	N = (Case[0], Case[1] - 1)
	S = (Case[0], Case[1] + 1)
	near = [W, E, N, S]
	near_ok = []
	for case in near:
		if case in remainings:
			near_ok.append(case)
	return near_ok != []

e = 0
n = 1
w = 2
s = 3

nom = input("Nom : ")
dim = (int(input("Dimensions :\n - Colonnes : ")), int(input(" - Lignes : ")))
cases = {}

gen = input("Génération aléatoire (a) ou à la main (m) ? ")

if gen == "a":
	print("\nClic gauche sur une case pour définir le départ.\nClic droit pour définir l'arrivée.\nEntrer pour valider.\nEchap pour annuler.")
	root = pg.display.set_mode((dim[0] * 64, dim[1] * 64))
	pieces = {"Perso": pg.image.load("images/Perso.gif").convert_alpha(), "0000": pg.image.load("images/0.gif").convert(), "0001": pg.image.load("images/1.gif").convert(), "0010": pg.image.load("images/2.gif").convert(), "0011": pg.image.load("images/3.gif").convert(), "0100": pg.image.load("images/4.gif").convert(), "0101": pg.image.load("images/5.gif").convert(), "0110": pg.image.load("images/6.gif").convert(), "0111": pg.image.load("images/7.gif").convert(), "1000": pg.image.load("images/8.gif").convert(), "1001": pg.image.load("images/9.gif").convert(), "1010": pg.image.load("images/10.gif").convert(), "1011": pg.image.load("images/11.gif").convert(), "1100": pg.image.load("images/12.gif").convert(), "1101": pg.image.load("images/13.gif").convert(), "1110": pg.image.load("images/14.gif").convert(), "1111": pg.image.load("images/15.gif").convert()}
	
	pg.display.set_caption(nom)
	for C in range(dim[0]):
		for L in range(dim[1]):
			cases[(C + 1, L + 1)] = "0000"
			root.blit(pieces["0000"], (C * 64, L * 64))
	pg.display.flip()
	
	end = False
	while not(end):
		for event in pg.event.get():
			if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
				exit()
			if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
				end = True
			if event.type == pg.MOUSEBUTTONDOWN:
				case = (event.pos[0] // 64 + 1, event.pos[1] // 64 + 1)
				if event.button == 1:
					if case[0] == 1 or case[0] == dim[0] or case[1] == 1 or case[1] == dim[1]:
						start = case
						print("Départ défini en {case}.".format(case = case))
					else:
						print("Position incorrecte : Le départ doit être une case adjacente au bord du plateau.")
				elif event.button == 3:
					if case[0] == 1 or case[0] == dim[0] or case[1] == 1 or case[1] == dim[1]:
						exit_ = case
						print("Arrivée définie en {case}.".format(case = case))
					else:
						print("Position incorrecte : L'arrivée doit être une case adjacente au bord du plateau.")
	
	current = start
	remainings = [c for c in cases.keys()]
	remainings.remove(current)
	cases_ok = [current]
	
	while remainings != []:
		W = (current[0] - 1, current[1])
		E = (current[0] + 1, current[1])
		N = (current[0], current[1] - 1)
		S = (current[0], current[1] + 1)
		nears = [W, E, N, S]
		near_ok = []
		for case in nears:
			if case in remainings:
				near_ok.append(case)
		
		if near_ok != []:
			next = choice(near_ok)
			if next == W:
				cases[current] = str_set(cases[current], w, 1)
				cases[next] = str_set(cases[next], e, 1)
			elif next == E:
				cases[current] = str_set(cases[current], e, 1)
				cases[next] = str_set(cases[next], w, 1)
			elif next == N:
				cases[current] = str_set(cases[current], n, 1)
				cases[next] = str_set(cases[next], s, 1)
			elif next == S:
				cases[current] = str_set(cases[current], s, 1)
				cases[next] = str_set(cases[next], n, 1)
			
			actualiser(current)
			actualiser(next)
			current = next
			if current in remainings:
				remainings.remove(current)
			if current not in cases_ok:
				cases_ok.append(current)
		
		else:
			ok = False
			for near in nears:
				if has_near_ok(near):
					while not(ok):
						test = choice(nears)
						if has_near_ok(test):
							current = test
							ok = True
					break
			if not(ok):
				current = cases_ok.pop()
		
	for hole in [start, exit_]:
		if hole[0] == 1:
			cases[hole] = str_set(cases[hole], w, 1)
		elif hole[0] == dim[0]:
			cases[hole] = str_set(cases[hole], e, 1)
		elif hole[1] == 1:
			cases[hole] = str_set(cases[hole], n, 1)
		elif hole[1] == dim[1]:
			cases[hole] = str_set(cases[hole], s, 1)
		actualiser(hole)
	
	print("Entrer pour valider.\nEchap pour annuler.")
	end = False
	while not(end):
		for event in pg.event.get():
			if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
				exit()
			if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
				end = True
	
	pg.quit()

elif gen == "m":
	print("\nClic gauche sur une case pour changer la piece.\nClic droit pour définir le départ.\nClic molette pour définir l'arrivée.\nEntrer pour valider.\nEchap pour annuler.")
	root = pg.display.set_mode((dim[0] * 64, dim[1] * 64))
	pieces = {"Perso": pg.image.load("images/Perso.gif").convert_alpha(), "0000": pg.image.load("images/0.gif").convert(), "0001": pg.image.load("images/1.gif").convert(), "0010": pg.image.load("images/2.gif").convert(), "0011": pg.image.load("images/3.gif").convert(), "0100": pg.image.load("images/4.gif").convert(), "0101": pg.image.load("images/5.gif").convert(), "0110": pg.image.load("images/6.gif").convert(), "0111": pg.image.load("images/7.gif").convert(), "1000": pg.image.load("images/8.gif").convert(), "1001": pg.image.load("images/9.gif").convert(), "1010": pg.image.load("images/10.gif").convert(), "1011": pg.image.load("images/11.gif").convert(), "1100": pg.image.load("images/12.gif").convert(), "1101": pg.image.load("images/13.gif").convert(), "1110": pg.image.load("images/14.gif").convert(), "1111": pg.image.load("images/15.gif").convert()}
	
	pg.display.set_caption(nom)
	for C in range(dim[0]):
		for L in range(dim[1]):
			cases[(C + 1, L + 1)] = "0000"
			root.blit(pieces["0000"], (C * 64, L * 64))
	pg.display.flip()
	
	end = False
	while not(end):
		for event in pg.event.get():
			if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
				exit()
			if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
				end = True
			if event.type == pg.MOUSEBUTTONDOWN:
				case = (event.pos[0] // 64 + 1, event.pos[1] // 64 + 1)
				if event.button == 1:
					if cases[case] == "1111":
						cases[case] = "0000"
					else:
						cases[case] = format(int(cases[case], 2) + 1, "04b")
					root.blit(pieces[cases[case]], (case[0] * 64 - 64, case[1] * 64 - 64))
					pg.display.flip()
				elif event.button == 3:
					if case[0] == 1 or case[0] == dim[0] or case[1] == 1 or case[1] == dim[1]:
						start = case
						print("Départ défini en {case}.".format(case = case))
					else:
						print("Position incorrecte : Le départ doit être une case adjacente au bord du plateau.")
				elif event.button == 2:
					if case[0] == 1 or case[0] == dim[0] or case[1] == 1 or case[1] == dim[1]:
						exit_ = case
						print("Arrivée définie en {case}.".format(case = case))
					else:
						print("Position incorrecte : L'arrivée doit être une case adjacente au bord du plateau.")
	
	pg.quit()

else:
	print("Vous ne savez pas lire ou écrire (voire même les deux ! :c)...")
	exit()

niveau = {"nom": nom, "dim": dim, "cases": cases, "start": start, "exit": exit_}
try:
	with open("Niveaux/{nom}".format(nom = nom), "wb") as data:
		pi.Pickler(data).dump(niveau)
except FileNotFoundError:
	open("Niveaux/{nom}".format(nom = nom), "w").close()
	with open("Niveaux/{nom}".format(nom = nom), "wb") as data:
		pi.Pickler(data).dump(niveau)
print("Niveau créé !")

input()