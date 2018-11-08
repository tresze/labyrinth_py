#labyrinth.py

import os, pygame, sys, getch

pygame.init()
pygame.mixer.music.load("pop.wav")

turn = 310
# matrix keszitese a megadott fajlbol
def matrix_file(file_name):
    m = []                # ebbe kerul majd a matrix
    f = open(file_name)   # fajl megnyitasa

    # soronkent vegigmegyunk a fajlon
    for line in f:
        line = line.strip()           # a sorbol toroljuk a whitespace karaktereket (pl sortores)
        line = list(line)             # listava alakitjuk a sor stringet "111001" -> ["1", "1", "1", "0", "0", "1"]

        m.append(line)   # beletesszuk a listat (sort) a matrixba
    
    return m

# a matrix elemei innen elerhetove valnak sor es oszlop alapjan; pl. a bal felso sarok igy: matrix[0][0]
matrix = matrix_file("maze.txt")

# labirintus es mozgathato karakter kirajzolasahoz fuggveny
def printmaze(matrix):
    k = 0
    for row in (matrix):
        for char in (row):
            if k < turn:
                if char == "0" or char == "4":     # ures helyek, ellenseg melletti mezok
                    sys.stdout.write("  ")
                elif char == "1":                  # fal
                    sys.stdout.write("〠")
                elif char == "2":                  # a mozgathato karakter (kor)
                    sys.stdout.write("◯ ")
                elif char == "3":                  # ellenseg
                    sys.stdout.write("⚉ ")
                elif char == "5":                 
                    sys.stdout.write("ↀ ")
                k += 1
        print()


# matrix soraihoz es oszlopaihoz inicializalt valtozok
i, j = 1, 1

# jatek inditasa es a labirintus kirajzolasa
print("\nControls: W, A, S, D.\nPress a button to start the game.\n")
getch.getch()                       # ennek a segitsegevel folyamatos a mozgas, nem kell mindig Entert leutni
matrix[1][1] = "2"                  # a 2-es (kor) kezdopozicioja
printmaze(matrix)                   # a labirintus kirajzolasa

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

    if matrix[i][j] == "4":         # az ellenseg melletti mezokon
        print("Don't touch the enemy!\n")

    if matrix[i][j] == "3":         # az ellensegre lepve
        print("You died!")
        exit()
    if matrix[i][j] == "5":
        turn += 310

    matrix[i][j] = "2"               # az eppen aktualis pozicio valtson 0-rol, 3-rol vagy 4-rol 2-re (korre)
    printmaze(matrix)
    pygame.mixer.music.play()       # hang lejatszasa

else:
    print("Congratulations! You managed to get out of the labyrinth!") # jatek vege