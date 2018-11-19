# labyrinth.py

import os
import sys
import getch
import contextlib
import subprocess
with contextlib.redirect_stdout(None):
    import pygame
    from random import randint

pygame.init()
pygame.mixer.music.load("pop.wav")

create = [sys.executable, "sub_file.py"]    # creating the credits


class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# text of menu
menu1 = "Please choose from the options:"
menu2 = "Let's play! (p)"
menu3 = "Credits (c)"
menu4 = "Quit (q)"

filename = bcolors.GREEN + """

                                                                     _           _                _       _   _
                                                                    | |         | |              (_)     | | | |
                                                                    | |     __ _| |__  _   _ _ __ _ _ __ | |_| |__
                                                                    | |    / _` | '_ \\| | | | '__| | '_ \\| __| '_ \\
                                                                    | |___| (_| | |_) | |_| | |  | | | | | |_| | | |
                                                                    |______\\__,_|_.__/ \\__, |_|  |_|_| |_|\\__|_| |_|
                                                                                        __/ |
                                                                                        |___/
                    """ + bcolors.ENDC


# creating a matrix from the given file
def load_matrix(file_name):
    maze = []                # the matrix goes here
    maze_file = open(file_name)     # opening the file

    # iterating through the file line by line
    for line in maze_file:
        line = line.strip()    # deleting whitespace from the end of line
        line = list(line)      # making a list out of a string line

        maze.append(line)    # putting the list (line) into the matrix

    # generating enemies
    for i in range(0, 6):
        # generating random coordinates (not on the edges)
        row = randint(1, len(maze) - 2)
        column = randint(1, len(maze[0]) - 2)

        # continue until an empty space is found
        while maze[row][column] != "0":
            row = randint(1, len(maze) - 2)
            column = randint(1, len(maze[0]) - 2)

        # if an empty space is found, put an enemy there (plus the enemies won't block the circle's path)
        if maze[row-1][column] != "3" and maze[row][column-1] != "3" and maze[row+1][column] != "3" and \
           maze[row][column+1] != "3" and maze[row-1][column-1] != "3" and maze[row-1][column+1] != "3" and \
           maze[row+1][column+1] != "3" and maze[row+1][column-1] != "3":
                maze[row][column] = "3"

        # surrounding the enemy with "fields next to the enemy" type fields
        if maze[row-1][column] == "0":
            maze[row-1][column] = "4"
        if maze[row][column-1] == "0":
            maze[row][column-1] = "4"
        if maze[row+1][column] == "0":
            maze[row+1][column] = "4"
        if maze[row][column+1] == "0":
            maze[row][column+1] = "4"

    return maze


# the matrix's elements are reachable from now based on rows and columns; e.g. top-left corner looks like matrix[0][0]
matrix = load_matrix("maze.txt")

# this variable makes sure that all of the characters won't get printed at once (just 310 of them)
maze_slice = 310


# definition for printing out the labyrinth and the moveable character
def printmaze(matrix):
    chars_count = 0     # counting the already printed characters

    for row in (matrix):
        for char in (row):
            if chars_count < maze_slice:
                if char == "0" or char == "4":    # empty spaces, fields next to the enemy
                    sys.stdout.write("  ")
                elif char == "1":                 # wall
                    sys.stdout.write("〠")
                elif char == "2":                 # moveable character (circle)
                    sys.stdout.write("◯ ")
                elif char == "3":                 # enemy
                    sys.stdout.write("⚉ ")
                elif char == "5":
                    sys.stdout.write("ↀ ")
                chars_count += 1
        print()


# variables initialized for the rows and columns of the matrix
row, column = 1, 1

# menu
print("%s \n %106s \n %+98s \n %+96s \n %+95s" % (filename, menu1, menu2, menu3, menu4))

user_input = ""

while user_input != "p" and user_input != "c" and user_input != "q":
    user_input = getch.getch()

    if user_input == "p":      # starting the game and printing out the maze
        os.system("clear")
        matrix[1][1] = "2"     # the circle's starting position
        printmaze(matrix)
    elif user_input == "c":    # credits
        subprocess.call(create)
        exit()
    elif user_input == "q":
        exit()
    else:
        print("Invalid input! Please enter \"p\", \"c\" or \"q\": ")

# implementing movement
while not (matrix[28][39] == "2" or matrix[29][39] == "2"):    # these two positions mean the exit of the labyrinth
    move = getch.getch()             # continuous movement, no pressing Enter needed
    print("\033[H\033[J")            # updating the screen

    matrix[row][column] = "0"        # this line makes sure that only one circle is present at once in the labyrinth

    if move == "a":    # move left = matrix[row][column-1] -> player is changing the column (-1), but not the row
        if matrix[row][column-1] != "1":    # if the circle does not arrive on a wall
            column = column - 1             # then print it out one position to the left
    if move == "s":
        if matrix[row+1][column] != "1":
            row = row + 1
    if move == "d":
        if matrix[row][column+1] != "1":
            column = column + 1
    if move == "w":
        if matrix[row-1][column] != "1":
            row = row - 1

    if matrix[row][column] == "4":
        print("Don't touch the enemy!\n")

    if matrix[row][column] == "3":
        tryagain = ""

        while tryagain != "y" and tryagain != "Y" and tryagain != "n" and tryagain != "N":
            tryagain = input("You died! Would you like to try again from where you failed before? (y/n)\n")

            if tryagain == "y" or tryagain == "Y":
                pass
            elif tryagain == "n" or tryagain == "N":
                exit()
            else:
                tryagain = input("Invalid input! Please enter \"y\" or \"n\": ")

    if matrix[row][column] == "5":
        maze_slice += 310

    matrix[row][column] = "2"    # change the actual position (0, 3 or 4) to 2 (the circle)
    printmaze(matrix)
    pygame.mixer.music.play()

else:
    print("Congratulations! You managed to get out of the labyrinth!")
