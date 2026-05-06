

def count_adjacent(location: dict[int, dict[int, str]], y: int, x: int) -> int:
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


floor: dict[int, dict[int, str]] = {}

with open("day4/data.txt") as data:
    for y_index, line in enumerate(data.readlines()):
        floor[y_index] = {}
        for x_index, item in enumerate(line.strip()):
            floor[y_index][x_index] = item
    total_count = 0
    count = 1

    while count > 0:
        count = 0

        new_floor: dict[int, dict[int, str]] = {}

        for y in range(len(floor)):
            line = ''
            new_floor[y] = {}
            for x in range(len(floor[0])):
                if floor[y][x] == '@' and count_adjacent(floor, y, x) < 4:
                    count += 1
                    highlighted = '\033[43m' + '@' + '\033[0m'
                    line += highlighted
                    new_floor[y][x] = 'x'
                else:
                    line += floor[y][x]
                    new_floor[y][x] = floor[y][x]
            print(line)

        floor = new_floor

        print(f"removed {count}\n")
        total_count += count
    print(f"total_count={total_count}")
