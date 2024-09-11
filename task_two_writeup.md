# Task Two Writeup

### Task Overview
To predict the usage of a legal identifier within a company name without checking against a list of legal identifier words, 
such as in legal.tsv, I fine-tuned a pre-trained [Google BERT model](https://huggingface.co/google-bert/bert-base-cased) on 
the dataset generated in task 1. 

### Use of Hugging Face API
I primarily used the Hugging Face `transformers` and `datasets` library to fine-tune the BERT model. 

First, I used the `datasets` library to load the dataset generated in task 1 and post it to Hugging Face at [TalonMeyer/URAP_interview_task_dataset](https://huggingface.co/datasets/TalonMeyer/URAP_interview_task_dataset). 

Then, I used the `transformers` library to load the pre-trained BERT model and fine-tune it on the dataset to recognize if a company name 
contained a legal identifier. This way, someone without a list of legal jargon can ascertain if a company name contains a legal identifier by
simply running inference on the model. 

Once the model training was complete I pushed the model to Hugging Face at [TalonMeyer/bert-base-cased-legal-keyword-identifier](https://huggingface.co/TalonMeyer/URAP_interview_task_model)
and implemented it in the `NameComponents` class.

### Use of Google Colab
The actual Jupiter notebook used to load the dataset and fine-tune the model was run on Google Colab to take advantage of the free GPU service.


### Possible Improvements
With more time I would like to create a new model which also predicts the location of the legal identifier within the company name. 
This could be done in a similar manner to the current model, but instead of a binary choice of classes (either the company name contains a legal identifier or it does not)
the model would have multiple classes, each representing the index of the legal identifier within the company name.

Another obvious improvement would be to train a larger model on a larger dataset. The dataset used in this task was relatively small, and a larger dataset with more varied legal identifiers would likely improve the model's performance.

If time permitted, I would also have liked to experiment with other pre-trained models to find the most optimal fit for our
dataset.

### Citation

**google/bert-base-cased**:
```
@article{DBLP:journals/corr/abs-1810-04805,
  author    = {Jacob Devlin and
               Ming{-}Wei Chang and
               Kenton Lee and
               Kristina Toutanova},
  title     = {{BERT:} Pre-training of Deep Bidirectional Transformers for Language
               Understanding},
  journal   = {CoRR},
  volume    = {abs/1810.04805},
  year      = {2018},
  url       = {http://arxiv.org/abs/1810.04805},
  archivePrefix = {arXiv},
  eprint    = {1810.04805},
  timestamp = {Tue, 30 Oct 2018 20:39:56 +0100},
  biburl    = {https://dblp.org/rec/journals/corr/abs-1810-04805.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

