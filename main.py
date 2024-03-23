# Project Library main file. This is supposed to launch the main menu.


from colorama import Fore, Back, Style
import signup
import login


class InvalidSelection(Exception):
    pass


def main_screen():
    print("1 - Sign up")
    print("2 - Login")
    print("3 - Exit")
    while True:
        try:
            selection = int(input(Fore.GREEN + "Select from the above options: " + Style.RESET_ALL))
            if selection not in range(1, 4):
                raise InvalidSelection
        except InvalidSelection:
            print(Fore.RED + "Invalid Selection" + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Value Error" + Style.RESET_ALL)
        else:
            if selection == 1:
                signup.main()
                break
            elif selection == 2:
                login.main()
                break
            else:
                exit()


first_input = main_screen()

