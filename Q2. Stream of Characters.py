import marimo

__generated_with = "0.20.4"
app = marimo.App()


@app.cell
def _():
    from typing import List, Dict, Any

    return Any, Dict, List


@app.cell
def _(Any, Dict, List):
    class StreamChecker:

        def __init__(self, words: List[str]):
            self.word_graph = self.build_word_graph(words)
            self.stream: List[str] = []
        
        def build_word_graph(self, words: List[str]) -> Dict[str, Any]:
            nodes: Dict[int, Dict[str, Any]] = {
                0: {"char": None, "children": {}, "is_word_start": False}  # root
            }
            next_id = 1

            for word in words:
                if not word:  # skip empty strings
                    continue

                current = 0
                # Insert reversed words to match suffixes of the stream quickly.
                for ch in reversed(word):
                    children = nodes[current]["children"]
                    if ch not in children:
                        children[ch] = next_id
                        nodes[next_id] = {"char": ch, "children": {}, "is_word_start": False}
                        next_id += 1
                    current = children[ch]

                nodes[current]["is_word_start"] = True

            return {"root_id": 0, "nodes": nodes}

        def query(self, letter: str) -> bool:
            self.stream.append(letter)

            nodes = self.word_graph["nodes"]
            current = self.word_graph["root_id"]

            # Walk backward through the stream, following reversed-word trie edges.
            for ch in reversed(self.stream):
                children = nodes[current]["children"]
                if ch not in children:
                    return False

                current = children[ch]
                if nodes[current].get("is_word_start", False):
                    return True

            return False


    return (StreamChecker,)


@app.cell
def _(StreamChecker):
    words = ["abc", "xyz"]
    streamchecker = StreamChecker(words)
    return (streamchecker,)


@app.cell
def _(streamchecker):
    streamchecker.word_graph
    return


if __name__ == "__main__":
    app.run()
