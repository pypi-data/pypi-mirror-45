# __main__.py for StatsScraper

from Scraper import Scraper


def main():

    scraper = Scraper()

    result = scraper.find_player_by_name("Ivica Zubac")
    print("Printing result\n")
    for p in result:
        print(p)

    sorted_points = scraper.sort_by_points("SG")
    print("========Printing top scorers========\n")
    for scores in sorted_points:
        print(scores[0], scores[1])

    sorted_assists = scraper.sort_by_assists("PF")
    print("\n\n\n=========Printing top 10 assisters========\n")
    count = 0
    for assists in sorted_assists:
        if(count >= 10):
            break
        print(assists[0], assists[1])
        count += 1

    sorted_rebounds = scraper.sort_by_rebounds("PG", "SG")
    print("\n\n\n=========Printing top 20 rebounders========\n")
    count = 0
    for rebounds in sorted_rebounds:
        if (count >= 20):
            break
        print(rebounds[0], rebounds[1])
        count += 1


if __name__ == "__main__":
    main()
