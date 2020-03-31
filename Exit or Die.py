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
from os import listdir

# Vérification de la présence du module "PyGame" et importation le cas échéant.
try:
	import pygame as pg
	pg.init()
except ModuleNotFoundError:
	print("Erreur : Vous ne disposez pas du module \"PyGame\".")
	exit()

class Plateau:
	"""
	Gère l'affichage du niveau et du joueur sur le plateau.
	
	Options :
	- root = Fenêtre contenant le plateau (Surface) ;
	- niveau = Niveau à afficher sur le plateau (Niveau).
	"""
	def __init__(self, root, niveau):
		"""
		Initialisation des variables et affichage de départ.
		"""
		# Variables
		self.root = root
		self.niveau = niveau
		
		# Affichage initial niveau et joueur
		pg.display.set_caption(self.niveau.nom)
		for C in range(self.niveau.dim[0]):
			for L in range(self.niveau.dim[1]):
				self.root.blit(pieces[self.niveau.cases[(C+1, L+1)]], (C * 64, L * 64))
		self.root.blit(pieces["Perso"], (self.niveau.start[0] * 64 - 36, self.niveau.start[1] * 64 - 36))
		
		pg.display.flip()

	def actualiser(self):
		"""
		Actualise le plateau à chaque déplacement du joueur.
		"""
		self.root.blit(pieces[self.niveau.cases[self.niveau.old]], ((self.niveau.old[0] - 1) * 64, (self.niveau.old[1] - 1) * 64))
		self.root.blit(pieces["Perso"], (self.niveau.current[0] * 64 - 36, self.niveau.current[1] * 64 - 36))
		pg.display.flip()

class Niveau:
	"""
	Contient l'intégralité des données du niveau.
	
	Options :
	- nom = Nom du niveau (str) ;
	- dim = Dimensions du niveau Colonnes x Lignes (Tuple) ;
	- cases = Emplacement des pièces (Dictionnaire) ;
	- start = Case de départ (Tuple) ;
	- exit = Case d'arrivée (Tuple).
	"""
	def __init__(self, nom, dim, cases, start, exit):
		self.nom = nom
		self.dim = dim
		self.cases = cases
		self.start = start
		self.exit = exit
		self.current = list(self.start)
		self.old = self.start
	
	def __str__(self):
		return "====================\nNiveau : {nom}\nDimensions : {dim}\nCases : {cases}\nDépart : {start}\nArrivée : {exit}\n====================".format(nom = self.nom, dim = "{c}x{l}".format(c = self.dim[0], l = self.dim[1]), cases = self.cases, start = self.start, exit = self.exit)

e = 0
n = 1
w = 2
s = 3

# Choix et récupération des données du niveau :

print("Liste des niveaux :")
for save in listdir("Niveaux"):
	print(save)
nom = input("\nNom : ")
with open("Niveaux/{nom}".format(nom = nom), "rb") as data:
	level_data = pi.Unpickler(data).load()
niveau = Niveau(**level_data)
print(niveau)

root = pg.display.set_mode((niveau.dim[0] * 64, niveau.dim[1] * 64))
pieces = {"Perso": pg.image.load("images/Perso.gif").convert_alpha(), "0000": pg.image.load("images/0.gif").convert(), "0001": pg.image.load("images/1.gif").convert(), "0010": pg.image.load("images/2.gif").convert(), "0011": pg.image.load("images/3.gif").convert(), "0100": pg.image.load("images/4.gif").convert(), "0101": pg.image.load("images/5.gif").convert(), "0110": pg.image.load("images/6.gif").convert(), "0111": pg.image.load("images/7.gif").convert(), "1000": pg.image.load("images/8.gif").convert(), "1001": pg.image.load("images/9.gif").convert(), "1010": pg.image.load("images/10.gif").convert(), "1011": pg.image.load("images/11.gif").convert(), "1100": pg.image.load("images/12.gif").convert(), "1101": pg.image.load("images/13.gif").convert(), "1110": pg.image.load("images/14.gif").convert(), "1111": pg.image.load("images/15.gif").convert()}

plateau = Plateau(root, niveau)

end = False
while not(end):
	for event in pg.event.get():
		if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
			end = True
		elif event.type == pg.KEYDOWN:
			# Trous vers l'extérieur
			if (event.key == pg.K_UP and niveau.current[1] == 1 and niveau.cases[tuple(niveau.current)][n] == "1") or (event.key == pg.K_DOWN and niveau.current[1] == niveau.dim[1] and niveau.cases[tuple(niveau.current)][s] == "1") or (event.key == pg.K_LEFT and niveau.current[0] == 1 and niveau.cases[tuple(niveau.current)][w] == "1") or (event.key == pg.K_RIGHT and niveau.current[0] == niveau.dim[0] and niveau.cases[tuple(niveau.current)][e] == "1"):
				if tuple(niveau.current) == niveau.exit:
					print("Gagné !")
				elif tuple(niveau.current) == niveau.start:
					print("Vous avez tourné en rond et êtes revenu au départ...")
				else:
					print("Vous êtes face à un mystérieux trou dans le mur, je vous déconseille d'y aller cela pourrait être dangeureux.")
				break
			elif event.key == pg.K_UP:
				if niveau.current[1] > 1:
					if niveau.cases[tuple(niveau.current)][n] == "1":
						niveau.old = tuple(niveau.current)
						niveau.current[1] -= 1
			elif event.key == pg.K_DOWN:
				if niveau.current[1] < niveau.dim[1]:
					if niveau.cases[tuple(niveau.current)][s] == "1":
						niveau.old = tuple(niveau.current)
						niveau.current[1] += 1
			elif event.key == pg.K_LEFT:
				if niveau.current[0] > 1:
					if niveau.cases[tuple(niveau.current)][w] == "1":
						niveau.old = tuple(niveau.current)
						niveau.current[0] -= 1
			elif event.key == pg.K_RIGHT:
				if niveau.current[0] < niveau.dim[0]:
					if niveau.cases[tuple(niveau.current)][e] == "1":
						niveau.old = tuple(niveau.current)
						niveau.current[0] += 1
			plateau.actualiser()

pg.quit()