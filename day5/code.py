

class pantry:
    fresh_ranges = []
    ingredients = []
    merged_ranges = []

    def __init__(self, file: str):
        with open(file, "r") as data:
            for line in data.readlines():
                cleaned_str = line.strip()
                if len(cleaned_str) == 0:
                    continue
                split_str = cleaned_str.split('-')
                if len(split_str) == 2:
                    r = (int(split_str[0]), int(split_str[1]))
                    self.fresh_ranges.append(r)
                    self.merged_ranges.append(r)
                else:
                    self.ingredients.append(int(cleaned_str))
            self.merge()

    def merge(self):
        for outside, m in enumerate(self.merged_ranges):
            for inside, m2 in enumerate(self.merged_ranges):
                if outside == inside:
                    continue
                if m[0] >= m2[0] and m[0] <= m2[1]:
                    if m[1] >= m2[1]:
                        print("merged right")
                        self.merged_ranges[inside] = (m2[0], m[1])
                        self.merged_ranges[outside] = (0, 0)
                    else:
                        print("found smaller, erase range")
                        self.merged_ranges[outside] = (0, 0)
                elif m[0] <= m2[0] and m[1] >= m2[0] and m[1] <= m2[1]:
                    print("merged left")
                    self.merged_ranges[inside] = (m[0], m2[1])
                    self.merged_ranges[outside] = (0, 0)
                elif m[0] == m2[0] and m[1] == m2[1]:
                    print("found duplicate")
                    self.merged_ranges[inside] = (m[0], m[1])
                    self.merged_ranges[outside] = (0, 0)
        self.merged_ranges = [
            item for item in self.merged_ranges if item != (0, 0)]

    def __str__(self):
        retVal: str = 'Fresh Ingredient Ranges\n'

        for range in self.fresh_ranges:
            retVal += f"\t{range[0]} - {range[1]}\n"

        retVal += "\nMerged Ranges\n"
        for r in self.merged_ranges:
            retVal += f"\t{r[0]} - {r[1]}\n"

        retVal += "\nIngredients\n"

        for ingredient in self.ingredients:
            retVal += f"\t{ingredient}\n"
        return retVal

    def count_fresh_ingredients(self) -> int:
        count = 0
        for ingredient in self.ingredients:
            for range in self.merged_ranges:
                if ingredient >= range[0] and ingredient <= range[1]:
                    count += 1
                    break
        return count

    def count_fresh_ids(self) -> int:
        fresh_ids = 0
        for r in self.merged_ranges:
            if r != (0, 0):
                fresh_ids += r[1] - r[0] + 1

        return fresh_ids


my_pantry = pantry(file="day5/data.txt")
print(my_pantry)
print(f"fresh ingredients={my_pantry.count_fresh_ingredients()}")
print(f"fresh id's={my_pantry.count_fresh_ids()}")
