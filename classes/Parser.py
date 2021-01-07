import filecmp
import os
import random
import re
import shutil

from classes.Card import Card
from classes.Image import Image


class Parser:
    DEFAULT_ANKI_FOLDER = {
        'win32': r'~\AppData\Anki2',
        'linux': '~/.local/share/Anki2',
        'darwin': '~/Library/Application Support/Anki2'
    }

    def __init__(self, file_path, anki_user_name='User 1'):
        self.file_path = file_path
        self.anki_user_name = anki_user_name

    def collect_cards(self):
        note_string = self.get_note_string()

        question_sections = self.get_question_sections(note_string)

        cards = []
        for section in question_sections:
            cards.extend(self.get_cards_from_section(section))

        return cards

    def get_cards_from_section(self, section):
        section = self.handle_images(section)

        tags = self.get_tags_from_section(section)
        deck_name = self.get_deck_name_from_section(section)

        questions = re.findall(r'^\d+\..+?(?=^>)',
                               section,
                               re.DOTALL | re.MULTILINE)
        # Clean questions from whitespace at the start and the end of string
        questions = list(map(lambda q: re.sub(r'\d+\.', '', q, 1).strip(), questions))

        answers = re.findall(r'(?:>.*?\n)+',
                             section,
                             re.DOTALL | re.MULTILINE)

        # Clean (remove '>' and unnecessary whitespace) answer strings
        answers = list(map(self.clean_answer_string, answers))

        if len(questions) != len(answers):
            raise ValueError(f'Different number of questions and answers in section:\n{section}')

        cards = []
        for question, answer in zip(questions, answers):
            cards.append(Card(question, answer, tags, deck_name))

        return cards

    def handle_images(self, section):
        # Find all unique image links in the text
        image_links = set(re.findall(r'!\[.*?]\(.*?\)', section))
        images = [Image(link) for link in image_links]

        # Change image name if image with this name already exists in Anki Media folder

        # Copy images to Anki Media folder
        # And change all image links in section string
        for image in images:
            self.copy_image_to_anki_media(image)
            section = section.replace(image.original_md_link, image.updated_md_link)

        return section

    def copy_image_to_anki_media(self, image):
        anki_folder_path = os.path.expanduser(self.DEFAULT_ANKI_FOLDER["linux"])
        anki_image_path = f'{anki_folder_path}/{self.anki_user_name}/collection.media/{image.file_name}'

        # Check if image already exists in Anki Media folder
        if os.path.exists(anki_image_path):
            # If same image is already in folder then skip
            if filecmp.cmp(image.abs_path, anki_image_path):
                image.path = image.file_name
                return

            # If not same then rename our image
            image.rename(f'{image.file_name}_{random.randint(100000, 999999)}')

        # Copy image
        shutil.copyfile(image.abs_path, anki_image_path)

        # Change path to be just file name (for it to work in Anki)
        image.path = image.file_name

    def get_tags_from_section(self, section):
        match = re.search(r'(?<=^Tags:).*?$',
                          section,
                          re.MULTILINE)
        if not match:
            return []

        tags = match.group().strip().split()
        return tags

    def get_deck_name_from_section(self, section):
        match = re.search(r'(?<=^Deck:).*?$',
                          section,
                          re.MULTILINE)

        if not match or not match.group().strip():
            raise ValueError(f"Couldn't find deck name in:\n{section}")

        deck_name = match.group().strip()
        return deck_name

    def clean_answer_string(self, answer):
        lines = answer.splitlines()
        # Remove first char ('>') and whitespace at the start
        # and the end of each line
        lines = map(lambda l: l[1:].strip(), lines)

        return '\n'.join(lines)

    def get_question_sections(self, note_string):
        return re.findall(r'^---$.+?^---$',
                          note_string,
                          re.MULTILINE | re.DOTALL)

    def get_note_string(self):
        with open(self.file_path, 'r') as note:
            note_string = note.read()

        return note_string
