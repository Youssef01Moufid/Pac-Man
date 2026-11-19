import json

class HighScoreManager:
    """ Manager Score """
    MAX_ENTRIES = 10

    def __init__(
        self,
        path: str
    ) -> None:
        """ Initialize the  highescoreManger """
        self.path = path
        self._entries: list[tuple[str, int]] = []
    

    def load(self) -> None:
        """ load the data inside the path file """
        try:
            with open(self.path, 'r') as f:
                data = json.load(f)
            for element in data:
                if not element['name']:
                    continue
                if element['score'] < 0:
                    continue
                name, score = element['name'], element['score']
                self._entries.append((name, score))

        except FileNotFoundError:
            with open(self.path, 'w') as f:
                json.dump(self._entries, f)
        except OSError:
            print("error OS")
        except json.JSONDecodeError:
            print("Error json")
    
    def add(self, name: str, score) -> None:
        self._entries.append((name, score))
        self._entries = sorted(self._entries, key=lambda e: e[1], reverse=True)[:10]


    def save(self) -> None:
        list_to_save = []
        for name, score in self._entries:
            list_to_save.append({
                "name": name,
                "score": score
            })
        try:
            with open(self.path, 'w') as f:
                json.dump(list_to_save, f)
        except OSError:
            print("OS Error")

    @property
    def entries(self):
        return list(self._entries)




if __name__ == "__main__":

    my_highsores = HighScoreManager("highscores.json")
    my_highsores.load()
    print(my_highsores.entries)