
position = 50
password = 0
password2 = 0

data = open("day1/data.txt", "r").readlines()

for line in data:
    original_position = position
    amount = 0
    movement = 0
    extra_movement = int(abs(int(line[1:])) / 100)

    # print(
    #    f"before Position: {position}")
    if line.startswith("L"):
        movement = -int(line[1:]) + extra_movement * 100
    elif line.startswith("R"):
        movement = int(line[1:]) - extra_movement * 100

    if position > 0 and position + movement < 0:
        amount += 1
    elif position + movement > 100:
        amount += 1

    password2 += amount + extra_movement

    position = original_position + movement

    position = position % 100

    if position == 0:
        password += 1
        password2 += 1

    print(
        f"ExtraMovement: {extra_movement}, Movement: {movement}, Original Position: {original_position}, New Position: {position}, amount: {amount}, password2: {password2}")


print(f"Password: {password}")
print(f"Password2: {password2}")


# * Left past 0
# * Left not past 0
# * Left stop at 0
# Left past 0 multiple times
# Left past 0 stop at 0
# * Right past 0
# * Right not past 0
# * Right stop at 0
# Right past 0 multiple times
# Right past 0 stop at 0
# from 0 Left past 0
# from 0 Left not past 0
# from 0 Left stop at 0
# from 0 Left past 0 multiple times
# from 0 Left past 0 stop at 0
# from 0 Right past 0
# from 0 Right not past 0
# from 0 Right stop at 0
# from 0 Right past 0 multiple times
# from 0 Right past 0 stop at 0
