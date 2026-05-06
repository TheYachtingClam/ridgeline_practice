

class pantry:
    fresh_ranges = []
    ingredients = []

    def __init__(self, file: str):
        with open(file, "r") as data:
            for line in data.readlines():
                cleaned_str = line.strip()
                if len(cleaned_str) == 0:
                    continue
                split_str = cleaned_str.split('-')
                if len(split_str) == 2:
                    self.fresh_ranges.append(
                        (int(split_str[0]), int(split_str[1])))
                else:
                    self.ingredients.append(int(cleaned_str))

    def __str__(self):
        retVal: str = 'Fresh Ingredient Ranges\n'

        for range in self.fresh_ranges:
            retVal += f"\t{range[0]} - {range[1]}\n"

        retVal += "\nIngredients\n"

        for ingredient in self.ingredients:
            retVal += f"\t{ingredient}\n"
        return retVal

    def count_fresh_ingredients(self) -> int:
        count = 0
        for ingredient in self.ingredients:
            for range in self.fresh_ranges:
                if ingredient >= range[0] and ingredient <= range[1]:
                    count += 1
                    break
        return count


my_pantry = pantry(file="day5/data.txt")
print(my_pantry)
print(f"fresh ingredients={my_pantry.count_fresh_ingredients()}")
