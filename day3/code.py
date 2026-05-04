from collections import deque
from math import pow


def get_joltage2(bank: str, amount: int) -> int:
    total = 0
    last_digit = 0
    last_place = 0
    last_multiplier = pow(10, amount - 1)
    working_bank = bank

    for place in range(amount):
        if amount - place - 1 == 0:
            active_search_area = working_bank
        else:
            active_search_area = working_bank[:-(amount-place-1)]
        # print(f"active_search_area={active_search_area}")
        for index, digit in enumerate(active_search_area):
            if int(digit) > last_place:
                last_place = int(digit)
                last_digit = index

        # print(f"remaining string={working_bank[last_digit+1:]}")
        working_bank = working_bank[last_digit+1:]
        total += last_place * last_multiplier
        last_digit = 0
        last_place = 0
        last_multiplier /= 10

    return total


def get_joltage(bank: str, num_batteries: int) -> int:
    joltage_str = ""
    joltage_dict: dict[int, int] = {}

    for digit in bank:
        if not str.isdigit(digit):
            continue

        if digit not in joltage_dict:
            joltage_dict[digit] = 1
        else:
            joltage_dict[digit] += 1

    queue = deque()
    for digit in sorted(joltage_dict, reverse=True):
        for i in range(joltage_dict[digit]):
            queue.append(digit)

    for use_digit in range(num_batteries):
        joltage_str += str(queue.popleft())

    return int(joltage_str)


data = open("day3/data.txt", "r").readlines()

joltage_total = 0

for bank in data:
    joltage = get_joltage2(bank.strip(), 12)
    print(f"joltage={joltage}")
    joltage_total += joltage


print(f"joltage_total={joltage_total}")
