import json
from services import Fetcher

def run():
    ft = Fetcher()
    ft.run()

def main():
    run()

if __name__ == "__main__":
    main()