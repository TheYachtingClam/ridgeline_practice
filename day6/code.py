
class problem:
    _numbers: list[int] = []
    _action: str

    def __init__(self, numbers: list[int], action: str):
        self._numbers = numbers
        self._action = action

    def __str__(self):
        ret_val: str = ''
        for index, num in enumerate(self._numbers):
            if index == 0:
                ret_val += f'- {num} '
            else:
                ret_val += f'{self._action} {num} '
        ret_val += f' = {self.solve()}'
        return ret_val

    def solve(self) -> int:
        ret_val: int
        if self._action == '+':
            ret_val = 0
        if self._action == '*':
            ret_val = 1
        for num in self._numbers:
            if self._action == '+':
                ret_val += num
            else:
                ret_val *= num
        return ret_val


class homework:

    problems: list[problem] = []

    def __init__(self, file: str):
        with open(file, 'r') as data:
            num_input: list[list[int]] = []
            actions: list[str]

            for line in data.readlines():
                split_line = line.strip().split()
                if str.isnumeric(split_line[0]):
                    num_input.append(split_line)
                else:
                    actions = split_line

            for index, _ in enumerate(num_input[0]):
                inp: list[int] = []
                for li in num_input:
                    inp.append(int(li[index]))
                self.problems.append(
                    problem(numbers=inp,  action=actions[index]))

    def __str__(self):
        ret_val: str = ''

        for prob in self.problems:
            ret_val += f'{prob}\n'

        return ret_val

    def total(self) -> int:
        total: int = 0

        for prob in self.problems:
            total += prob.solve()
        return total


my_homework = homework('day6/data.txt')
print(my_homework)
print(f"total={my_homework.total()}")
