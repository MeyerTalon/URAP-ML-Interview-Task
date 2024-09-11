import re
from logger import logger
from multiprocessing import Pool
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class NameComponents:
    """
    The NameComponents class is used to parse company names into their raw name, legal identifier, location, and base
    name.It also contains a method to check if a company name contains a legal identifier using a fine-tuned BERT model.

    Attributes:
        locations_dict (dict): all locations from locations.tsv files parsed to a dictionary.
        legal_dict (dict): all legal identifiers from the legal.txt file parsed to a dictionary.
        company_dict (dict): all company names from the companies.txt file parse to a dictionary.
        model (AutoModelForSequenceClassification): a fine-tuned BERT model to check for legal identifiers, initialized
            to None with __init__ and later loaded from HuggingFace with initialize_model().
        tokenizer (AutoTokenizer): a fine-tuned BERT tokenizer to tokenize the company names, initialized
            to None with __init__ and later loaded from HuggingFace with initialize_model().
    """

    def __init__(self) -> None:
        """
        Initialize the NameComponents class by reading in the data files from the folder URAP_test_data.
        """

        logger.info('Initializing NameComponents class.')

        # Initialize model and tokenizer, but do not load them. This is done in the initialize method.
        self.model = None
        self.tokenizer = None

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
                key = re.sub(r'[^\w\s]', '', key.lower())
                self.legal_dict[line.replace('\n', '').lower()] = index

        # Open companies.txt and populate the company_dict.
        with open(r'./src/URAP_test_data/companies.txt') as f:
            for index, line in enumerate(f):
                self.company_dict[line.replace('\n', '')] = index

    @staticmethod
    def generate_consecutive_word_combinations(comp_name: str) -> [str]:
        """
        This method generates all possible combinations of consecutive words in a string. For instance, the string
        'the brown fox' returns ['the', 'brown', 'fox', 'the brown', 'the brown fox', 'brown fox'].
        I created this method to check for multi-word locations such as 'long island'.

        Args:
            comp_name (str): the name of the company to parse in a dictionary.

        Returns:
            combinations (list): a list of all possible consecutive word combinations in the comp_name string.
        """

        # Split the company name into a list of words.
        name_split = comp_name.split()
        combinations = comp_name.split()

        # Generate all possible consecutive word combinations.
        for i in range(len(name_split)):
            combo = name_split[i]
            for j in range(i + 1, len(name_split)):
                combo += ' ' + name_split[j]
                combinations.append(combo)

        return combinations

    def get_name_components(self, comp_name: str) -> dict[str: str]:
        """
        This method extracts the raw name, legal identifier, location, and base name within a company name returning the
        components as a dict.

        Args:
            comp_name (str): the name of the company to parse in a dictionary.

        Returns:
            output (dict): a dictionary of string keys and string values denoting the parts composing the
                company name.
        """

        logger.info(f'Starting text parsing on {comp_name}.')

        # Create the output dictionary and add the raw comp_name string to it.
        components = {'raw': comp_name}

        try:

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

        except Exception as e:
            logger.error(f'{comp_name} generated error: {e}')

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

    def initialize_model(self) -> None:
        """
        This method initializes the custom fine-tuned BERT tokenizer and model.
        """
        logger.info('Initializing the custom fine-tuned BERT tokenizer and model.')

        try:
            # Initialize the custom fine-tuned BERT tokenizer and model.
            self.tokenizer = AutoTokenizer.from_pretrained('google-bert/bert-base-cased')
            self.model = AutoModelForSequenceClassification.from_pretrained('TalonMeyer/bert-base-cased-legal-keyword-identifier')
        except Exception as e:
            logger.error(f'Error in initialize_model: {e}.')

    def contains_legal_identifier(self, comp_name: str) -> bool:
        """
        This method checks if a company name contains a legal identifier using the fine-tuned BERT model. I split the
        model initialization away from the __init__ method in case someone running this script has a low amount of
        memory. This way, they can use the class without having to load the model.

        Args:
            comp_name (str): the name of the company to parse in a dictionary.

        Returns:
            bool: True if the company name contains a legal identifier, False otherwise.
        """

        logger.info(f'Starting legal identifier inference check on: {comp_name}.')

        try:

            # Check if the model and tokenizer are initialized.
            if self.model is None or self.tokenizer is None:
                raise Exception('Model and tokenizer not initialized. Make sure you previously ran initialize_model')

            # Tokenize the company name.
            tokens = self.tokenizer(comp_name, return_tensors='pt')

            # Get the model output.
            outputs = self.model(**tokens)

            # Get the predicted labels.
            predicted_label = outputs.logits.argmax(dim=1)

            # Check if the company name contains a legal identifier.
            if 1 in predicted_label[0]:
                return True
            else:
                return False
        except Exception as e:
            logger.error(f'Error in contains_legal_identifier: {e}. Make sure you previously ran initialize_model.')


if __name__ == '__main__':

    # Create instance of NameComponents and parse all company names.
    name_components = NameComponents()
    name_components.get_all_name_components()

    # Test the contains_legal_identifier method.
    name_components.initialize_model()
    print(name_components.contains_legal_identifier('Apple Inc.'))
