from src.fltk import *
from time import sleep
from random import randint
# dimensions du jeu
taille_case = 20
largeur_plateau = 40  # en nombre de cases
hauteur_plateau = 30  # en nombre de cases

cree_fenetre(taille_case * largeur_plateau,taille_case * hauteur_plateau)
framerate = 4
option = False
gameover = False
jouer_a_1 = False
jouer_a_2 = False
# options 
obstacle = False 
acceleration = False 
pacman = False 
#LES FONCTIONS
def case_vers_pixel(case):

    """
    Fonction recevant les coordonnées d'une case du plateau sous la
    forme d'un couple d'entiers (id_colonne, id_ligne) et renvoyant les
    coordonnées du pixel se trouvant au centre de cette case. Ce calcul
    prend en compte la taille de chaque case, donnée par la variable
    globale taille_case.
    """

    i, j = case
    return (i + .5) * taille_case, (j + .5) * taille_case
def affiche_pommes(pommes):

    """
    Cette fonction recoit les coordonnées de pommes pour ensuite
    les transformer en pixel et range la valeur x et y dans deux
    variables respectives.
    Ensutie la fonction trace un cercle et un rectangle aux
    coordonnées x, y pour y représenter une pomme.
    ----------
    pommes : coordonnées de la prochaine pomme
    -------

    """

    x, y = case_vers_pixel(pommes)

    cercle(x, y, taille_case/2,
           couleur='darkred', remplissage='red')
    rectangle(x-2, y-taille_case*.4, x+2, y-taille_case*.7,
              couleur='darkgreen', remplissage='darkgreen')

def affiche_obstacles(obstacles):
    for obstacle in obstacles:
        x, y = case_vers_pixel(obstacle)
        rectangle(x - taille_case/4, y - taille_case/2, x + taille_case/4, y + taille_case/2,
                  couleur='black', remplissage='grey')
def affiche_serpent(serpent, joueur):

    x, y = case_vers_pixel(serpent)

    if joueur == 1 :
        cercle(x, y, taille_case/2 + 1,couleur='darkgreen', remplissage='green')
    elif joueur == 2:
        cercle(x, y, taille_case/2 + 1,couleur='darkred', remplissage='orange')

def change_direction1(direction, touche):#joueur1
    """
    Renvoie le vecteur unitaire indiquant la direction correspondant à la touche
    pressée par l'utilisateur. Les valeurs de retour possibles sont (0, 1),
    (1, 0), (0, -1) et (-1, 0).
    """
    if touche == 'Up' and direction != (0, 1):
        return (0, -1)
    elif touche == 'Down' and direction != (0, -1):
        return (0, 1)
    elif touche == 'Left' and direction != (1, 0):
        return (-1, 0)
    elif touche == 'Right' and direction != (-1, 0):
        return (1, 0)
    else:
        # pas de changement !
        return direction
def change_direction2(direction2, touche):
    if touche == 'z' and direction2 != (0, 1):
        return (0, -1)
    elif touche == 's' and direction2 != (0, -1):
        return (0, 1)
    elif touche == 'q' and direction2 != (1, 0):
        return (-1, 0)
    elif touche == 'a' and direction2 != (-1, 0):
        return (1, 0)
    else:
        return direction2
def deplacement_serpent(serpent,direction):
    if serpent == serpent1:
        serpent1[0][0] += direction1[0]
        serpent1[0][1] += direction1[1]
        queue_serpent1 = [serpent1[0][0], serpent1[0][1]]
        serpent1.pop()
        serpent1.insert(0,queue_serpent1)

    elif serpent == serpent2:
        serpent2[0][0] += direction2[0]
        serpent2[0][1] += direction2[1]
        queue_serpent2 = [serpent2[0][0], serpent2[0][1]]
        serpent2.pop()
        serpent2.insert(0,queue_serpent2)
def is_inside_button(x, y, button_coords):
    return button_coords[0] <= x <= button_coords[2] and button_coords[1] <= y <= button_coords[3]
