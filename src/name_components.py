import re
from logger import logger
from multiprocessing import Pool
import pandas as pd
import os


class NameComponents:

    def __init__(self) -> None:
        """
        Initialize the NameComponents class by reading in the data files from the folder URAP_test_data as pandas
        dataframes and storing them as instance variables.
        """

        logger.info('Initializing NameComponents class.')

        # Initialize dicts to hold the locations, legal identifiers, and companies.
        self.locations_dict = {}
        self.legal_dict = {}
        self.company_dict = {}

        # Open locations.tsv and populate the locations_dict.
        with open(r'./src/URAP_test_data/locations.tsv') as f:
            for line in f:
                key, value = line.split('\t')
                self.locations_dict[key] = value.replace('\n', '')

        # Open legal.txt and populate the legal_dict.
        with open(r'./src/URAP_test_data/legal.txt') as f:
            for index, line in enumerate(f):
                self.legal_dict[line.replace('\n', '').lower()] = index

        # Open companies.txt and populate the company_dict.
        with open(r'./src/URAP_test_data/companies.txt') as f:
            for index, line in enumerate(f):
                self.company_dict[line.replace('\n', '')] = index

    @staticmethod
    def contains_word(sentence: str, word: str) -> bool:
        """
        This helper function is used to check if a whole word is contained in a sentence. This is needed as opposed to a
        simple in keyword check because in only looks for matching characters, so if the company name was Cool Company
        Inc. the location co (Colorado) would be contained in the company name which is not what we want.

        Args:
            sentence (str): the sentence which may contain the word.
            word (str): the word to look for in the sentence.

        Returns:
            True if the whole word is in the sentence, False otherwise.
        """

        # This regex pattern matches the word preceded by and followed by any non-alphabetical character to make sure
        # theword is not within a larger word.
        return bool(re.search(f'([^a-zA-Z]|^){word}([^a-zA-Z]|$)', sentence))

    @staticmethod
    def generate_consecutive_word_combinations(comp_name: str) -> [str]:
        """

        Args:
            comp_name:

        Returns:

        """
        name_split = comp_name.split()
        combinations = comp_name.split()

        for i in range(len(name_split)):
            combo = name_split[i]
            for j in range(i + 1, len(name_split)):
                combo += ' ' + name_split[j]
                combinations.append(combo)

        return combinations

    def get_name_components(self, comp_name: str) -> dict[str: str]:
        """
        This function extracts the legal identifier and location name within a company name.

        Args:
            comp_name (str): the name of the company to parse in a dictionary.

        Returns:
            output (dict): a dictionary of string keys and string values denoting the parts composing the
                company name.
        """

        logger.info(f'Starting text parsing on {comp_name}.')

        # Create the output dictionary and add the raw comp_name string to it.
        components = {'raw': comp_name}

        # Remove all non-alphanumerics besides whitespaces and cast to lowercase.
        edited_comp_name = re.sub(r'[^\w\s]', '', comp_name.lower())

        # For every consecutive combination of words in comp_name, check legal and location
        comp_name_word_combinations = self.generate_consecutive_word_combinations(edited_comp_name)

        # Loop through all combinations of our word to search for legal terms and locations.
        for combo in comp_name_word_combinations:

            if combo in self.legal_dict and combo not in components.values():
                components['legal'] = combo
                edited_comp_name = edited_comp_name.replace(combo, '')

            if combo in self.locations_dict and combo not in components.values():
                components['location'] = combo
                edited_comp_name = edited_comp_name.replace(combo, '')

        # Once the legal and location are removed, all that remains is the base name.
        components['base_name'] = re.sub(r'[ ]+', ' ', edited_comp_name).strip()

        logger.info(f'Completed name component parsing on: {comp_name}, with result: {components}')

        return components

    def get_all_name_components(self) -> None:
        """
        This method parses all companies in the companies.txt file using the get_name_components method and writes the
        result to /URAP_test_data/company_names_parsed.csv
        """
        logger.info(f'Starting text parsing on all company names.')

        try:
            with Pool() as p:
                all_components = p.map(self.get_name_components, self.company_dict.keys())
        except Exception as e:
            logger.error(f'Pool error: {e}.')

        all_components_df = pd.DataFrame(all_components)
        all_components_df.to_csv(r'./src/URAP_test_data/company_names_parsed.csv', index=False)

        logger.info(f'Completed text parsing on all company names.')


if __name__ == '__main__':

    name_components = NameComponents()
    name_components.get_all_name_components()
