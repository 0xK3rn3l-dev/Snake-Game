from snake import StandardSnake, GoldenSnake, RedSnake

SNAKES = [
    StandardSnake,
    GoldenSnake,
]

def create_snake(index, positions, cell_size):
    snake_class = SNAKES[index]
    return snake_class(positions, cell_size)