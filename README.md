# batch-text-to-anki-flashcards
Converts your text notes into Anki flashcards with a python script. Takes specially formatted text files and converts them into Anki flashcards, supporting one-way, two-way, or cloze deletion cards.

## Features
- Flexible card types: supports one-way, two-way, and cloze deletion flashcards
- HTML character handling: automatically replaces '<' and '>' with HTML-safe alternatives to ensure your cards display correctly in Anki
- Multiple Encoding Support: Reads files with various encodings (UTF-8, Latin-1, Windows-1252) making it more versatile with different text file formats.
- Anki Integration: Utilizes Anki Connect to add cards directly to your Anki decks, streamlining the card creation process.

## Requirements
- Anki with Anki Connect plugin installed.
- Python 3.x

## Installation
1. Clone this repository or download the 'text_to_anki2.py' script directly.
2. Ensure you have Python 3.x installed on your system.
3. Install the required Python package 'requests' by running
```shell
pip install requests
```

## Usage
Prepare your notes in a text file following the specified format
```Text
[Card Type]
Side 1 or Question or Cloze deletion paragraph
Side 2 or Answer or Cloze deletion notes
Notes (optional) or Cloze tags
Tags (optional)
--
```
Card Types:
'1' for one-way cards
'2' for two-way cards
'c' for clozedeletion cards
Example input file:
```Text
1
What is the capital of France?
Paris
Paris is the fourth-most populated city in the European Union.
Geography::Europe Geography::Capitals
--
2
What is the primary neurotransmitter involved in the parasympathetic nervous system?
Acetylcholine is an important neurotransmitter involved with this
Important for rest-and-digest functions
Neuroscience pharmacology
--
c
According to {{c1::Ohm's Law}}, the current through a conductor between two points is directly proportional to the voltage across the two points and inversely proportional to the resistance between them, represented by the formula {{c2::I = V/R}}.
Essential for understanding electrical circuits
Engineering::Electronics
--
```
To convert your notes into Anki flashcards, run:
```shell
python text_to_anki2.py [input_text_file] [deck_name]
```
Replace '[input_text_file]' with the path to your notes file and '[deck_name]' with the name of the Anki deck you wish to add cards to.

## Contributing
Contributions are welcome! I'm not much of a programmer yet, so this script leaves a lot to be desired. If you have ideas for improvements, bug fixes, or new features, feel free to fork this repository, make your changes, and submit a pull request.

## TODO
### User Interface Improvements
- Implement a more-user friendly CLI with argument parsing, offering help messages, usage examples, and error handling.
### File Handling and Formats
- Extend the tool to read from various formats like Markdown, CSV, JSON, and Google Docs, in addition to plain text.
- Before adding cards to Anki, generate a preview file (e.g., HTML or PDF) for user review, ensuring the content is formatted correctly.
- Instead of stopping execution on the first error, log errors to a file and proceed with processing, giving a summary at the end.
### Enhanced Text and Card Processing
- Implement more sophisticated HTML character handling and support for images, audio files, and LaTeX formatting within cards.
- Add options for how to handle duplicates, such as skipping, updating, or appending additional information to existing cards.
- Integrate content validation to check for common mistakes or missing fields before attempting to add cards to Anki.
### Anki Integration
- Improve error handling for Anki Connect responses, providing clear feedback on connection issues or Anki API errors.
- Allow users to create or select existing decks and models directly from the script, possibly including template customization.
- Provide real-time feedback during the batch processing of cards, including progress indicators and summaries of added/failed cards.
### Configuration and Customization
- Allow users to save their preferences, such as default deck, model names, and encoding settings, in a configuration file.
- Enable users to define custom models and templates directly from the script, adjusting fields and styling to their needs.
