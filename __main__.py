import requests
import bs4

def find_data_in_soup(soup):
    # var to store all data
    all_defs_and_words = []
    # looks for each card
    cards = soup.find_all("div", class_="SetPageTerm-sideContent")
    for card in cards:
        # mini sub list that stores teh term and def
        word_and_def = []
        text = card.find_all("span")
        # look for the def and the term in the div
        for word in text:
            word_and_def.append(word.text)
        # add the term and the def list, to the larger full list
        all_defs_and_words.append(word_and_def)
    return all_defs_and_words


def print_cards(all_defs_and_words):
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


def get_input_from_file(file_name):
    """reads the contents of given file name returns a list of lines"""
    file_contents = []
    with open(file_name, 'r') as f_in:
        for line in f_in:
            file_contents.append(line)
    return file_contents 


def quizlet_write_to_file(quizlet_term_def, quizlet_name):
    # open file with a so that we append
    with open(quizlet_name + ".lst", 'a') as f_out:
        # loop througt the dictionary
        f_out.write("!!!" + quizlet_name + "!!!\n")
        term_number = 1
        term_flapper = True
        # loop through list
        for card in quizlet_term_def:
            # loop through sub-list
            for text in card:
                if term_flapper == True:
                    f_out.write("term (" + str(term_number) + "): " +  text + '\n')
                else:
                    f_out.write("def (" + str(term_number) + "): "+ text + '\n')
                    f_out.write("---------------------" + '\n')
                    term_number += 1
                term_flapper = not(term_flapper)


def main():
    input_file = "input.txt"
    # read url from file and remove new line
    list_of_urls = get_input_from_file(input_file)
    print(list_of_urls)
    for url in list_of_urls:
        # all of this bs to remove the new line from the url
        url = list(url)
        url.pop(-1)
        url = "".join(url)
        print("Working on: (" + url + ")...")

        # because someone doesn't like being scraped this is a random header I found somewhere
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}
        responce = requests.get(url, headers=headers)
        soup = bs4.BeautifulSoup(responce.content, "html.parser")
        # get the quizlet's name
        quizlet_name = soup.find("div", class_="SetPage-titleWrapper").h1.text

        # searches the soup for the wanted data
        all_defs_and_words = find_data_in_soup(soup)
        # prints the data found in bs to cmd 
        # print_cards(all_defs_and_words)
        # writes to the file
        quizlet_write_to_file(all_defs_and_words, quizlet_name)


if __name__ == "__main__":
    main()
