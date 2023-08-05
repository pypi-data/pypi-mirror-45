#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
#
#  class Film.py
#
#  Copyright 2019 Robert Sebille <robert@sebille.name>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#


from time import sleep
from os import listdir


class Film:
    """Cette classe fournit des outils pour afficher des petits films
    à partir de frames en ascii.

    Les frames peuvent être dans un seul fichier, avec un séparateur ou
    dans plusieurs fichiers qui seront lus d'un répertoire à préciser,
    et dans l'ordre alphanumérique croissant.

    Pour démarrer:
        from film import Film
        Film.demo()
    Dépot: https://gitlab.adullact.net/zenjo/film/tree/master
    """

    _version = "0.0.11"

    def __init__(self, titre="", dict_sous_titres={}):
        """Constructeur"""
        self._titre = str(titre)
        self._frames = []
        self._reverse = False
        self._affiche_titre = True
        self._affiche_ctrl_c = True
        self._titre_x = 2
        self._dict_sous_titres = dict_sous_titres

    def __str__(self):
        """Retoune la chaîne "Film : Titre du film" """
        return str("Film : " + self.titre)

    # Private
    def __ccls(cls):  # clear the screen
        return "\033[2J"
    __ccls = classmethod(__ccls)

    def __ccxy2(self, x, y):  # position cursor at x across, y down
        return "\033["+str(y)+";"+str(x)+"f"

    def __csrv(self):  # print reverse
        return "\033[7m"

    def __csrs(self):  # print, reset all
        return "\033[0m"

    # Public
    # class methods
    def version(cls):
        return cls._version
    version = classmethod(version)

    def delay(cls, secondes):
        """Evite l'importation de la méthode sleep du module time"""
        sleep(secondes)
    delay = classmethod(delay)

    def clearsc(cls):
        """Efface l'écran."""
        print(cls.__ccls())
    clearsc = classmethod(clearsc)

    def demo(cls):
        from film.demo import demo
        demo()
    demo = classmethod(demo)

    # property
    def get_titre(self):
        """Retourne le titre"""
        return self._titre

    def set_titre(self, titre):
        """Modifie ou crée le titre"""
        self._titre = str(titre)

    titre = property(get_titre, set_titre)

    def set_frame(self, fichier, sep="#"):
        """Lit les frames à partir d'un seul fichier. Ces frames sont
        séparées par un séparateur, par défaut #
        """
        with open(fichier) as c:
            liste = c.readlines()
        s = "".join(liste)
        liste = s.split(sep)
        for l in liste:
            self._frames.append(l.split("\n"))

    frame = property('', set_frame)

    def set_frames(self, repertoire):
        """Lit les frames à partir de fichiers dans répertoire. Chaque frame
        est dans un fichier propre. Les fichiers sont lus dans le répertoire
        dans le sens alphnumérique croissant de leurs noms.
        """
        frms = []
        for fichier in listdir(repertoire):
            with (open(repertoire + '/' + fichier)) as f:
                frms.append(f.read())
        for f in frms:
            self._frames.append(f.split("\n"))

    frames = property('', set_frames)

    def get_dict_sous_titres(self):
        """Retourne le dictionnaire des sous-titres"""
        return self._dict_sous_titres

    def set_dict_sous_titres(self, dict_sous_titres):
        """Modifie ou crée le dictionnaire des sous-titres

        Ce dictionnaire est de la forme: {(a, b): "sous-titre"}
        ou a = n° de la frame où l'affichage de "sous-titre" démarre et
        b = n° - 1 de la frame où s'arrête l'affichage de "sous-titre"
        """
        self._dict_sous_titres = dict_sous_titres

    dict_sous_titres = property(get_dict_sous_titres, set_dict_sous_titres)

    def get_titre_x(self):
        """Retourne la coordonnées x d'affichage du titre"""
        return self._titre_x

    def set_titre_x(self, titre_x):
        """Décide la coordonnée x du titre"""
        self._titre_x = titre_x

    titre_x = property(get_titre_x, set_titre_x)

    def get_reverse(self):
        """Retourne le sens du film en avant ou en arrière (booléen)"""
        return self._reverse

    def set_reverse(self, direction):
        """Décide le sens du film, en avant ou en arrière (booléen)"""
        self._reverse = direction

    reverse = property(get_reverse, set_reverse)

    def get_affiche_titre(self):
        """Retourne si il faut afficher le titre (booléen)"""
        return self._affiche_titre

    def set_affiche_titre(self, affiche_titre):
        """Décide si il faut afficher le titre (booléen)"""
        self._affiche_titre = affiche_titre

    affiche_titre = property(get_affiche_titre, set_affiche_titre)

    def get_affiche_ctrl_c(self):
        """Retourne si il faut afficher une mention CTRL + C (booléen)"""
        return self._affiche_ctrl_c

    def set_affiche_ctrl_c(self, affiche_ctrl_c):
        """Décide si il faut afficher une mention CTRL + C (booléen)"""
        self._affiche_ctrl_c = affiche_ctrl_c

    affiche_ctrl_c = property(get_affiche_ctrl_c, set_affiche_ctrl_c)

    # other methods
    def projection(self, nb=0, x=2, y=2, trace=0, delai=0.1):
        """Lance l'instance film en lisant les frames.

        - nb: nombre de frames à exécuter. 0 = non déterminé
        - x, y les coordonnées haut gauche de départ du film (y compris
        le titre, si self.affiche_titre = True
        - trace nombre de blancs à ajouter à la frame suivant le sens du film:
        avant si self.reverse = False, après si self.reverse = True
        - delai: la durée en seconde de chaque frame

        Si self.reverse = True, le film peut avoir des effets de bord non
        désiré quand x < 0. Vous pouvez régler cela via l'appel de la
        méthode.
        """

        self.clearsc()
        if self.affiche_titre:
            self.goto(self.titre_x + 2, y)
            print(self.get_titre())
            y += 2
        if self.reverse:
            dep = nb
            after = " " * trace
            before = ""
        else:
            dep = 0
            after = ""
            before = " " * trace
        seq = 0
        while (dep <= nb and dep >= 0) or nb == 0:
            try:
                for f in self._frames:
                    # affichage de la frame
                    for l in range(len(f)):
                        self.goto(x + dep, y + l)
                        print(before + f[l] + after)
                    # Traitement des sous-titres
                    self.goto(28, y + l + 1)
                    print(" "*40)
                    for k, v in self._dict_sous_titres.items():
                        if seq in range(int(k[0]), int(k[1])):
                            self.goto(28, y + l + 1)
                            self.print_reverse(v)
                    # affichage éventuel du CTRL+C
                    self.goto(0, y + l + 2)
                    if self.affiche_ctrl_c:
                        print(" CTRL + C to stop.")
                    sleep(delai)
                    # deplacement et sequençage
                    if self.reverse:
                        dep -= 1
                        seq -= 1
                    else:
                        dep += 1
                        seq += 1
            except KeyboardInterrupt:
                print("\nReçu CTRL + C")
                input("Pressez entrée pour sortir.")
                exit("Bye !")

    def goto(self, x, y):
        """Amène le curseur en x, y pour impression (print)"""
        print(self.__ccxy2(x, y), sep="", end="")

    def print_reverse(self, message):
        """Inverse couleur et background pour l'impression d'un message"""
        print(self.__csrv() + " " + message + " " + self.__csrs())