#boucle principale
jouer = True
while jouer:
    efface_tout()
    score1 = 0
    score2 = 0
    gagnant1 = False
    gagnant2 = False
    direction1 = [0, 0]  
    direction2 = [0, 0]
    obstacles = [[randint(0, 39),randint(0, 29)],
                 [randint(0, 39),randint(0, 29)],
                 [randint(0, 39),randint(0, 29)],
                 [randint(0, 39),randint(0, 29)]]
    pommes = [randint(0, 38),randint(0, 28)]

    # liste des coordonnées de cases adjacentes décrivant le serpent
    serpent1 = [[20 ,10],[-1,-1]]
    serpent2 = [[20 ,20],[-1,-1]]
#menu principal=================================
    menu = True
    image(400, 300, "assets/menu.gif")
    while menu:
        mise_a_jour()
        # gestion des événements
        ev = donne_ev()
        ty = type_ev(ev)
        # Quand on quitte le jeu il se ferme
        if ty == 'Quitte':
            jouer = False
            break

        # Fonctionnement des boutons
        elif ty == 'ClicGauche':

            #1 joueur
            if 160 <= abscisse(ev) <= 750 and 200 <= ordonnee(ev) <= 300:
                jouer_a_1 = True
                menu = False

            # 2 joueurs
            elif 160 <= abscisse(ev) <= 750 and 320 <= ordonnee(ev) <= 400:
                jouer_a_1 = True
                jouer_a_2 = True
                menu = False

            # Option
            elif 160 <= abscisse(ev) <= 750 and 420 <= ordonnee(ev) <= 510:
                menu = False
                option = True
### Menu option ##############################################################

    while option:
        efface_tout()
        image(400, 300, "assets/option.gif")
        #obstacle
        if obstacle:
            texte(640, 185, "ON", couleur='green', taille=16)
        else:
            texte(640, 185, "OFF", couleur='red', taille=16)
        #acceleration
        if acceleration:
            texte(670, 270, "ON", couleur='green', taille=16)
        else:
            texte(670, 270, "OFF", couleur='red', taille=16)
        #pacman
        if pacman:
            texte(625, 355, "ON", couleur='green', taille=16)
        else:
            texte(625, 355, "OFF", couleur='red', taille=16)
        #Retour
        mise_a_jour()
        # gestion des événements
        ev = donne_ev()
        ty = type_ev(ev)
        if ty == 'Quitte':
            jouer = False
            break
        # Fonctionnement des boutons
        elif ty == 'ClicGauche':
            #Bouton Obstacle
            if 150 <= abscisse(ev) <= 720 and 160 <= ordonnee(ev) <= 230:
                if obstacle == False:
                    obstacle = True
                else:
                    obstacle = False
            #Bouton Retour
            elif 220 <= abscisse(ev) <= 650 and 430 <= ordonnee(ev) <= 500:
                option = False
                menu = True
                continue
            #Bouton Acceleration
            elif 150 <= abscisse(ev) <= 720 and 250 <= ordonnee(ev) <= 320:
                if acceleration == False:
                    acceleration = True
                else:
                    acceleration = False
            elif 180 <= abscisse(ev) <= 680 and 330 <= ordonnee(ev) <= 400:
                if pacman == False:
                    pacman = True
                else:
                    pacman = False
### mode JOUER_A_1===========================================
    while jouer_a_1:
        framerate = 4
        efface_tout()
        image(400, 300, "assets/map.png")
