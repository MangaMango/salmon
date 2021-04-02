from entities.manga import Manga
from entities.edition import Edition
from entities.volume import Volume

import os, json

list_added_volumes = []
volumes = os.listdir("json_volumes")
for volume in volumes:
    with open(f"json_volumes/{volume}") as json_file:
        data = json.load(json_file)
        list_added_volumes.append(data["volume_url"])

editions = os.listdir("json_editions")
for edition in editions:
    with open(f"json_editions/{edition}") as json_file:
        data = json.load(json_file)
        edition_name = data["name"]
        volumes_url = data["volumes_url"]
        for url in volumes_url:
            try:
                if not any(url in s for s in list_added_volumes):
                    volume = Volume()
                    volume._get_amazon_link(url, edition_name)
            except:
                print(f"ERROR: {url}")
                pass

exit(1)



list_anime = [
    "Demon Slayer",
    "One Piece",
    "The Quintessential Quintuplets",
    "Kingdom",
    "My Hero Academia",
    "Haikyuu!!",
    "Spy X Family",
    "The Heroic Legend of Arslan",
    "Shingeki No Kyojin",
    "Rurouni Kenshin",
    "Nanatsu No Taizai",
    "Detective Conan",
    "Dr. Stone",
    "Black Clover",
    "Ace of Diamond",
    "Shuumatsu no Valkyrie",
    "Yomamushi Pedal",
    "Everyone’s Toy: Minasama No Omocha",
    "Naruto",
    "Dragon Ball"
]

for anime in list_anime:
    manga = Manga(anime)
    manga.set_editions_url()
    manga.save_json()

    for edition in manga._editions_url:
        edition = Edition(manga._name, edition)
        edition.set_volumes_url()
        edition.save_json()