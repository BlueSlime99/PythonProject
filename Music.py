
#!/usr/bin/python
 
# -*- coding: ascii -*-

import shelve
import sys
import os

BIENVENUE = "Bienvenue dans votre base de données musicales personnelle!!!"
AUREVOIR = "Rock yourself out!"
MENU_PRINCIPAL = """
Menu principal

1) Afficher la base de données musicales
2) Ajouter un (plusieurs) morceau(x)
3) Rechercher par critères
4) Quitter le programme"""

MENU_AJOUT = """
Menu d'ajout de morceaux

1) Ajouter manuellement
2) Ajouter sur base d'un fichier"""
try:
    fichier = sys.argv[1]
except IndexError:
    print()

def charger_db():
    """Cette fonction créé la base de donnée musicale et affiche à l'utilisateur si la base existe déjà ou vient d'être créée,
    en cas d'erreur d'ouverture, un message est affiché à l'utilisateur
    :return: None"""
    db = None
    try:
        if(fichier != "blues"):
            db = shelve.open(fichier+'dat', writeback=True)
        if os.path.exists(fichier+'.dat'):
            print("Base de données musicales", fichier," chargée avec succès.")
        else:
            print("Nouvelle base de données musicales", fichier,"créée avec succès.")
        db = shelve.open(fichier, writeback=True)
    except ValueError:
        print("Une erreur est survenue au chargement ou à la création de la base de données musicales.")
        print(AUREVOIR)
    except NameError:
        print("Aucun nom de base de données musicales n'a été spécifié.")
        print(AUREVOIR)
    return db

def afficher_tout(db):
    """Fonction d'affichage des éléments qui se trouvent dans la base de donnée triés par ordre alphabétique et par note
    :param: la database"""
    try:
        tri=[]
        liste = ['Titre', 'Année', 'Artiste', 'Genre', 'Guitare', 'Note']
        if len(dict(db)) != 0:
            print("Base de données musicales complète :")
        for cle in db.keys():
            i = 0
            donnee = cle.split("_")
            donnee.append(db[cle])
            tri.append(donnee)
            listetri = sorted(tri, key=lambda colonnes: (colonnes[5]), reverse = True)
            finaltri = sorted(listetri, key=lambda colonnes: (colonnes[0]))
        for j in range(len(finaltri)):
            print()
            for i in range(len(liste)):
                if finaltri[j][i] == -1:
                    finaltri[j][i] = ''
                print(liste[i], " : " , finaltri[j][i])
        print()
    except UnboundLocalError:
        print()
        print("Votre base de donnée est vide, vous pouvez l'alimenter en faisant le choix 2")

def choix_valide(choix,min,max):
    """Fonction vérifie si le choix de l'utilisateur est correct
    :param choix: l'input de l'utilisateur
    :param min: la valeur minimum à choisir
    :param la valeur maximum à choisir
    return: booléen"""
    res = True
    try:
        choix = int(choix)
        if not (choix >= min and choix <= max):
            res = False
    except ValueError:
        res = False
    return res

def menu():
    """Fonction principale de l'execution du programme selon le choix de l'utilisateur """
    print(BIENVENUE)
    db = charger_db()
    if db is not None:
        choix = saisir_choix()
        while choix != 4:
            if choix == 1:
                afficher_tout(db)
            elif choix == 2:
                ajouter_morceaux(db)
            elif choix == 3:
                if len(dict(db)) == 0:
                    print("Votre base de donnée est vide, vous pouvez l'alimenter en tapant 2")
                else:
                    rechercher_morceaux(db)
            choix = saisir_choix()
        print(AUREVOIR)

def ajouter_morceaux(db):
    """Fonction gère l'alimentation de la base de donnée, fait appel aux 2 fonctions ajouter_mannuellement ou ajouter_donnee_fichier
        selon le choix de l'utilisateur qui est donné en input
        param: she: la datebase"""
    print(MENU_AJOUT)
    choix = int(input("Votre choix :"))
    print()
    while not choix_valide(choix, 1, 2):
        choix = input("choix incorrect, Votre choix :")
    if choix == 1:
        ajouter_manuellement(db)
    elif choix == 2:
        ajouter_donnee_fichier(db)

def ajouter_manuellement(db):
    """Cette fonction gère l'ajout manuel de donnée, vérifie si le morceau à insérer n'existe pas dans la base pour l'inserer, si ce dernier est deja
    dedans, il ne peut pas être réinséré
    :param: db base de donnée"""
    dico={}
    adto_db = saisir_morceau()
    shelkey = adto_db[0:5]
    new = ('_').join(shelkey)
    if adto_db[-1] == "":
        adto_db[-1] = -1
    else:
        adto_db[-1] = int(adto_db[-1])
    if new not in dict(db):
        print("Morceau", shelkey[0], "correctement inséré dans la base de données musicales")
        dico[new] = adto_db[-1]
        db[new] = dico[new]
    else:
        print("Morceau déjà présent dans la base de données musicales")

def ajouter_donnee_fichier(db):
    """Cette fonction alimente la base de donnée via un fichier csv dont le nom est fourni par l'utilisateur en input, indique à l'utilisateur
    si les morceaux insérés avec succés ou s'ils existent déjà dans la base de donnée,
    le fichier est checké avec la fonction check_file decrite ci-dessous.
    param: bd: base de donnée"""
    file = input("Veuillez saisir le nom du fichier : ")
    try:
        dico = check_file(file)
        for ajoutee in dico:
            if ajoutee not in dict(db):
                x = ajoutee.split("_")
                print("Morceau", x[0], "correctement inséré dans la base de données musicales")
                db[ajoutee] = dico[ajoutee]
            else:
                print("Morceau déjà présent dans la base de données musicales")
    except FileNotFoundError:
        print("Erreur lors de l'ouverture du fichier")

