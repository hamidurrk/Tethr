import pygame as pg
from random import random

fps = 120

def get_rect(x, y):
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2


def get_next_nodes(x, y):
    check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows and not grid[y][x] else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]


def heuristic(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])


cols, rows = 250, 150
TILE = 6

pg.init()
sc = pg.display.set_mode([cols * TILE, rows * TILE])
clock = pg.time.Clock()
# grid
grid = [[1 if random() < 0.2 else 0 for col in range(cols)] for row in range(rows)]
# dict of adjacency lists
graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        if not col:
            graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)

# A* settings
start = (0, 0)
goal = (cols-1, rows-1)
open_set = [(start, heuristic(start, goal))]
visited = set()
came_from = {}

while open_set:
    # Sort the open set by the heuristic
    open_set.sort(key=lambda x: x[1])
    current, _ = open_set.pop(0)

    if current == goal:
        break

    visited.add(current)
    try: 
        for neighbor in graph[current]:
            if neighbor not in visited:
                if (neighbor, heuristic(neighbor, goal)) not in open_set:
                    open_set.append((neighbor, heuristic(neighbor, goal)))
                    came_from[neighbor] = current
    except Exception as e:
        print("Can't move")
        pass

    # fill screen
    sc.fill(pg.Color('black'))
    # draw grid
    [[pg.draw.rect(sc, pg.Color('forestgreen'), get_rect(x, y), border_radius=TILE // 5)
      for x, col in enumerate(row) if col] for y, row in enumerate(grid)]
    # draw A* work
    [pg.draw.rect(sc, pg.Color('purple'), get_rect(x, y)) for x, y in visited]
    [pg.draw.rect(sc, pg.Color('darkslategray'), get_rect(x, y)) for (x, y), _ in open_set]
    pg.draw.rect(sc, pg.Color('red'), get_rect(*start), border_radius=TILE // 3)
    pg.draw.rect(sc, pg.Color('blue'), get_rect(*goal), border_radius=TILE // 3)

    # draw path
    for node in visited:
        pg.draw.rect(sc, pg.Color('white'), get_rect(*node), TILE, border_radius=TILE // 3)
    
    # pygame necessary lines
    [exit() for event in pg.event.get() if event.type == pg.QUIT]
    pg.display.flip()
    clock.tick(fps)

# Reconstruct path
path = []
current = goal
while current != start:
    path.append(current)
    current = came_from[current]
path.append(start)
path.reverse()

while True:
    # fill screen
    sc.fill(pg.Color('black'))
    # draw grid
    [[pg.draw.rect(sc, pg.Color('forestgreen'), get_rect(x, y), border_radius=TILE // 5)
      for x, col in enumerate(row) if col] for y, row in enumerate(grid)]
    # draw A* work
    [pg.draw.rect(sc, pg.Color('black'), get_rect(x, y)) for x, y in visited]
    [pg.draw.rect(sc, pg.Color('darkslategray'), get_rect(x, y)) for (x, y), _ in open_set]

    # draw path
    for node in path:
        pg.draw.rect(sc, pg.Color('white'), get_rect(*node), TILE, border_radius=TILE // 3)
    pg.draw.rect(sc, pg.Color('red'), get_rect(*start), border_radius=TILE // 3)
    pg.draw.rect(sc, pg.Color('blue'), get_rect(*goal), border_radius=TILE // 3)
    # pygame necessary lines
    [exit() for event in pg.event.get() if event.type == pg.QUIT]
    pg.display.flip()
    clock.tick(fps)
