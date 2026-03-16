import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    import random

    return (random,)


@app.cell
def _(random):
    class RandomizedCollection:

        def __init__(self):
            self.values: list[int] = []
            self.indices: dict[int, set[int]] = {}

        def insert(self, val: int) -> bool:
            val_in_collection = val in self.indices and len(self.indices[val]) > 0
            if val not in self.indices:
                self.indices[val] = set()

            self.values.append(val)
            self.indices[val].add(len(self.values) - 1)
            return not val_in_collection

        def remove(self, val: int) -> bool:
            if val not in self.indices or len(self.indices[val]) == 0:
                return False

            remove_idx = self.indices[val].pop()
            last_idx = len(self.values) - 1
            last_val = self.values[last_idx]

            if remove_idx != last_idx:
                self.values[remove_idx] = last_val
                self.indices[last_val].remove(last_idx)
                self.indices[last_val].add(remove_idx)

            self.values.pop()

            if len(self.indices[val]) == 0:
                del self.indices[val]

            return True

        def getRandom(self) -> int:
            return random.choice(self.values)

    return


@app.cell
def _(random):
    temp = {7:3, 8:2}

    print(temp)
    print(temp.values())
    print(temp.keys())

    random.choices(population=list(temp.keys()),weights = list(temp.values()))[0]
    return


if __name__ == "__main__":
    app.run()
