from urllib.request import urlopen
from bs4 import BeautifulSoup

"""
Finds stats of League of Legends player via op.gg and bs4.
"""


# Find the line of HTML code with given tag and class.
def tag_content_str(tag_name, class_code):
    tag_content = str(page_content.find(tag_name, attrs={'class': class_code}))

    indices = tag_start_end(tag_content)
    res = tag_content[
          indices[0]:indices[1]
          ].strip()  # Final is stripped from all leading/trailing spaces.

    return res


# Finds content wanted since HTML formats like this: <TAG>CONTENT</TAG>.
def tag_start_end(content):
    # Finding the range in which the wanted content lies ie >CONTENT<.
    start = content.find(">") + 1
    end = content.rfind("<")

    return start, end


# Main loop.
if __name__ == '__main__':
    while True:
        username = input("League username (case-sensitive): ")
        print("*****\nSearching...")
        url = f"https://na.op.gg/summoner/userName={username}"
        page_html = urlopen(url)
        page_content = BeautifulSoup(page_html, features="html.parser")

        # RETRIEVE INFO -----
        # Rank can be simply obtained with the functions defined above.
        rank = tag_content_str('div', 'TierRank')
        main = tag_content_str('div', 'ChampionName')
        lad_rank = tag_content_str('span', 'ranking')
        if lad_rank == "Non":
            lad_rank = "Unranked"

        # Since the ChampionName class has another layer of code, we extract the range in which
        # the champion name exists and strips the result of whitespace.
        main = main[tag_start_end(main)[0]: tag_start_end(main)[1]].strip()

        # Format.
        print("Finished.\n"
              "*****\n")

        print(f"{username}\n"
              f"--------\n"
              f"LADDER RANK: {lad_rank}\n"
              f"SOLO Q RANK: {rank}\n"
              f"FAVOURITE CHAMP: {main}\n")
