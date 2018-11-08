#labyrinth.py

import os, sys, getch, contextlib, subprocess
with contextlib.redirect_stdout(None):
    import pygame
    from random import randint

    pygame.init()
    pygame.mixer.music.load("pop.wav")
    create = [sys.executable, 'sub_file.py']
    class bcolors:
        PURPLE = '\033[95m'
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'



    filename3 = "mazo.txt"
    header1 =" Please choose from the options."
    header2 = " Player vs. Player (w)"
    header3 = "Player vs. Computer (2)"
    header4 = "Quit (3)"
    header5 = "Credits (C)"
    filename2 = bcolors.GREEN + """

                                                                         _           _                _       _   _     
                                                                        | |         | |              (_)     | | | |    
                                                                        | |     __ _| |__  _   _ _ __ _ _ __ | |_| |__  
                                                                        | |    / _` | '_ \| | | | '__| | '_ \| __| '_ \ 
                                                                        | |___| (_| | |_) | |_| | |  | | | | | |_| | | |
                                                                        |______\__,_|_.__/ \__, |_|  |_|_| |_|\__|_| |_|
                                                                                            __/ |                       
                                                                                            |___/                        
                    """ + bcolors.ENDC














maze_slice = 310     # ennek a valtozonak a segitsegevel nem lesz printelve az osszes karakter egyszerre (csak 310)

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
matrix = matrix_file("maze.txt")

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

# jatek inditasa es a labirintus kirajzolasa
print("%s \n %110s \n %+105s \n %+105s \n %+98s \n %+98s " % (filename2,header1,header2,header3,header4,header5))
getch.getch()
os.system('clear')                    # ennek a segitsegevel folyamatos a mozgas, nem kell mindig Entert leutni
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
    if move == "c":
        subprocess.call(create)
    
    
    
            

    if matrix[i][j] == "4":
        print("Don't touch the enemy!\n")

    if matrix[i][j] == "3":
        print("You died!")
        exit()

    if matrix[i][j] == "5":
        maze_slice += 310


    matrix[i][j] = "2"               # az eppen aktualis pozicio valtson 0-rol, 3-rol vagy 4-rol 2-re (korre)
    printmaze(matrix)
    pygame.mixer.music.play()

else:
    print("Congratulations! You managed to get out of the labyrinth!")

def exit_program():
   while True:
        for e in pygame.event.get():
            if e.type == QUIT or e.type == KEYDOWN and e.key == pygame.K_ESCAPE:
                exit_program()
                