### MODE PACMAN
        #accelerationt
        if acceleration and framerate < 30:
            #framerate += 1
            print(framerate) 
        # Afficher le score 
        if pacman:
            texte(10, 10,("Score", score1), taille = "16", couleur = "white",police = 'benguiat')
        else:
            texte(10, 10,("Score", score1), taille = "16", couleur = "green",police = 'benguiat')

        affiche_pommes(pommes)
        # on crée un obstacle qui se déplace
        chance_obstacle = randint (1,60)
        if chance_obstacle == 7:
            obstacles = [[randint(0, 39),randint(0, 29)],
                         [randint(0, 39),randint(0, 29)],
                         [randint(0, 39),randint(0, 29)],
                         [randint(0, 39),randint(0, 29)]]
        if obstacle:
            affiche_obstacles(obstacles)

        #afficher le score du serpent 2
        if jouer_a_2:
            texte(700, 10,("Score", score2), taille = "16",couleur = "orange", police = 'benguiat')
            for i in range(len(serpent2)+1):
                affiche_serpent(serpent2[i-1], 2)
        # appel de la fonction affiche_serpent
        for i in range(len(serpent1)+1):
            affiche_serpent(serpent1[i-1], 1)
        mise_a_jour()
        # gestion des événements
        ev = donne_ev()
        ty = type_ev(ev)
   
        if ty == 'Quitte':
            jouer = False
            break
        # appel de la fonction change_direction
        elif ty == 'Touche':
            depart = True
            print(touche(ev))
            direction1 = change_direction1(direction1, touche(ev))
            if jouer_a_2 == True:
                direction2 = change_direction2(direction2, touche(ev))

        #afficher le message de début
        if (direction1 == [0, 0] and direction2 == [0, 0]):
            texte(70,200,"La partie peut commencer !", couleur = "white",police = 'benguiat')

        mise_a_jour()

        # appel de la fonction déplacement serpent
        if serpent1[0] == pommes:
            score1 += 1
            pommes = [randint(0,36), randint(0,26)]
            serpent1.append([serpent1[0][0], serpent1[0][1]])
            if acceleration and framerate < 25:
                framerate += 1
                print("Accélération ! Nouveau framerate :", framerate)
        deplacement_serpent(serpent1,direction1)

        mise_a_jour()
        # serpent 2
        if serpent2[0] == pommes and jouer_a_2:
            score2 += 1
            pommes = [randint(0,36), randint(0,26)]
            serpent2.append([serpent2[0][0], serpent2[0][1]])
        deplacement_serpent(serpent2,direction2)
        if pommes == obstacles[:]:
            pommes = [randint(0,36), randint(0,26)]
# MORT AVEC OBSTRACLE
        # obstacle = True
        if obstacle:
            if (serpent1[0] == obstacles[0] or serpent1[0] == obstacles[1] or
            serpent1[0] == obstacles[2] or serpent1[0] == obstacles[3]):
                mise_a_jour()
                sleep(0.5)
                if jouer_a_2:
                    gagnant2 = True
                gameover = True
                jouer_a_1 = False
                efface_tout()
            #joueur 1 et 2
            if jouer_a_2:
                if (serpent2[0] == obstacles[0] or serpent2[0] == obstacles[1] or
                serpent2[0] == obstacles[2] or serpent2[0] == obstacles[3]
                and jouer_a_2 == True):
                    mise_a_jour()
                    sleep(0.5)
                    gagnant1 = True
                    gameover = True
                    jouer_a_1 = False
                    efface_tout()
        # le serpent 1 ne mange pas la queue
        if serpent1[0] in serpent1[2:]:
            mise_a_jour()
            sleep(0.5)
            if jouer_a_2:
                    gagnant2 = True
            gameover = True
            jouer_a_1 = False
            efface_tout()
            continue

        # le serpent 2 se mange la queue
        if (serpent2[0] in serpent2[2:] and jouer_a_2 == True):
            mise_a_jour()
            sleep(0.5)
            gagnant1 = True
            gameover = True
            jouer_a_1 = False
            efface_tout()
            continue
        # 2 joueurs
        if jouer_a_2 == True:
            # Quand le serpent 1 rentre dans le serpent 2
            if serpent1[0] in serpent2[:]:
                mise_a_jour()
                sleep(0.5)
                gagnant2 = True
                gameover = True
                solo = False
                efface_tout()
                continue
            #serpent 2 rentre dans le serpent 1
            elif serpent2[0] in serpent1[:]:
                mise_a_jour()
                sleep(0.5)
                gagnant1 = True
                gameover = True
                jouer_a_1 = False
                efface_tout()
       #Création des bordures d
        if pacman == False:
            # Si le serpent 1 sort
            if (serpent1[0][0] >= 40 or serpent1[0][0] <= -1 or serpent1[0][1] >= 30 or serpent1[0][1] <= -1):
                mise_a_jour()
                sleep(0.5)
                if jouer_a_2:
                    gagnant2 = True
                gameover = True
                jouer_a_1 = False
                efface_tout()
                continue

            # Si le serpent 2 sort de la map
            if (serpent2[0][0] >= 40 or serpent2[0][0] <= -1 or
            serpent2[0][1] >= 30 or serpent2[0][1] <= -1 and jouer_a_2 == True):
                mise_a_jour()
                sleep(0.5)
                gagnant1 = True
                gameover = True
                jouer_a_1 = False
                efface_tout()
                continue

