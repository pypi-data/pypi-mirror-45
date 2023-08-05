#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
#
#  exemple.py
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

from film import Film


def demo():

    # On crée 4 nouveaux films (f1, 2, 3, 4), avec leur titre (non requis),
    # leur diction de sous-titre(non-resuis) et leur(s) fichier(s) de freme(s)
    # requis avant de jouer le film
    d1 = {
        (5, 10):  "        Bonjour           ",
        (20, 27): " Quelle belle promenade ! ",
        (34, 41): " Et quel temps agréable.  ",
        (48, 55): "     Allez, au revoir     "
        }

    f1 = Film("La promenade tranquille ...", d1)
    f1.frames = "frames/"

    d2 = {
        (5, 15):  "      Ouf ti !        ",
        (25, 35): " Ca tape la vitesse ! ",
        (45, 60): "   Bon, je freine.    "
        }

    f2 = Film("La moto infernale", d2)
    f2.frame = "frame/roflflyingmoto"

    d3 = {
        (5, 10):  "   Je t'aurai, rascal !    ",
        (15, 20): " Essaie toujours, voyou !  ",
        (25, 30): " Tu ne t'en sortiras pas ! ",
        (35, 40): "  Numérotte tes abattis !  "
        }

    f3 = Film("La poursuite impitoyable", d3)
    f3.frame = "frame/poursuiteci"

    f4 = Film("La poursuite effroyable")
    f4.frame = "frame/poursuiteic"
    # On peur ajouter les sous-titres par après
    f4.dict_sous_titres = {
        (5, 10):  "   Ha ha, on ne dit plus rien !   ",
        (15, 20): " C'est ce que tu crois, bandit !  ",
        (25, 30): " Je te tiens cette fois, rascal ! ",
        (35, 40): "    Compte là-dessus, voyou !     "
        }

    # on efface l'écran. Méthode de classe, car quand on efface l'écran,
    # c'est pour tous les objets films
    Film.clearsc()

    # goto: place le curseur à x, y pour impression
    f1.goto(20, 6)
    f1.print_reverse("Les studios Robert Sebille présentent")
    f1.goto(29, 8)
    # retourne la version de la classe
    print("Version " + Film.version())
    Film.delay(2)

    Film.clearsc()
    f1.goto(25, 6)
    # Inverse couleur et background pour l'impression d'un message
    # get_titre property, bon, faut-il l'expliquer? ;)'
    f1.print_reverse(f1.titre)
    Film.delay(2)
    # lance le film f1. 65 frames à jouer, démarrer le film en 2, 2
    # 0 blanc de "trace", delai de 0.2 secondes par frame
    f1.projection(66, 2, 2, 0, 0.2)
    f1.goto(27, 6)
    print("Sniff ! Que c'était beau !")
    Film.delay(2)

    Film.clearsc()
    f2.goto(27, 6)
    f2.print_reverse(f2.titre)
    Film.delay(2)
    # La moto, ça fonce ...
    f2.projection(82, 2, 2, 0, 0.05)
    f1.goto(30, 6)
    print("Tonnerre! Quelle vitesse !")
    Film.delay(2)

    Film.clearsc()
    f3.goto(27, 6)
    f3.print_reverse(f3.titre)
    Film.delay(2)
    f3.projection(45, 2, 2, 0, 0.2)
    f3.goto(13, 6)
    print("Quelle suspense époustouflant !")
    Film.delay(2)
    f3.goto(13, 6)
    print("Rembobinons ?                  ")
    Film.delay(1)
    f3.goto(13, 6)
    print("Rembobinons !                  ")
    Film.delay(1)
    # Place le sens du film en arrière
    f3.reverse = True
    # on a mis un débit par frame plus rapide pour le rembobinage
    f3.projection(45, 2, 2, 0, 0.05)
    Film.delay(1)
    Film.clearsc()
    f3.goto(13, 6)
    print("Et rejouons ce splendide film ! ")
    Film.delay(2)
    # on replace le sens du film en avant
    f3.reverse = False
    f3.projection(45, 2, 2, 0, 0.2)
    f3.goto(10, 6)
    print("Quelle film ! On ne s'en lasse pas !")
    Film.delay(2)
    f3.goto(10, 6)
    print("Mais ce n'est pas tout, voyons la suite")
    Film.delay(2)

    Film.clearsc()
    f4.titre = "La revanche des indiens"
    f4.goto(27, 6)
    f4.print_reverse(f4.titre)
    Film.delay(2)
    Film.clearsc()
    f4.goto(27, 6)
    print("Ha ha !")
    Film.delay(2)
    f4.projection(45, 2, 2, 0, 0.2)
    Film.delay(1)

    Film.clearsc()
    f4.goto(27, 6)
    f4.print_reverse("C'est fini ! Sniff !")
    Film.delay(2)
    Film.clearsc()
    f4.goto(27, 6)
    f4.print_reverse("A vous de jouer !")
    Film.delay(2)
    Film.clearsc()
    Film.goto(f4, 0, 0)
    print("""
Usage:
from classes.Film import Film
help(Film)
""")
    Film.delay(2)
    help(Film)
    print("\n\n\n")


if __name__ == '__main__':
    demo()
    pass
