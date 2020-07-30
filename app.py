from utilis.words import Words

""" The main script including business logic of application"""

MENU_OPTIONS = {
    "a": "animals",
    "e": "emotions",
    "f": "food",
    "h": "health",
    "i": "incorrect_translate",
    "m": "man",
    "p": "plants",
    "r": "reset table 'incorrect_translate'",
    "s": "sport",
    "t": "travel",
    "w": "work",
    "q": "quit"
}

menu_prompt = f"{MENU_OPTIONS}\nselect category: "
print("Welcome to my program\n")


def menu():
    """
    main menu of app.py
    """
    selection = input(menu_prompt)
    while selection != "q":
        if selection in MENU_OPTIONS:
            category = MENU_OPTIONS[selection]
            words = Words(category)
            if category == MENU_OPTIONS["r"]:
                words.clear_table_wrong_answers()
                menu()
            sub_menu(words)
        print(f"Invalid category: {selection}")
        selection = input(menu_prompt)


def sub_menu(words: Words):
    """
    sub_menu is detached from menu() to avoid create "root" instance over every iteration
    """
    while True:
        polish_word = words.ask_user_to_translate()
        if polish_word is None:
            menu()
        print(polish_word)
        user_answer = input("\nEnter correct translate or 'b' to back to main menu: \n")
        if user_answer == "b":
            print(f"Total score: {words.score} points")
            menu()
        message = words.check_translate_is_correct(user_answer)
        print(f"{message}")


menu()
