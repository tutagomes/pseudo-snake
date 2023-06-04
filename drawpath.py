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
        grid[pos[0]][pos[1]] = i + 1

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
    path = [[5, 3], [4, 3], [4, 2], [3, 2], [2, 2], [2, 1], [2, 0], [3, 0], [3, 1], [4, 1], [4, 0], [5, 0], [5, 1], [5, 2], [6, 2], [6, 1], [6, 0], [7, 0], [8, 0], [9, 0], [9, 1], [9, 2], [9, 3], [9, 4], [9, 5], [8, 5], [8, 6], [9, 6], [9, 7], [8, 7], [8, 8], [9, 8], [9, 9], [8, 9], [7, 9], [6, 9], [5, 9], [5, 8], [6, 8], [7, 8], [7, 7], [6, 7], [6, 6], [7, 6], [7, 5], [7, 4], [8, 4], [8, 3], [8, 2], [8, 1], [7, 1], [7, 2], [7, 3], [6, 3], [6, 4], [6, 5], [5, 5], [4, 5], [4, 6], [5, 6], [5, 7], [4, 7], [4, 8], [4, 9], [3, 9], [2, 9], [1, 9], [0, 9], [0, 8], [1, 8], [2, 8], [3, 8], [3, 7], [2, 7], [2, 6], [3, 6], [3, 5], [2, 5], [2, 4], [1, 4], [1, 5], [1, 6], [1, 7], [0, 7], [0, 6], [0, 5], [0, 4], [0, 3], [0, 2], [0, 1], [0, 0], [1, 0], [1, 1], [1, 2], [1, 3], [2, 3], [3, 3], [3, 4], [4, 4], [5, 4]]
    draw_path(int(math.sqrt(len(path))), path , []) 
