import requests
import bs4


def main():

    url = "https://quizlet.com/215414023/us-hist-ch-11-14-flash-cards/"
    # because someone doesn't like being scraped this is a random header I found somewhere
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}
    responce = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(responce.content, "html.parser")
    
    all_defs_and_words = []

    cards = soup.find_all("div", class_="SetPageTerm-sideContent")
    for card in cards:
        word_an_def = []
        text = card.find_all("span")
        for word in text:
            word_an_def.append(word.text)
        all_defs_and_words.append(word_an_def)

    # create a flapper to flip between calling string def or term and print the term numb
    def_flapper = True
    def_number = 1
    for card in all_defs_and_words: 
        # look throug the list's sublists
        for definition_or_term in card:
            if def_flapper == True:
                print("(" + str(def_number) + ") def: ")
            else: 
                print("(" + str(def_number) + ") term: ") 
                def_number += 1
            print(definition_or_term)
            def_flapper = not(def_flapper)

if __name__ == "__main__":
    main()
