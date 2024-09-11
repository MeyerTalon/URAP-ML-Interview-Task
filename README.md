# URAP-ML-Interview-Task
This repository contains the code for a UC Berkeley URAP interview task provided by Professor Anastasia Fedyk. More specifically, this task will demonstrate my textual analysis and ML abilities by analyzing several .txt and .tsv files.

## NameComponents Overview

The `NameComponents` class is designed to parse company names, extract specific components like locations, legal identifiers, and base names, and process this data for further analysis. It uses dictionaries derived from external files (e.g., `locations.tsv`, `legal.txt`, and `companies.txt`) to perform the parsing, and outputs the results into a CSV file.

## Table of Contents

- [Usage](#usage)
- [Constructor (`__init__` method)](#initialization)
- [Generate Consecutive Word Combinations](#generate_consecutive_word_combinations)
- [Get Name Components](#get_name_components)
- [Get All Name Components](#get_all_name_components)
- [Contains Legal Identifier](#contains_legal_identifier)

---

## Usage
Clone the repository and run the following commands to install the required packages:
```bash
pip install -r requirements.txt
```
Then run the following command to execute the script:
```bash
python src/name_components.py
```

## Constructor (`__init__` method)

**Description**: This method initializes the `NameComponents` class by reading the data files (`locations.tsv`, `legal.txt`, `companies.txt`) and populating corresponding dictionaries (`locations_dict`, `legal_dict`, `company_dict`).

### Algorithm:
1. Log the initialization process.
2. Initialize three empty dictionaries: `locations_dict`, `legal_dict`, and `company_dict`.
3. Open the `locations.tsv` file:
   - For each line, split by the tab character (`\t`).
   - Populate `locations_dict` with the first column as the key and the second as the value.
4. Open the `legal.txt` file:
   - Clean the line of non-alphanumeric characters using regular expressions.
   - Populate `legal_dict` with each legal term as the key, and its index as the value.
5. Open the `companies.txt` file:
   - Populate `company_dict` with each line representing a company name as the key, and its index as the value.
6. Initialize the fine-tined BERT model and tokenizer for legal identifier detection.

### Example:
```python
name_components = NameComponents()
```

---

## Generate Consecutive Word Combinations

```python
@staticmethod
def generate_consecutive_word_combinations(comp_name: str) -> [str]:
```

**Description**: This static method generates all possible consecutive word combinations from a given company name. It's useful for detecting multi-word entities such as multi-word locations or legal identifiers.

### Algorithm:
1. Split the input string `comp_name` into words using spaces.
2. Initialize `combinations` with the split words.
3. For each word in the split list:
   - Create consecutive word combinations by concatenating it with the following words.
4. Return a list of all consecutive combinations.

### Example:
```python
generate_consecutive_word_combinations('the brown fox')
# Returns: ['the', 'brown', 'fox', 'the brown', 'the brown fox', 'brown fox']
```

---

## Get Name Components

```python
def get_name_components(self, comp_name: str) -> dict[str: str]:
```

**Description**: This method takes a company name as input and extracts its raw name, legal identifier, location, and base name. The extracted components are returned as a dictionary.

### Algorithm:
1. Log the start of parsing for `comp_name`.
2. Create an output dictionary `components` with the raw company name as `'raw'`.
3. Clean the input by removing non-alphanumeric characters and converting it to lowercase.
4. Generate all consecutive word combinations from the cleaned company name.
5. Loop through these combinations:
   - If a combination matches a legal identifier in `legal_dict` and hasn't been added yet, add it to `components['legal']`.
   - If a combination matches a location in `locations_dict` and hasn't been added yet, add it to `components['location']`.
6. After removing any matched legal or location terms, set the remaining part of the name as the base name (`'base_name'`).
7. Handle any exceptions by logging errors.
8. Log the completion of parsing, showing the resulting components.
9. Return the `components` dictionary.

### Example:
```python
components = name_components.get_name_components("Apple Inc. California")
# Returns: 
# {
#   'raw': 'Apple Inc. California',
#   'legal': 'inc',
#   'location': 'california',
#   'base_name': 'apple'
# }
```

---

## Get All Name Components

```python
def get_all_name_components(self) -> None:
```

**Description**: This method parses all company names from `companies.txt` using the `get_name_components` method. It then writes the parsed results into a CSV file (`company_names_parsed.csv`).

### Algorithm:
1. Log the start of parsing for all company names.
2. Use Python's multiprocessing `Pool` to parallelize the parsing of company names.
3. For each company name in `company_dict`, apply the `get_name_components` method.
4. Handle any multiprocessing errors and log them.
5. Convert the parsed company components into a Pandas DataFrame.
6. Save the DataFrame as a CSV file (`src/URAP_test_data/company_names_parsed.csv`).
7. Log the completion of parsing.

### Example:
```python
name_components.get_all_name_components()
# Parses all company names and outputs a CSV file with their components.
```
---
## Contains Legal Identifier

```python   
def contains_legal_identifier(self, comp_name: str) -> bool:
```   

**Description**: This method takes a company name as input and determines if it contains a legal identifier. It uses the fine-tuned BERT model to predict the presence of a legal identifier in the company name.

### Algorithm:
1. Tokenize the input company name using the BERT tokenizer.
2. Pad the tokenized sequence to the maximum length.
3. Convert the tokenized sequence to tensor format.
4. Perform inference using the fine-tuned BERT model.
5. Extract the predicted label from the model output.
6. Return `True` if the model predicts the presence of a legal identifier, `False` otherwise.

### Example:
```python
contains_legal_identifier = name_components.contains_legal_identifier("Apple Inc.")
# Returns: True
```
---


## Usage Example

To use the class and parse all company names, simply run the following in the main script:
```python
if __name__ == '__main__':
    name_components = NameComponents()
    name_components.get_all_name_components()
```

This will initialize the class, parse all company names, and store the results in a CSV file.

---




