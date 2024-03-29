import os
import random

class Flashcards:
    """Class representing all flashcards"""
    all_flashcards = []
    def __init__(self,term,definition):
        self.term = term
        self.definition = definition
        self.mistakes = 0
        Flashcards.all_flashcards.append(self)
        
class LogStream:
    def __init__(self):
        self.lines = []
        
    def In(self):
        line = input()
        self.lines += [line + '\n']
        return line

    def Out(self,line):
        self.lines += [line + '\n']
        print(line)
        
    def Write(self,file_path):
        export_file = open(file_path, 'w', encoding='utf-8')
        for line in self.lines:
            export_file.write(line)
        export_file.close()

log_stream = LogStream()

def check_input(user_input,type):
    """Checks if the user input already exists as a term or definition"""
    if type == 'term':
        if Flashcards.all_flashcards == []:
            return True
        elif any([user_input == card.term for card in Flashcards.all_flashcards]): # TODO: maybe
            log_stream.Out(f'The card "{user_input}" already exists. Try again:')
            return False
        else:
            return True
    if type == 'definition':
        if Flashcards.all_flashcards == []:
            return True
        elif any([user_input == card.definition for card in Flashcards.all_flashcards]):
            log_stream.Out(f'The definition "{user_input}" already exists. Try again:')
            return False
        else:
            return True

def input_term_def(type):
    """Prompts user to input a term and definition for a card until a unique input is given"""
    check = False
    while check == False:
        user_input = log_stream.In()
        check = check_input(user_input,type)
    return user_input

def ask_answer(card_number):
    """Prompts user for an answer for the given card"""
    prompt = Flashcards.all_flashcards[card_number].term
    correct_answer = Flashcards.all_flashcards[card_number].definition
    log_stream.Out(f'Print the definition of "{prompt}":')
    user_input = log_stream.In()
    wrong_answer = True
    if user_input == correct_answer:
        log_stream.Out('Correct!')
        wrong_answer = False
    else:
        Flashcards.all_flashcards[card_number].mistakes += 1
        for card in (cards for cards in Flashcards.all_flashcards if cards != Flashcards.all_flashcards[card_number]):
            if card.definition == user_input:
                log_stream.Out(f'Wrong. The right answer is "{correct_answer}", but your definition is correct for "{card.term}".')
                wrong_answer = False
                break
    if wrong_answer:
        log_stream.Out(f'Wrong. The right answer is "{correct_answer}".')



def user_add():
    log_stream.Out("The card:")
    term = input_term_def('term')
    log_stream.Out("The definition of the card:")
    definition = input_term_def('definition')
    log_stream.Out(f'The pair ("{term}":"{definition}") has been added.')
    Flashcards(term,definition)

def user_import():
    log_stream.Out("File name:")
    import_file = log_stream.In()
    if not os.path.isfile(import_file):
        log_stream.Out("File not found.")
    else:
        imported_file = open(import_file, 'r')
        imported_data = [line.rstrip('\n')  for line in imported_file]
        imported_file.close()
        imported_terms = imported_data[0::3]
        imported_definitions = imported_data[1::3]
        imported_mistakes = imported_data[2::3]
        for i in range(len(imported_terms)):
            for k, o in enumerate(Flashcards.all_flashcards):
                if o.term == imported_terms[i] or o.definition == imported_definitions[i]:
                    del Flashcards.all_flashcards[k]
                    break
            Flashcards(imported_terms[i],imported_definitions[i],int(imported_mistakes[i]))
        cards_added = len(imported_terms)
        log_stream.Out(f'{cards_added} cards have been loaded.')

def user_export():
    log_stream.Out("File name:")
    file_name = log_stream.In()
    export_file = open(file_name, 'w', encoding='utf-8')
    for cards in Flashcards.all_flashcards:
        export_file.write(cards.term + '\n')
        export_file.write(cards.definition + '\n')
        export_file.write(str(cards.mistakes) + '\n')
    export_file.close()
    amount_of_cards = len(Flashcards.all_flashcards)
    log_stream.Out(f'{amount_of_cards} cards have been saved.')

def user_remove():
    log_stream.Out("Which card?")
    to_remove = log_stream.In()
    removed_a_card = 0
    for i, o in enumerate(Flashcards.all_flashcards):
        if o.term == to_remove:
            print("The card has been removed.")
            del Flashcards.all_flashcards[i]
            removed_a_card = 1
            break
    if not removed_a_card:
        log_stream.Out(f'Can\'t remove "{to_remove}": there is no such card.')

def user_ask():
    log_stream.Out("How many times to ask?")
    ask_number = int(log_stream.In())
    amount_of_cards = len(Flashcards.all_flashcards)
    for _ in range(ask_number):
        card_pick = random.randint(0,amount_of_cards-1)
        ask_answer(card_pick)

def user_exit():
    log_stream.Out("Bye bye!")
    return "Exit procedure"

def hardest_card():
    card_mistakes = [card.mistakes for card in Flashcards.all_flashcards]
    max_mistakes = max(card_mistakes)
    if max_mistakes == 0:
        log_stream.Out("There are no cards with errors.")
    else:
        terms = ['"' + card.term + '"' for card in Flashcards.all_flashcards if card.mistakes == max_mistakes]
        terms_joined = ", ".join(terms)
        log_stream.Out(f'The hardest cards are {terms_joined}. You have {max_mistakes} errors answering them.')

def reset_stats():
    for i, _ in enumerate(Flashcards.all_flashcards):
        Flashcards.all_flashcards[i].mistakes = 0

check_exit = ''    
while check_exit != "Exit procedure":
    log_stream.Out("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
    prompt_input = log_stream.In()
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
    if prompt_input == 'log':
        filepath = log_stream.In()
        log_stream.Write(filepath)
        log_stream.Out("The log has been saved.")
    if prompt_input == 'hardest card':  
        hardest_card()
    if prompt_input == 'reset stats':  
        reset_stats()

for cards  in Flashcards.all_flashcards:
    print(cards.term)
    print(cards.definition)
    print(cards.mistakes)        
