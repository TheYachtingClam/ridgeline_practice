
class tachyon:
    manifolds: dict[dict[int, str]] = {}

    def __init__(self, file: str):
        with open(file, 'r') as data:
            for outside_index, line in enumerate(data.readlines()):
                self.manifolds[outside_index] = {}
                for inside_index, item in enumerate(line.strip()):
                    self.manifolds[outside_index][inside_index] = item

    def __str__(self):
        ret_val: str = ''
        for line in sorted(self.manifolds):
            for i in sorted(self.manifolds[line]):
                ret_val += self.manifolds[line][i]
            ret_val += '\n'
        return ret_val

    def split(self) -> int:
        splits = 0
        current_beams: dict[int, int] = {}

        for y in sorted(self.manifolds):
            for x in sorted(self.manifolds[y]):
                if self.manifolds[y][x] == 'S':
                    current_beams[x] = 1
                elif self.manifolds[y][x] == '^':
                    if x in current_beams:
                        if x+1 in current_beams:
                            current_beams[x + 1] += current_beams[x]
                        else:
                            current_beams[x + 1] = current_beams[x]
                        if x-1 in current_beams:
                            current_beams[x - 1] += current_beams[x]
                        else:
                            current_beams[x - 1] = current_beams[x]

                        del current_beams[x]
                        splits += 1
                        print(f'split at [y,x]=[{y},{x}]')
            print(
                f'current={[f"{item}[{current_beams[item]}]" for item in sorted(current_beams)]}')
            print(f'splits={splits}')
            print(
                f'universes={sum([current_beams[item] for item in current_beams])}')
        return splits


my_tachyon = tachyon("day7/data.txt")
print(my_tachyon)
print(f'split={my_tachyon.split()}')
