
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


my_tachyon = tachyon("day7/data.txt")
print(my_tachyon)
