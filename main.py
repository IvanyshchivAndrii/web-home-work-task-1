import webbrowser
from ContactBook import ContactBook
import Header
from sort import FileSorter
from CryptoPrice import CryptoPriceFetcher
import NB
from abc import ABC, abstractmethod


# ANSI escape codes for text coloring
class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"


class BaceGPA(ABC):

    @abstractmethod
    def start_contactbook(self):
        pass

    @abstractmethod
    def start_notebook(self):
        pass

    @abstractmethod
    def start_filesorter(self):
        pass

    @abstractmethod
    def start_cryptoprice(self):
        pass

    @abstractmethod
    def start_browsersearch(self):
        pass


class GPA(BaceGPA):
    def __init__(self, contact: ContactBook, note: NB, price: CryptoPriceFetcher,
                 websearch: webbrowser):
        self.contact = contact
        self.note = note
        self.price = price
        self.sorter = None
        self.websearch = websearch

    def start_contactbook(self):
        self.contact.main()

    def start_notebook(self):
        self.note.run()

    def start_filesorter(self):
        target_folder = input("Enter the folder path to sort: ")
        self.sorter = FileSorter(target_folder)
        self.sorter.run()

    def start_cryptoprice(self):
        self.price.display_crypto_prices()

    def start_browsersearch(self):
        query = input("Enter your search query: ")
        self.websearch.open(f"https://www.google.com/search?q={query}")


def main():
    Header.header_text()
    gpa = GPA(ContactBook(), NB, CryptoPriceFetcher(), webbrowser)

    while True:
        print("Choose a command:")
        print(f"{Colors.BLUE}1. ContactBook{Colors.RESET}")
        print(f"{Colors.GREEN}2. NoteBook{Colors.RESET}")
        print(f"{Colors.YELLOW}3. FileSorter{Colors.RESET}")
        print(f"{Colors.MAGENTA}4. CryptoPrice{Colors.RESET}")
        print(f"{Colors.CYAN}5. WebSearch{Colors.RESET}")
        print(f"{Colors.RED}6. Exit{Colors.RESET}")

        user_input = input("Enter command number: ")
        if user_input == '1':
            gpa.start_contactbook()

        elif user_input == '2':
            gpa.start_notebook()

        elif user_input == '3':
            gpa.start_filesorter()

        elif user_input == '4':
            gpa.start_cryptoprice()

        elif user_input == '5':
            gpa.start_browsersearch()

        elif user_input == '6':
            print(f"{Colors.RED}Goodbye!{Colors.RESET}")
            break
        else:

            print(f"{Colors.RED}Wrong command. Enter a valid command.{Colors.RESET}")


if __name__ == '__main__':
    main()
