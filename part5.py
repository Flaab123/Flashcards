import os
import random

class Flashcards:
    """Class representing all flashcards"""
    all_flashcards = []
    def __init__(self,term,definition):
        self.term = term
        self.definition = definition
        Flashcards.all_flashcards.append(self)


def check_input(user_input,type):
    """Checks if the user input already exists as a term or definition"""
    if type == 'term':
        if Flashcards.all_flashcards == []:
            return True
        elif any([user_input == card.term for card in Flashcards.all_flashcards]): # TODO: maybe
            print(f'The card "{user_input}" already exists. Try again:')
            return False
        else:
            return True
    if type == 'definition':
        if Flashcards.all_flashcards == []:
            return True
        elif any([user_input == card.definition for card in Flashcards.all_flashcards]):
            print(f'The definition "{user_input}" already exists. Try again:')
            return False
        else:
            return True

def input_term_def(type):
    """Prompts user to input a term and definition for a card until a unique input is given"""
    check = False
    while check == False:
        user_input = input()
        check = check_input(user_input,type)
    return user_input

def ask_answer(card_number):
    """Prompts user for an answer for the given card"""
    prompt = Flashcards.all_flashcards[card_number].term
    correct_answer = Flashcards.all_flashcards[card_number].definition
    print(f'Print the definition of "{prompt}":')
    user_input = input()
    wrong_answer = True
    if user_input == correct_answer:
        print('Correct!')
        wrong_answer = False
    else:
        for card in (cards for cards in Flashcards.all_flashcards if cards != Flashcards.all_flashcards[card_number]):
            if card.definition == user_input:
                print(f'Wrong. The right answer is "{correct_answer}", but your definition is correct for "{card.term}".')
                wrong_answer = False
                break
    if wrong_answer:
        print(f'Wrong. The right answer is "{correct_answer}".')

def user_add():
    print("The card:")
    term = input_term_def('term')
    print("The definition of the card:")
    definition = input_term_def('definition')
    print(f'The pair ("{term}":"{definition}") has been added.')
    Flashcards(term,definition)

def user_import():
    print("File name:")
    import_file = input()
    if not os.path.isfile(import_file):
        print("File not found.")
    else:
        imported_file = open(import_file, 'r')
        imported_data = [line.rstrip('\n')  for line in imported_file]
        imported_file.close()
        imported_terms = imported_data[0::2]
        imported_definitions = imported_data[1::2]
        for i in range(len(imported_terms)):
            for k, o in enumerate(Flashcards.all_flashcards):
                if o.term == imported_terms[i] or o.definition == imported_definitions[i]:
                    del Flashcards.all_flashcards[k]
                    break
            Flashcards(imported_terms[i],imported_definitions[i])
        cards_added = len(imported_terms)
        print(f'{cards_added} cards have been loaded.')

def user_export():
    print("File name:")
    file_name = input()
    export_file = open(file_name, 'w', encoding='utf-8')
    for cards in Flashcards.all_flashcards:
        export_file.write(cards.term + '\n')
        export_file.write(cards.definition + '\n')
    export_file.close()
    amount_of_cards = len(Flashcards.all_flashcards)
    print(f'{amount_of_cards} cards have been saved.')

def user_remove():
    print("Which card?")
    to_remove = input()
    removed_a_card = 0
    for i, o in enumerate(Flashcards.all_flashcards):
        if o.term == to_remove:
            print("The card has been removed.")
            del Flashcards.all_flashcards[i]
            removed_a_card = 1
            break
    if not removed_a_card:
        print(f'Can\'t remove "{to_remove}": there is no such card.')

def user_ask():
    print("How many times to ask?")
    ask_number = int(input())
    amount_of_cards = len(Flashcards.all_flashcards)
    for _ in range(ask_number):
        card_pick = random.randint(0,amount_of_cards-1)
        ask_answer(card_pick)

def user_exit():
    print("Bye bye!")
    return "Exit procedure"

check_exit = ''    
while check_exit != "Exit procedure":
    print("Input the action (add, remove, import, export, ask, exit):")
    prompt_input = input()
    if prompt_input == 'add':
        user_add()
    if prompt_input == 'remove':
        user_remove()
    if prompt_input == 'import':
        user_import()
    if prompt_input == 'export':
        user_export()
    if prompt_input == 'ask':
        user_ask()
    if prompt_input == 'exit':
        check_exit = user_exit()

