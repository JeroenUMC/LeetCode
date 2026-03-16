import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    import random

    return (random,)


@app.cell
def _(random):
    class RandomizedSet:

        def __init__(self):
            self.set: set[int] = set()

        def insert(self, val: int) -> bool:
            val_in_set = val in self.set
            if not val_in_set:
                self.set.add(val)
            return not val_in_set

        def remove(self, val: int) -> bool:
            val_in_set = val in self.set
            if val_in_set:
                self.set.remove(val)
        
            return val_in_set

        def getRandom(self) -> int:
            return random.choice(list(self.set))

    return (RandomizedSet,)


@app.cell
def _(RandomizedSet):
    sol = RandomizedSet()

    print(sol.insert(1))

    print(sol.insert(1))
    return


if __name__ == "__main__":
    app.run()
