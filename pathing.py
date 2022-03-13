import csv
import pygame
import sys
def load_cells(): #Loads the cells file. Should only be run once per game launch.
    cells = list(csv.reader(open('maze.csv',"r")))[1:]# ignore header line
    #cell_name = cells[node_x][node_y] # 0th elemnt of 0th cell
    #x = int(cell_name.split(",")[0].lstrip('(')) # extract x position from cell name
    #y = int(cell_name.split(",")[1].rstrip(')')) # extract y position
    return cells

def draw_maze(screen_info, cells):  #This draws the maze based on the cells inputed.
    x = 0
    y = 0
    size = 100
    line_colour = (0, 255, 0, 1)
    line_alt_col = (0, 0, 0, 1)
    line_width = 4
    for cell in cells:
        if len(cell) >= 1:
            if cell[1] == "0":
                #print(str(cell[0]) + ": ", cell[1])
                pygame.draw.line(screen_info["screen"], line_colour, (x + size, y), (x + size, y + size), line_width)
            if cell[2] == "0":
                #print(str(cell[0]) + ": ", cell[2])
                pygame.draw.line(screen_info["screen"], line_colour, (x, y), (x, y + size), line_width)
            if cell[3] == "0":
                #print(str(cell[0]) + ": ", cell[3])
                pygame.draw.line(screen_info["screen"], line_colour, (x, y), (x + size, y), line_width)
            if cell[4] == "0":
                #print(str(cell[0]) + ": ", cell[4])
                pygame.draw.line(screen_info["screen"], line_colour, (x, y + size), (x + size, y + size), line_width)
            y += size
            if y >= screen_info["width"]:
                y = 0
                x += size
            if x >= screen_info["height"]:
                x = 0
                y = 0

def check_next_node(direction, cells, node_x, node_y):
    player_x = node_x - 1
    player_y = node_y - 1
    current_cell = 10 * player_x
    current_cell = current_cell + player_y
    #print("X = " + str(node_x) + " | Y = " + str(node_y) + "\nCurrent Cell = " + str(current_cell))
    if direction == 0:
        if cells[current_cell][1] == "1":
            return True
        else:
            return False
    if direction == 90:
        if cells[current_cell][3] == "1":
            return True
        else:
            return False
    if direction == 180:
        if cells[current_cell][2] == "1":
            return True
        else:
            return False
    if direction == 270:
        if cells[current_cell][4] == "1":
            return True
        else:
            return False

def cells_converter(cells):
    cell_dict = {}
    cell_list = []
    x = 0
    while x <= 99:
        if cells[x][1] == "1":
            x_temp = x + 10
            if x_temp > 99:
                x_temp = x_temp - 100
            cell = str(cells[x_temp][0].replace("(", ""))
            cell = cell.replace(")", "")
            cell_list.append(cell)
        if cells[x][2] == "1":
            cell = str(cells[x - 10][0].replace("(", ""))
            cell = cell.replace(")", "")
            cell_list.append(cell)
        if cells[x][3] == "1":
            cell = str(cells[x - 1][0].replace("(", ""))
            cell = cell.replace(")", "")
            cell_list.append(cell)
        if cells[x][4] == "1":
            x_temp = x + 1
            if x_temp > 99:
                x_temp = x_temp - 100
            cell = str(cells[x_temp][0].replace("(", ""))
            cell = cell.replace(")", "")
            cell_list.append(cell)
        if cell_dict.get(str(cells[x][0])) is not None:
            cell_dict[str(cells[x][0])] = cell_dict[str(cells[x][0])] + cell_list
        else:
            cell_dict[str(cells[x][0])] = cell_list
        cell_list = []
        x += 1
        if x > 99:
            break
    return cell_dict

def path_find(cells, node_x, node_y, player_node_x, player_node_y):
    queue = [[str(node_y) + ", " + str(node_x)]]
    destination = str(player_node_x) + ", " + str(player_node_y)
    visited = []
    while len (queue) > 0:
        path = queue.pop(0)
        node = path[-1]
        node = "(" + node + ")"
        if node not in visited:
            for neighbour in cells[node]:
                new_path = path.copy()
                new_path.append(neighbour)
                if neighbour == destination:
                    return new_path
                queue.append(new_path)
            visited.append(node)

def cell_number_calc(y, x, debug):
    if debug is True:
        print("(cell_number_calc): Input y = " + str(y) + " | Input x = " + str(x))
    y -= 1
    if debug is True:
        print("(cell_number_calc): y = " + str(y))
    x -= 1
    if debug is True:
        print("(cell_number_calc): x = " + str(x))
    cell_number = 10 * x
    if debug is True:
        print("(cell_number_calc): cell_number = 10 * " + str(x) + " = " + str(cell_number))
    cell_number = cell_number + y
    if debug is True:
        print("(cell_number_calc): cell_number = cell_number + " + str(y) + " = " + str(cell_number))
    return cell_number
