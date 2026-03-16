import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    from typing import List,Self,Any

    return Any, List


@app.cell
def _(Any, List):
    class interval(list):
        def __init__(self,start: Any, end: Any):
            super().__init__([int(start),int(end)])

    def neighbours(value: int) -> list[int]:
        return [value-1,value+1]

    class SummaryRanges:

        def __init__(self):
            self.arr: List[int] =  []
            self.intervals: List[interval] = []

        def get_interval(self,value:int, from_left: bool) -> interval | None:
            # search [0] in all intervals if from_left. Else search all [1]
            index = 0 if from_left else 1
            for inter in self.intervals:
                if inter[index] == value:
                    return inter 
            return None

        def update_intervals(self,value:int):
            neighs = neighbours(value)
            neigh_0 = neighs[0]
            neigh_1 = neighs[1]

            left_interval = self.get_interval(neigh_0, from_left = False)
            right_interval = self.get_interval(neigh_1, from_left = True)
        
            if left_interval != None and right_interval != None:
                new_interval = interval(left_interval[0],right_interval[1])
                self.intervals.remove(left_interval)
                self.intervals.remove(right_interval)
            elif left_interval != None:
                new_interval = interval(left_interval[0],value)
                self.intervals.remove(left_interval)
            elif right_interval != None:
                new_interval = interval(value,right_interval[1])
                self.intervals.remove(right_interval)
            else:
                new_interval = interval(value,value)
            self.intervals.append(new_interval)
    
        def addNum(self, value: int) -> None:
            if value in self.arr:
                return
            self.arr.append(value)
            self.update_intervals(value)

        def getIntervals(self) -> List[interval]:
            return sorted(self.intervals)


    return (SummaryRanges,)


@app.cell
def _(SummaryRanges):
    solution = SummaryRanges()

    solution.addNum(5)
    print(solution.intervals)

    solution.addNum(6)
    print(solution.intervals)

    solution.addNum(8)
    print(solution.intervals)

    solution.addNum(7)
    print(solution.intervals)

    print(solution.getIntervals())
    return


if __name__ == "__main__":
    app.run()
