
class junction_box:
    x: int
    y: int
    z: int

    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f'({self.x},{self.y},{self.z})'


class pad:
    circuits: list[list[junction_box]] = []

    def __init__(self, file: int):
        with open(file, 'r') as data:
            for line in data.readlines():
                inp = line.strip().split(',')
                circuit = [junction_box(
                    x=int(inp[0]), y=int(inp[1]), z=int(inp[2]))]
                self.circuits.append(circuit)

    def __str__(self):
        ret_val: int = ''
        for circuit in self.circuits:
            ret_val += '['
            for box in circuit:
                ret_val += f'{box}'
            ret_val += ']\n'
        return ret_val


my_pad = pad('day8/test.txt')
print(my_pad)
