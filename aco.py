# Imports
import math
import random

# Paramètres
alpha = 3
beta = 3
eta = 100
rho = 0.0005    # Taux d'évaporation des phéromones

ter_size = 150     # Taille du terrain
base_qte_ressource = 50     # Nombre de ressource de base pour un point donné

space = 3  # Espace reservé autour des ressources (permettant le déplacement)    

# On tire au hasard la position de la colonie
colony_x = random.randint(10, ter_size-11)
colony_y = random.randint(10, ter_size-11)

matrix = []    # Martice contenant le contenu de chaque coordonnée    

ants = []      # Liste de fourmis
ressources = []    # Liste de ressources (sous forme de coordonnées)
qte_ressources = []    # Liste des quantités de chaque ressources (correspondant à la liste "ressources")
nb_obstacles = 2000    # Nombre d'obstacles sur le terrain
nb_ants = 500     # Nombre de fourmis sur le terrain
nb_leaders = 50
nb_ressources = 30      # Nombre de points ou l'on trouve des ressources

base_ph = 1.0

    

def InitTerrain(ter_size):

    # On initialise la matrice, en lui donnant sa taille ainsi que l'intensité des phéromones par défaut
    for i in range(ter_size):
        matrix.append([])

        for j in range(ter_size):
            matrix[i].append(base_ph)

    matrix[colony_x][colony_y] = "spawn"   # On indique dans la matrice que cette position correspond à la acolonie (aka le point de spawn des fourmis)
    print("Spawn OK")
    
    CreateAnts()
    print("Ants OK")

    CreateRessources()
    print("Ressources OK")

    CreateObstacles()
    print("Obstacles OK")

    print("Initialisation OK")



# Procédure créant les obstacles
def CreateObstacles():

    for i in range(nb_obstacles):

        ok_obstacles = 0    # Nombre de validation (objectif : une par ressources plus une pour la colonie)
        
        while ok_obstacles <= nb_ressources: # Tant que toutes les validation voulues ne sont pas validées
            
            # On choisi des coordonnées au hasard

            x = random.randint(0, ter_size-1)
            y = random.randint(0, ter_size-1)

            # On teste le viabilité

            if not ((matrix[x][y] == "obstacle") and (matrix[x][y] == "ressource") and (matrix[x][y] == "spawn")):      # Si l'emplacement n'est pas déjà occupé
                
                if (((x <= colony_x - space) or (x >= colony_x + space)) or ((y <= colony_y - space) or (y >= colony_y + space))):  # Si le point considéré n'interfère pas avec l'espace reservé autour de la colonie
                    ok_obstacles += 1

                else:
                    ok_obstacles = 0
                
                for i in range(nb_ressources):      # Validation de l'espace nécéssaire autour de ressources chaque

                    ressource_x = ressources[i][0]
                    ressource_y = ressources[i][1]

                    if (((x <= ressource_x - space) or (x >= ressource_x + space)) or ((y <= ressource_y - space) or (y >= ressource_y + space))):
                        ok_obstacles += 1
                        
                    else:
                        ok_obstacles = 0

        matrix[x][y] = "obstacle"




# Procédure créant les ressources
def CreateRessources():
    for i in range(nb_ressources):
        ok_ressource = False    # Booléen correspondant au succès du placement de la ressource
        while (not ok_ressource):   # On essaie de placer la ressource en boucle jusqu'à y arriver
            x = random.randint(7, ter_size - 7)   # On tire  les coordonnées au hasard (en excluant les bords)
            y = random.randint(7, ter_size - 7)
            ok_x = (abs(x - colony_x) in range(20, ter_size-1)) and (abs(y - colony_y) in range(0, ter_size-1))
            ok_y = (abs(y - colony_y) in range(20, ter_size-1)) and (abs(x - colony_x) in range(0, ter_size-1))
            if (ok_x or ok_y):
                if ([x, y] not in ressources):    # on vérifie qu'une ressource n'occupe pas déjà cet espace
                    ressources.append([x, y])
                    qte_ressources.append(base_qte_ressource)
                    matrix[x][y] = "ressource"   # On indique dans la matrice que cette case est prise par une ressource
                    ok_ressource = True     # La ressource a été placée, le booléen passe à True

# Procédure créant les fourmmis
def CreateAnts():
    leader = nb_leaders
    for i in range(nb_ants):
        if (leader != 0):
            ants.append(Ant(True))
            leader -= 1
        else:
            ants.append(Ant(False))


