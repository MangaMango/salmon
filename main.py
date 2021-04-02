import json
from services import Fetcher

def run(manga_name):
    ft = Fetcher(manga_name)
    ft.run()

def main():
    with open("config/manga_list.json") as json_file:
        data = json.load(json_file)
        manga_list = data["manga_list"]

    for manga in manga_list:
        run(manga)


if __name__ == "__main__":
    main()