def rechercher_morceaux(db):
    """Fonction pour permettre à l'utilisateur de faire sa recherche sur la base de données et affiche en suite le resultat
    :param db:  la base de donne"""
    liste = ['Titre', 'Année', 'Artiste', 'Genre', 'Guitare', 'Note']
    print("Recherche de musiques correspondant à certains critères")
    print()
    print("Veuilez saisir les données du morceau :")
    li=[]
    final = []
    listeser = []
    search = saisir_morceau()
    if set(search) != {''}:
        for i in dict(db):
            val = i.split("_")
            val.append(db[i])
            listeser.append(val)
        for j in range(len(search)):
            for song in listeser:
                if j == 2:
                    if (search[j] in song[j]):
                        if song not in final:
                            final.append(song)
                else:
                    if search[j] == song[j]:
                        if song not in final:
                            final.append(song)
                            if search[5] is int:
                                if search[5] <= song[5]:
                                    if song not in final:
                                        final.append(song)
        for s in final:
            li.append(s)
        for elem in li:
            for i in range(len(search)):
                if set(search[0:5])!= '':
                    if search[5] is int:
                        if int(search[5]) > int(elem[5]):
                            if elem in final:
                                final.remove(elem)
            for k in range(5):
                if elem[k] != search[k] and search[k] != '':
                    if elem in final:
                        final.remove(elem)
                if i != 2:
                    if elem[i] != search[i] and search[i] != '' and int(search[5]) > int(elem[5]):
                        if elem in final:
                            final.remove(elem)
                elif search[i] not in elem[i]:
                    if elem in final:
                        final.remove(elem)
    if len(final) == 0:
        print()
        print("Aucun morceau trouvé dans la base de donnée")

    for j in range(len(final)):
        print()
        for i in range(len(liste)):
            if final[j][i] == -1:
                final[j][i] = ''
            print(liste[i], " : " , final[j][i])
    print()

def saisir_morceau():
    """Cette fonction permet la saisie et la vérification des données, si les données ne sont pas correctes on demande à l'utilisateur
    de saisir une donnée valide
     return: liste des données saisie par l'utilisateur"""
    liste_elements = []
    title = input("Titre : ")
    while title.isdigit():
        title = input("Veuillez saisir un Titre valide : ")
    liste_elements.append(title)
    year = input("Année : ")
    while year.isalpha():
        year = input("Veuillez saisir une Année valide : ")
    liste_elements.append(year)
    artists = input("Artistes (séparés par des virgules) : ")
    while artists.isdigit():
        artists = input("Veuillez saisir un Artiste valide : ")
    liste_elements.append(artists)
    style = input("style : ")
    while style.isdigit():
        style = input("Veuillez saisir un Style valide : ")
    liste_elements.append(style)
    guitar = input("Guitare : ")
    while guitar.isdigit():
        guitar = input("Veuillez saisir une Guitare : ")
    liste_elements.append(guitar)
    note = input("Note : ")
    while note not in['0','1','2','3','4','5','6','7','8','9','10','']:
        note = input("Veuillez saisir une Note entre 0 et 10 : ")
    if note != '':
        note = int(note)
    liste_elements.append(note)
    return liste_elements

def saisir_choix():
    """Cette fonction affiche le menu principale est demande à l'utilisateur de saisir son choix, si le choix n'est pas valide
    on redemande à l'utilisateur de saisir un choix valide
    return: le choix de l'utilisateur"""
    print(MENU_PRINCIPAL)
    choix = input("Votre choix : ")
    while not choix_valide(choix, 1, 4):
        choix = input("Veuillez saisir un choix entre 1 et 4 : ")
    choix = int(choix)
    return choix

def check_file(filename):
    """Fonction de verification des données présentes dans le fichier à injecter dans la base de donnée, si les éléments présents
    dans une lignes ne sont pas valides, on indique à l'utilisateur que cette ligne ne peut pas être injectée dans la base de donnée.
     les données valides sont ajoutées dans un dictionnaire
      param: le nom du fichier à injecter
      return: dictionnaire des données à ajouter dans la base de données"""
    dico = {}
    fichier = open(filename, "r", encoding='UTF-8')
    print("Lecture du fichier terminée avec succès.")
    print()
    lirelefich = fichier.readlines()
    lirelefich = lirelefich[1:]
    for i,elem in enumerate(lirelefich):
        x = elem.strip().split(";")
        if not x[0].isdigit() and x[1].isdigit() and len(x[1]) == 4 and not x[2].isdigit() and not x[3].isdigit() and not x[4].isdigit() and x[4] !='':
            if x[5] == '':
                x[5] = -1
                p = ("_").join(x[0:5])
                dico[str(p)] = int(x[5])
            elif x[5] in ['0','1','2','3','4','5','6','7','8','9','10']:
                p = ("_").join(x[0:5])
                dico[str(p)] = int(x[5])
        else:
            print("La ligne numéro", i+1, "contient des éléments incorrects, celle-ci ne peut pas être insérée dans votre base de donnée")
    return dico
if __name__ =='__main__':
    menu()

