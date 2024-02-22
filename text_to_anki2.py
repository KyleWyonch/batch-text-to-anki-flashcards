# FILE: text_to_anki2.py
# Created: ~2023-10
# Purpose: Convert notes of the following format into Anki flashcards:
# [1-2c] - Either 1 way, 2 way, or cloze deletion card
# Side 1 or Question or Cloze deletion paragraph
# Side 2 or Answer or Cloze deletion notes
# Notes
# Tags
# --
# TODO Proper format checking inherent in the script, so that it will not add anything if there is an error.
# TODO (Probably inherent as an Emacs script) Add auto-deletion of text once cards are in Anki

import requests
import sys
import logging
from typing import List, Tuple, Dict

ANKI_CONNECT_URL = 'http://localhost:8765'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 2024-02-21: Added functionality to replace instances of < and > with HTML-safe alternatives: &lt; and &gt;
def replace_html_characters(text: str) -> str:
    return text.replace("<", "&lt;").replace(">", "&gt;")

# 2024-01-28: Added multiple encodings with a try/except, originally was just utf-8, but ran into an error yesterday when trying to add cards with an accented e
def read_with_encodings(path, encodings=('utf-8', 'latin-1', 'windows-1252')):
    for encoding in encodings:
        try:
            with open(path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Unable to decode the file {path} with any of the provided encodings.")

def parse_text_file(file_path: str) -> List[List[str]]:
    try:
        content = read_with_encodings(file_path)
    except FileNotFoundError:
        logging.error(f"File {file_path} not found.")
        sys.exit(1)
    except ValueError as e:
        logging.error(e)
        sys.exit(1)

    cards_raw = content.split('\n--\n')
    cards = [card.split('\n') for card in cards_raw]

    return cards

def create_payload(deck_name: str, model_name: str, fields: Dict[str, str], tags: List[str]) -> Dict:
    return {
        'action': 'addNote',
        'version': 6,
        'params': {
            'note': {
                'deckName': deck_name,
                'modelName': model_name,
                'fields': fields,
                'options': {
                    'allowDuplicate': False
                },
                'tags': tags
            }
        }
    }

def process_card(card: List[str]) -> Tuple[str, Dict[str, str], List[str]]:
    if len(card) < 2:
        return None, None, None

    card_type, *card_data = card
    # Apply HTML character replacement for each field of the card
    card_data = [replace_html_characters(field) for field in card_data]
    
    model_name = fields = tags = None

    if card_type.startswith('1'):  # One-way card
        model_name = '1 Way Card'
        fields = {'Question': card_data[0], 'Answer': card_data[1], 'Notes': card_data[2] if len(card_data) > 2 else ''}
        tags = card_data[3].split() if len(card_data) > 3 else []
    elif card_type.startswith('2'):  # Two-way card
        model_name = '2 Way Card'
        fields = {'Question 1': card_data[0], 'Question 2': card_data[1], 'Notes': card_data[2] if len(card_data) > 2 else ''}
        tags = card_data[3].split() if len(card_data) > 3 else []
    elif card_type.startswith('c'): # cloze-deletion
        model_name = 'Cloze'
        fields = {'Text': card_data[0], 'Notes': card_data[1] if len(card_data) > 1 else ''}
        tags = card_data[2].split() if len(card_data) > 2 else []

    return model_name, fields, tags


def add_cards_to_deck(deck_name: str, cards: List[List[str]]) -> int:
    actions = []
    for card in cards:
        model_name, fields, tags = process_card(card)
        if model_name and fields and tags is not None:
            payload = create_payload(deck_name, model_name, fields, tags)
            actions.append(payload)

    if not actions:
        logging.warning("No valid cards found in the input file.")
        return 0

    batch_payload = {
        'action': 'multi',
        'version': 6,
        'params': {
            'actions': actions
        }
    }

    try:
        response = requests.post(ANKI_CONNECT_URL, json=batch_payload).json()
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while connecting to Anki: {e}")
        sys.exit(1)

    results = response.get('result', [])
    added_cards = sum(1 for result in results if result)

    return added_cards


def main(input_file: str, deck_name: str):
    cards = parse_text_file(input_file)
    added_cards = add_cards_to_deck(deck_name, cards)

    logging.info(f'Successfully added {added_cards} cards to Anki deck "{deck_name}".')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        logging.error('Usage: python text_to_anki.py [input_text_file] [deck_name]')
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
