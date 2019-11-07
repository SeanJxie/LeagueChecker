from urllib.request import urlopen
from bs4 import BeautifulSoup

"""
Finds stats of League of Legends player via op.gg and bs4.
"""


# Find the line of HTML code with given tag and class.
def tag_content_str(tag_name, class_code):
    tag_content = str(page_content.find(tag_name, attrs={'class': class_code}))
    # print(tag_content)
    indices = tag_start_end(tag_content)
    res = tag_content[
          indices[0]:indices[1]
          ].strip()  # Final is stripped from all leading/trailing spaces.

    return res


# Finds content wanted since HTML formats something like this: <TAG>CONTENT</TAG>.
def tag_start_end(content):
    # Finding the range in which the wanted content lies ie >CONTENT<.
    start = content.find(">") + 1
    end = content.rfind("<")

    return start, end


if __name__ == '__main__':
    while True:
        username = input("League username: ")
        print("*****\nSearching...")
        url = f"https://op.gg/summoner/userName={username}"
        page_html = urlopen(url)
        page_content = BeautifulSoup(page_html, features="html.parser")

        # RETRIEVE INFO -----
        # Info can be simply obtained with the functions defined above.
        rank = tag_content_str('div', 'TierRank')
        main_champ = tag_content_str('div', 'ChampionName')
        # Since the ChampionName class has another layer of code within, we extract the range in which
        # the champion name exists and strips the result of whitespace.
        main_champ = main_champ[tag_start_end(main_champ)[0]: tag_start_end(main_champ)[1]].strip()
        # Change "No" to "None" when there is no champion data.
        if main_champ == "No":
            main_champ = "None"

        # Change a "Non" rank into "Unranked".
        lad_rank = tag_content_str('span', 'ranking')
        if lad_rank == "Non":
            lad_rank = "Unranked"
        # Kill:Death ratio.
        kda = tag_content_str('span', 'KDARatio')
        wins = tag_content_str('span', 'win')
        losses = tag_content_str('span', 'lose')

        # Change "Non" to "None" when there is no win/loss.
        if wins == 'Non':
            wins = "None"
            losses = "None"

        # Format.
        print("Finished.\n"
              "*****\n")

        print(f"{username}\n"
              f"--------\n"
              f"LADDER RANK: {lad_rank}\n"
              f"SOLO Q RANK: {rank}\n"
              f"KILL/DEATH: {kda}\n"
              f"WIN/LOSS: {wins}:{losses}\n"
              f"FAVOURITE CHAMP: {main_champ}\n")
