from snake import StandardSnake, GoldenSnake, RedSnake
# here will be more snakes i mean colors snakes

SNAKES = [
    StandardSnake,
    GoldenSnake,
]

def create_snake(index, positions, cell_size):
    snake_class = SNAKES[index]
    return snake_class(positions, cell_size)