

def count_adjacent(location: dict[int, dict[int, bool]], y: int, x: int) -> int:
    count = 0
    if y != 0 and x != 0 and location[y - 1][x-1] == '@':
        count += 1
    if y != 0 and location[y - 1][x] == '@':
        count += 1
    if y != 0 and x != len(location[0])-1 and location[y - 1][x+1] == '@':
        count += 1
    if x != 0 and location[y][x-1] == '@':
        count += 1
    if x != len(location[0])-1 and location[y][x+1] == '@':
        count += 1
    if y != len(location)-1 and x != 0 and location[y + 1][x-1] == '@':
        count += 1
    if y != len(location)-1 and location[y + 1][x] == '@':
        count += 1
    if y != len(location)-1 and x != len(location[0])-1 and location[y + 1][x+1] == '@':
        count += 1
    return count


floor: dict[int, dict[int, bool]] = {}

with open("day4/data.txt") as data:
    for y_index, line in enumerate(data.readlines()):
        floor[y_index] = {}
        for x_index, item in enumerate(line.strip()):
            floor[y_index][x_index] = item

    count = 0
    for y in range(len(floor)):

        line = ''
        for x in range(len(floor[0])):
            if floor[y][x] == '@' and count_adjacent(floor, y, x) < 4:
                count += 1
                line += 'x'
            else:
                line += floor[y][x]
        print(line)

    print(f"count={count}")
