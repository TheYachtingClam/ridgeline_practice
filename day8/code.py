from collections import deque
from math import sqrt, pow


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

    def find_distance(self, box: 'junction_box') -> int:
        return sqrt(
            pow(self.x - box.x, 2) +
            pow(self.y - box.y, 2) +
            pow(self.z - box.z, 2))


class Wire:
    box_one: junction_box
    box_two: junction_box
    distance: int

    def __init__(self, box1: junction_box, box2: junction_box):
        self.box_one = box1
        self.box_two = box2
        self.distance = box1.find_distance(box2)

    def __str__(self):
        return f'({self.box_one.x},{self.box_one.y},{self.box_one.z}),({self.box_two.x},{self.box_two.y},{self.box_two.z})[{self.distance}]'


class Circuit:
    boxes: dict[junction_box]

    def __init__(self):
        self.boxes = {}

    def __str__(self):
        return f'circuit length: {len(self.boxes)}'

    def add_wire(self, wire: Wire):
        self.boxes[wire.box_one] = 1
        self.boxes[wire.box_two] = 1

    def getCircuitLength(self):
        return len(self.boxes)

    def is_wire_in_circuit(self, wire: Wire) -> bool:
        if wire.box_one in self.boxes:
            return True
        if wire.box_two in self.boxes:
            return True
        return False

    def merge_circuit(self, circuit: 'Circuit'):
        for c in circuit.boxes:
            self.boxes[c] = 1


class pad:
    boxes: list[junction_box] = []
    circuits: list[Circuit] = []

    def __init__(self, file: int):
        with open(file, 'r') as data:
            for line in data.readlines():
                inp = line.strip().split(',')
                box = junction_box(
                    x=int(inp[0]), y=int(inp[1]), z=int(inp[2]))
                self.boxes.append(box)

    def __str__(self):
        val = 0
        for box in self.boxes:
            pass
            # print(box)
        for circuit in self.circuits:
            # print(circuit)
            val += circuit.getCircuitLength()
        return f'pad connected {val}/{len(self.boxes)}'

    def get_circuit_total(self):
        val = 0
        for circuit in self.circuits:
            val += circuit.getCircuitLength()
        return val

    def connect_shortest(self, amount: int, after: int):
        shortest: list[Wire] = []
        list_max = 0

        for outsidebox_index, outsidebox in enumerate(self.boxes):
            if outsidebox_index + 1 == len(self.boxes):
                continue
            for insidebox_index, insidebox in enumerate(self.boxes[outsidebox_index+1:]):
                if insidebox_index == outsidebox_index:
                    continue
                distance = outsidebox.find_distance(insidebox)
                # print(f'distance={distance}')
                if distance < after:
                    continue

                if len(shortest) < amount or distance < list_max:
                    w = Wire(outsidebox, insidebox)
                    shortest.append(w)
                    # print(f"adding {w}")

                    if len(shortest) > amount:
                        max_to_remove = max(
                            shortest, key=lambda wire: wire.distance)
                        # print(f"removing {max_to_remove}")
                        shortest.pop(shortest.index(max_to_remove))

                    list_max = max(
                        shortest, key=lambda wire: wire.distance).distance
        new_shortest = sorted(shortest, key=lambda wire: wire.distance)

        for short in new_shortest:
            # print(f'working on wire: {short}')
            wire_found = False
            circuits_wire_is_found_in = []
            for circuit in self.circuits:
                if circuit.is_wire_in_circuit(short):
                    circuits_wire_is_found_in.append(circuit)
                    wire_found = True

            if wire_found:
                if len(circuits_wire_is_found_in) >= 2:
                    new_circuit = Circuit()
                    for matched_circuit in circuits_wire_is_found_in:
                        new_circuit.merge_circuit(matched_circuit)
                        self.circuits.remove(matched_circuit)
                    new_circuit.add_wire(short)
                    self.circuits.append(new_circuit)
                else:
                    circuits_wire_is_found_in[0].add_wire(short)

            if not wire_found:
                new_circuit = Circuit()
                new_circuit.add_wire(short)
                self.circuits.append(new_circuit)

            if self.get_circuit_total() == len(self.boxes):
                print(
                    f'last wire found={short} total_circuits_connected={self.get_circuit_total()}')
                return (list_max, len(self.boxes) - self.get_circuit_total())

        val = 0
        for circuit in self.circuits:
            # print(circuit)
            val += circuit.getCircuitLength()

        return (list_max, len(self.boxes) - val)

    def find_shortest_connections(self, amount: int) -> list[Wire]:
        shortest: list[Wire] = []
        list_max = 0

        for outsidebox_index, outsidebox in enumerate(self.boxes):
            if outsidebox_index + 1 == len(self.boxes):
                continue
            for insidebox_index, insidebox in enumerate(self.boxes[outsidebox_index+1:]):
                if insidebox_index == outsidebox_index:
                    continue
                distance = outsidebox.find_distance(insidebox)
                # print(f'distance={distance}')

                if len(shortest) < amount or distance < list_max:
                    w = Wire(outsidebox, insidebox)
                    shortest.append(w)
                    # print(f"adding {w}")

                    if len(shortest) > amount:
                        max_to_remove = max(
                            shortest, key=lambda wire: wire.distance)
                        # print(f"removing {max_to_remove}")
                        shortest.pop(shortest.index(max_to_remove))

                    list_max = max(
                        shortest, key=lambda wire: wire.distance).distance

        for short in sorted(shortest, key=lambda wire: wire.distance):
            print(short)

        circuits: list[Circuit] = []
        for short in shortest:
            wire_found = False
            circuits_wire_is_found_in = []
            for circuit in circuits:
                if circuit.is_wire_in_circuit(short):
                    circuits_wire_is_found_in.append(circuit)
                    wire_found = True

            if wire_found:
                if len(circuits_wire_is_found_in) >= 2:
                    print("merging circuits")
                    new_circuit = Circuit()
                    for matched_circuit in circuits_wire_is_found_in:
                        new_circuit.merge_circuit(matched_circuit)
                        circuits.remove(matched_circuit)
                    new_circuit.add_wire(short)
                    circuits.append(new_circuit)
                else:
                    circuits_wire_is_found_in[0].add_wire(short)

            if not wire_found:
                new_circuit = Circuit()
                new_circuit.add_wire(short)
                circuits.append(new_circuit)

        b = []

        for circuit in circuits:
            print(circuit)
            b.append(circuit.getCircuitLength())

        j = sorted(b, reverse=True)

        print(f'sum:{j[0]*j[1]*j[2]}')
        print(j)

        return shortest


my_pad = pad('day8/data.txt')
print(my_pad)
# my_pad.find_shortest_connections(10)
m = my_pad.connect_shortest(10000, 0)
print(m)
print(my_pad)
