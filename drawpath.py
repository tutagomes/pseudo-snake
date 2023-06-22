import matplotlib.pyplot as plt
import numpy as np
import math 

def draw_path(grid_size, path, blocked = []):
    # create a grid with all zeros
    grid = np.zeros((grid_size, grid_size))

    # mark the blocked positions with -1
    for block in blocked:
        grid[block[0]][block[1]] = -1

    # mark the path positions with their order in the path
    for i, pos in enumerate(path):
        grid[int(pos[0])][int(pos[1])] = i + 1

    # create a color map for the grid
    colors = ["white"]
    cmap = plt.cm.colors.ListedColormap(colors)

    # plot the grid
    plt.figure(2)
    plt.figure(figsize=(grid_size, grid_size))
    plt.imshow(grid, cmap=cmap)

    # add the numbers
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] > 0:
                plt.text(j, i, int(grid[i][j]), ha='center', va='center', color='blue')

    plt.title('Best Path')
    plt.show()
    #plt.savefig('foo.png')


if __name__ == '__main__':
    path = np.loadtxt('./cycles/30_1.0')

    draw_path(int(math.sqrt(len(path))), path , []) 