# Procédure gérent l'évaporation des phéromones
def PheromonesEvaporation():
    for i in range(ter_size):
        for j in range(ter_size):
            if (type(matrix[i][j]) == type(0.0)):	
                matrix[i][j] = (1 - rho) * matrix[i][j]

# Procédure permettant de bouger les fourmis
def MoveAnt():
    for n in ants:
        n.SelectSide()



# Procédure d'update
def UpdateACO():
    MoveAnt()
    PheromonesEvaporation()






# Classe Ant
class Ant:
    # Constructeur
    def __init__(self, is_leader_input):
        self.x = colony_x
        self.y = colony_y
        self.put_pheromone = False
        self.moves = 0
        self.to_avoid = []
        self.to_avoid_index = 0
        self.potential_paths = []	
        self.is_leader = is_leader_input
    
    # Procédure réinitialisant la fourmmi
    def Reset(self):
        self.x = colony_x
        self.y = colony_y
        self.put_pheromone = False
        self.to_avoid = []
        self.to_avoid_index = 0
        self.moves = 0


    def Move(self, dir):

        if ([self.x, self.y] not in self.to_avoid):
            self.to_avoid.append([self.x, self.y])
        

        # Valeurs par défaut, on ne bouge pas
        move_x = 0
        move_y = 0

        if dir == 0:    # Sud
            move_y = -1

        if dir == 1:    # Sud-Est
            move_y = -1
            move_x = 1

        if dir == 2:    # Est
            move_x = 1

        if dir == 3:    # Nord-Est
            move_x = 1
            move_y = 1

        if dir == 4:    # Nord
            move_y = 1

        if dir == 5:    # Nord-Ouest
            move_y = 1
            move_x = -1

        if dir == 6:    # Ouest
            move_x = -1

        if dir == 7:    # Sud-Ouest
            move_x = -1
            move_y = -1
        
        self.x += move_x
        self.y += move_y
			
        if [self.x, self.y] not in self.to_avoid:
            self.to_avoid.append([self.x, self.y])

        if (move_x == 0) or (move_y ==0):
            self.moves += 1

        else:
            self.moves += 2 ** .5
            
            
    def TryMove(self, dir):
        if dir == 0:
            return [self.x, self.y - 1]

        if dir == 1:
            return [self.x + 1, self.y - 1]

        if dir == 2:
            return [self.x + 1, self.y]

        if dir == 3:
            return [self.x + 1, self.y + 1]

        if dir == 4:
            return [self.x, self.y + 1]

        if dir == 5:
            return [self.x - 1, self.y + 1]

        if dir == 6:
            return [self.x - 1, self.y]

        if dir == 7:
            return [self.x - 1, self.y - 1]

		    
    # Fonction permettant de récupérer l'intensité des phéromones présentes autour de la fourmi
    def GetPheromone(self, dir):
        
        # Coordonnées du point à regarder
        # Valeur par défaut : on ne veut pas bouger
        ph_x = self.x
        ph_y = self.y


        # Suivant la direction choisie, on met à jour le point à regarder
        if (dir == 0):
            ph_y = self.y - 1

        if (dir == 1):
            ph_y = self.y - 1
            ph_x = self.x + 1

        if (dir == 2):
            ph_x = self.x + 1

        if (dir == 3):
            ph_x = self.x + 1
            ph_y = self.y + 1

        if (dir == 4):
            ph_y = self.y + 1

        if (dir == 5):
            ph_y = self.y + 1
            ph_x = self.x - 1

        if (dir == 6):
            ph_x = self.x - 1

        if (dir == 7):
            ph_x = self.x - 1
            ph_y = self.y - 1
            
        # Si le point ne contient qu'un float (aka un niveau de phéromones)
        if (type(matrix[ph_x][ph_y]) == type(0.0)):
            return matrix[ph_x][ph_y]

        else:
            return base_ph * 10000

    # Fonction calculant l'inverse du coût du chemin choisi (aka la distance)
    def CalcEta(self, dir):
        # Si on ne va pas en diagonale
        if (dir == 0) or (dir == 2) or (dir == 4) or (dir == 6):
            return 1.0
        # Sinon
        else:
            return (1 / (2 ** .5))

    # Procédure ajoutant les chemins actuellement disponibles si rien ne l'empêche
    def PotetialPaths(self, tab):
        self.potential_paths = []
        for i in tab:
            pp = self.TryMove(i)
            if not(pp in self.to_avoid) and (pp[0] in range(0, ter_size-1)) and (pp[1] in range(0, ter_size-1)) and (matrix[pp[0]][pp[1]] != "obstacle"):
                self.potential_paths.append(i)
                
    # Fonction calculant la somme des éléments d'un tableau jusqu'à un indice donné
    def SumTab(self, tab, last_i):
        sum_tab = 0
        if (last_i >= len(tab)):
            last_i = len(tab) - 1
        for i in range(0, last_i):
            sum_tab = sum_tab + tab[i]
        return sum_tab

	# Procédure sélectionnant un chemin
    def SelectSide(self):
        if (self.put_pheromone):	# Si on place des phéromones
            self.to_avoid_index += 1
            self.x = self.to_avoid[-self.to_avoid_index][0]
            self.y = self.to_avoid[-self.to_avoid_index][1]

            if (type(matrix[self.x][self.y]) == type(0.0)):
                tau = matrix[self.x][self.y] + (eta / self.moves)
                matrix[self.x][self.y] = tau

            if (matrix[self.x][self.y] == "spawn"):     # Si la fourmi est de retrour dans la colony, on la reset
                self.Reset()

        else:            
            # Suivant la position de la fourmi, on considère différent chemins possibles (pour éviter de sortir du terrain et donc de planter)
            if ((self.x == 0) and (self.y == 0)):
                self.PotetialPaths([2, 3, 4])

            if ((self.x == 0) and (self.y == ter_size-1)):
                self.PotetialPaths([0, 1, 2])
            
            if ((self.x == 0) and (self.y in range(1, ter_size-2))):
                self.PotetialPaths([0, 1, 2, 3, 4])

            if ((self.x == ter_size-1) and (self.y == 0)):
                self.PotetialPaths([4, 5, 6])

            if ((self.x == ter_size-1) and (self.y == ter_size-1)):
                self.PotetialPaths([0, 6, 7])
                
            if ((self.x == ter_size-1) and (self.y in range(1, ter_size-2))):
                self.PotetialPaths([0, 4, 5, 6, 7])
                
            if ((self.x in range(1, ter_size-2)) and (self.y == 0)):
                self.PotetialPaths([2, 3, 4, 5, 6])
                
            if ((self.x in range(1, ter_size-2)) and (self.y == ter_size-1)):
                self.PotetialPaths([0, 1, 2, 6, 7])
                
            if ((self.x in range(1, ter_size-2)) and (self.y in range(1, ter_size-2))):
                self.PotetialPaths([0, 1, 2, 3, 4, 5, 6, 7])
			
            # On calcule la probabilité d'un mouvement

            sum_ph = 0     # Somme des niveaux de phéromones
            for i in self.potential_paths:
                sum_ph += (self.CalcEta(i) ** beta) * (self.GetPheromone(i) ** alpha)

            prob = []   # Probabilités associées aux chemins disponibles
            for i in self.potential_paths:
                prob.append(((self.CalcEta(i) ** beta) * (self.GetPheromone(i) ** alpha)) / sum_ph )
                

            if (self.is_leader):        # Si la fourmi est un leader

                def SelectDirection():
                    if (len(self.potential_paths) > 0):    # Si on a au moins un chemin possible
                        max_prob = max(prob)
                        max_id = [i for i, j in enumerate(prob) if (j == max_prob)]
                        return self.potential_paths[random.choice(max_id)]
                    else:       # Si aucun chemin n'est possible, on reset la fourmi
                        self.Reset()

            else:                       # Si la fourmi n'est pas un leader
                prob_tab = []
                for i in range(0, len(prob)):
                    prob_tab.append(self.SumTab(prob, i))

                def SelectDirection():
                    if (len(self.potential_paths) > 0):     # Si on a au moins un chemin possible
                        r = random.random()
                        for i in range (len(prob_tab)-1):
                            if ((r >= prob_tab[i]) and (r < prob_tab[i+1])):
                                return self.potential_paths[i]
                        if (r >= prob_tab[-1]):
                            return self.potential_paths[-1]
                    else:       # Si aucun chemin n'est possible, on reset la fourmi
                        self.Reset()
            
            new_direction = SelectDirection()
            self.Move(new_direction)

            if (matrix[self.x][self.y] == "ressource"):
                self.put_pheromone = True
                qte_ressources[ressources.index([self.x, self.y])] -= 1

                if (qte_ressources[ressources.index([self.x, self.y])] == 0):     # Si le point a été vidé
                    matrix[self.x][self.y] = base_ph
                    self.put_pheromone = False