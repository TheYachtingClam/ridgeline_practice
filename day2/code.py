def is_invalid(d: str):
    if len(d) % 2 == 1:
        return False
    half_length = int(len(d)/2)

    for j in range(half_length):
        if d[j] != d[half_length+j]:
            return False
    return True


def is_invalid2(d: str):

    for cut_size in range(len(d)):
        if cut_size == 0 or len(d) % cut_size != 0:
            continue

        chunks = [d[i:i+cut_size] for i in range(0, len(d), cut_size)]
        current_val = True
        for chunk in chunks:
            if chunk != chunks[0]:
                current_val = False
        if current_val:
            return current_val


data = open("day2/data.txt", "r").readline()

invalid_ids = []

for r in data.split(','):
    low = int(r.split('-')[0])
    high = int(r.split('-')[1])

    for bob in range(low, high+1):
        if is_invalid2(str(bob)):
            invalid_ids.append(bob)
            print(f"{bob} is invalid")

    id_val = 0
    for frank in invalid_ids:
        id_val += frank

print(f"final val = {id_val}")
