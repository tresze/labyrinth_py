#labyrinth.py

import os, pygame, sys, getch
from random import randint

pygame.init()
pygame.mixer.music.load("pop.wav")

# matrix keszitese a megadott fajlbol
def matrix_file(file_name):
    m = []                # ebbe kerul majd a matrix
    f = open(file_name)   # fajl megnyitasa

    # soronkent vegigmegyunk a fajlon
    for line in f:
        line = line.strip()           # a sorbol toroljuk a whitespace karaktereket
        line = list(line)             # listava alakitjuk a sor stringet

        m.append(line)   # beletesszuk a listat (sort) a matrixba
    
    # ellensegek generalasa
    for i in range(0, 6):
        # veletlen koordinata generalasa (nem a legszelso mezokhoz)
        x = randint(1, len(m) - 2)
        y = randint(1, len(m[0]) - 2)

        # folytatjuk, amig nem talalunk olyat, ahol ures hely van
        while m[x][y] != "0":
            x = randint(1, len(m) - 2)
            y = randint(1, len(m[0]) - 2)

        # ha megvan, odateszunk egy ellenseget
        m[x][y] = "3"

        # es korbevesszuk az ellenseg koruli mezokkel
        if m[x-1][y] == "0":
            m[x-1][y] = "4"
        if m[x][y-1] == "0":
            m[x][y-1] = "4"
        if m[x+1][y] == "0":
            m[x+1][y] = "4"
        if m[x][y+1] == "0":
            m[x][y+1] = "4"
    
    return m

# a matrix elemei innen elerhetove valnak sor es oszlop alapjan; pl. a bal felso sarok igy: matrix[0][0]
matrix = matrix_file("maze.txt")

# labirintus es mozgathato karakter kirajzolasahoz fuggveny
def printmaze(matrix):
    for row in matrix:
        for char in row:
            if char == "0" or char == "4":     # ures helyek, ellenseg melletti mezok
                sys.stdout.write("  ")
            elif char == "1":                  # fal
                sys.stdout.write("〠")
            elif char == "2":                  # a mozgathato karakter (kor)
                sys.stdout.write("◯ ")
            elif char == "3":                  # ellenseg
                sys.stdout.write("⚉ ")
        print()

# matrix soraihoz es oszlopaihoz inicializalt valtozok
i, j = 1, 1

# jatek inditasa es a labirintus kirajzolasa
print("\nControls: W, A, S, D.\nPress a button to start the game.\n")
getch.getch()                       # ennek a segitsegevel folyamatos a mozgas, nem kell mindig Entert leutni
matrix[1][1] = "2"                  # a 2-es (kor) kezdopozicioja
printmaze(matrix)

# mozgas implementalasa
while not (matrix[28][39] == "2" or matrix[29][39] == "2"): # ez a ket pozicio a labrinitus kijaratat jelenti
    move = getch.getch()
    print("\033[H\033[J")           # kepernyo frissitese
    matrix[i][j] = "0"              # ez a sor biztositja, hogy csak egy 2-es (kor) legyen egyszerre a labirintusban
    if move == "a":                 # balra lepes = matrix[i][j-1] --> a jatekos nem valtoztatja a sort, az oszlopot viszont eggyel balra igen
        if matrix[i][j-1] != "1":   # ha nem falra erkezik a kor
            j = j - 1               # akkor egy pozicioval balrabb fogja kirajzolni azt
    if move == "s":
        if matrix[i+1][j] != "1":
            i = i + 1 
    if move == "d":
        if matrix[i][j+1] != "1":
            j = j + 1 
    if move == "w":
        if matrix[i-1][j] != "1":
            i = i - 1

    if matrix[i][j] == "4":
        print("Don't touch the enemy!\n")

    if matrix[i][j] == "3":
        print("You died!")
        exit()

    matrix[i][j]= "2"               # az eppen aktualis pozicio valtson 0-rol, 3-rol vagy 4-rol 2-re (korre)
    printmaze(matrix)
    pygame.mixer.music.play()
    
else:
    print("Congratulations! You managed to get out of the labyrinth!")

