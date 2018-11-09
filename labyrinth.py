#labyrinth.py

import os, sys, getch, contextlib, subprocess
with contextlib.redirect_stdout(None):
    import pygame
    from random import randint

pygame.init()
pygame.mixer.music.load("pop.wav")

create = [sys.executable, "sub_file.py"]     # stablista letrehozasa

class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# menu szovege
menu1 = "Please choose from the options:"
menu2 = "Let's play! (p)"
menu3 = "Credits (c)"
menu4 = "Quit (q)"

filename = bcolors.GREEN + """

                                                                         _           _                _       _   _     
                                                                        | |         | |              (_)     | | | |    
                                                                        | |     __ _| |__  _   _ _ __ _ _ __ | |_| |__  
                                                                        | |    / _` | '_ \| | | | '__| | '_ \| __| '_ \ 
                                                                        | |___| (_| | |_) | |_| | |  | | | | | |_| | | |
                                                                        |______\__,_|_.__/ \__, |_|  |_|_| |_|\__|_| |_|
                                                                                            __/ |                       
                                                                                            |___/                        
                    """ + bcolors.ENDC

# matrix keszitese a megadott fajlbol
def load_matrix(file_name):
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

        # ha megvan, odateszunk egy ellenseget (plusz biztositva van, hogy az ellensegek ne zarjak el az utat)
        if m[x-1][y] != "3" and m[x][y-1] != "3" and m[x+1][y] != "3" and m[x][y+1] != "3" and m[x-1][y-1] != "3" and m[x-1][y+1] != "3" and m[x+1][y+1] != "3" and m[x+1][y-1] != "3":
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
matrix = load_matrix("maze.txt")

# ennek a valtozonak a segitsegevel nem lesz printelve az osszes karakter egyszerre (csak 310)
maze_slice = 310

# labirintus es mozgathato karakter kirajzolasahoz fuggveny
def printmaze(matrix):
    chars_count = 0     # kirajzolt karakterek megszamolasa

    for row in (matrix):
        for char in (row):
            if chars_count < maze_slice:
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
                chars_count += 1
        print()

# matrix soraihoz es oszlopaihoz inicializalt valtozok
i, j = 1, 1

# menu
print("%s \n %110s \n %+102s \n %+100s \n %+99s" % (filename, menu1, menu2, menu3, menu4))

user_input = ""

while user_input != "p" and user_input != "c" and user_input != "q":
    user_input = getch.getch()

    if user_input == "p":                   # jatek inditasa es a labirintus kirajzolasa
        os.system("clear")
        matrix[1][1] = "2"                  # a 2-es (kor) kezdopozicioja
        printmaze(matrix)
    elif user_input == "c":                 # stablista
        subprocess.call(create)
        exit()
    elif user_input == "q":
        exit()
    else:
        print("Invalid input! Please enter \"p\", \"c\" or \"q\": ")

# mozgas implementalasa
while not (matrix[28][39] == "2" or matrix[29][39] == "2"): # ez a ket pozicio a labrinitus kijaratat jelenti
    move = getch.getch()            # ennek a segitsegevel folyamatos a mozgas, nem kell mindig Entert leutni
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
        tryagain = ""

        while tryagain != "y" and tryagain != "Y" and tryagain != "n" and tryagain != "N":
            tryagain = input("You died! Would you like to try again from where you failed before? (y/n)\n")

            if tryagain == "y" or tryagain == "Y":
                pass
            elif tryagain == "n" or tryagain == "N":
                exit()
            else:
                tryagain = input("Invalid input! Please enter \"y\" or \"n\": ")

    if matrix[i][j] == "5":
        maze_slice += 310

    matrix[i][j] = "2"               # az eppen aktualis pozicio valtson 0-rol, 3-rol vagy 4-rol 2-re (korre)
    printmaze(matrix)
    pygame.mixer.music.play()

else:
    print("Congratulations! You managed to get out of the labyrinth!")

