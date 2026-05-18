
class Playground:
    red_tiles: list = []

    def __init__(self, file: str):
        with open(file, 'r') as data:
            for line in data.readlines():
                sp = line.strip().split(',')
                self.red_tiles.append((int(sp[0]), int(sp[1])))

    def __str__(self):
        ret_val = ''
        for tile in self.red_tiles:
            ret_val += f'{tile[0], tile[1]}\n'
        return ret_val

    def find_biggest(self) -> int:
        largest_size = 0
        for outsidetile_index, outsidetile in enumerate(self.red_tiles):
            if outsidetile_index + 1 == len(self.red_tiles):
                continue
            for insidetile_index, insidetile in enumerate(self.red_tiles[outsidetile_index+1:]):

                size = (abs(outsidetile[0] - insidetile[0]) + 1) * \
                    (abs(outsidetile[1] - insidetile[1]) + 1)
                if size > largest_size:
                    largest_size = size
        return largest_size


playground = Playground('day9/data.txt')
print(playground)
print(f'biggest: {playground.find_biggest()}')