### MODE PACMAN======================================
        if pacman:

            #Si le serpent 1 sort
            if (serpent1[0][0] >= 40 or serpent1[0][0] <= -1 or
            serpent1[0][1] >= 30 or serpent1[0][1] <= -1):
                for i in range(0, len(serpent1)):
                    if serpent1[i][0] == 40:
                        serpent1[i][0] = 0
                    elif serpent1[i][0] == -1:
                        serpent1[i][0] = 40
                    elif serpent1[i][1] == 30:
                        serpent1[i][1] = 0
                    elif serpent1[i][1] == -1:
                        serpent1[i][1] = 30

            #Si le serpent 2 sort 
            if (serpent2[0][0] >= 40 or serpent2[0][0] <= -1 or
                serpent2[0][1] >= 30 or serpent2[0][1] <= -1 and jouer_a_2 == True):
                for i in range(0, len(serpent2)):
                    if serpent2[i][0] == 40:
                        serpent2[i][0] = 0
                    elif serpent2[i][0] == -1:
                        serpent2[i][0] = 40
                    elif serpent2[i][1] == 30:
                        serpent2[i][1] = 0
                    elif serpent2[i][1] == -1:
                        serpent2[i][1] = 30
        sleep(1 / framerate)
# Menu GAME OVER ==========================
    while gameover:
        image(400, 300, "assets/game_over.gif")
        if jouer_a_2 == False:
            texte(750, 10, (score1), taille=30, couleur='white', police='benguiat')
            # Bouton rejouer
            rectangle(50, 280, 230, 330, remplissage='darkgreen')
            texte(140, 305, "Rejouer", taille=25, couleur='white', police='benguiat', ancrage='center')
            # Bouton quitter
            rectangle(50, 370, 230, 420, remplissage='darkred')
            texte(140, 395, "Quitter", taille=25, couleur='white', police='benguiat', ancrage='center')
            mise_a_jour()
        if jouer_a_2 == True :
            texte(50, 18,(score1), taille = "15", couleur = 'white',
                    police = 'benguiat')
            texte(700, 18,(score2), taille = "15", couleur = 'white',
                    police = 'benguiat')
            #le joueur 2 a gagné
            if gagnant2 == True and jouer_a_2 == True:
                texte(250, 295,("Le joueur 2 gagne"), taille = "15",couleur = 'white', police = 'benguiat')

            #le joueur 1 a gagné
            elif gagnant1:
                texte(250, 295,("Le joueur 1 gagne"), taille = "15",couleur = 'white', police = 'benguiat')
            #MENU GAMEOVER
            rectangle(50, 280, 230, 330, remplissage='darkgreen')
            texte(140, 305, "Rejouer", taille=25, couleur='white', police='benguiat', ancrage='center')
            # Bouton quitter
            rectangle(50, 370, 230, 420, remplissage='darkred')
            texte(140, 395, "Quitter", taille=25, couleur='white', police='benguiat', ancrage='center')

            mise_a_jour()

        ev = donne_ev()
        ty = type_ev(ev)

        if ty == 'Quitte':
            jouer = False
            break
        elif ty == 'ClicGauche':
            x_click, y_click = abscisse(ev), ordonnee(ev)

            # Bouton Quitter
            if is_inside_button(x_click, y_click, (50, 370, 230, 420)):
                gameover = False
                menu = True
                jouer_a_2 = False
                ferme_fenetre()  # Quitter

            elif is_inside_button(x_click, y_click, (50, 280, 230, 330)):
                gameover = False
                jouer_a_1 = True
                if jouer_a_2:
                    jouer_a_2 = True

        mise_a_jour()
        sleep(1/framerate)
ferme_fenetre()
