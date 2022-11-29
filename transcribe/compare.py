import spacy
import transcribe.assemblyai
import csv
# import en_core_web_sm

# Mean Error Rate
# from Levenshtein import distance as levenshtein_distance
# nlp = spacy.load('en_core_web_sm')

def compare(bill_id):
    ground_truth = parse_file_to_str(f'true_{bill_id}.txt')
    assembly = parse_file_to_str(f'{bill_id}.txt')
    return ground_truth, assembly

def metrics(groundtruth, predicted):
    ground_truth_nlp = nlp(groundtruth)
    assembly_nlp = nlp(predicted)
    num_words_groundtruth = len([token.text for token in ground_truth_nlp if token.is_stop != True and token.is_punct != True])
    num_words_predicted = len([token.text for token in assembly_nlp if token.is_stop != True and token.is_punct != True])
    num_nouns_groundtruth = len([token.text for token in ground_truth_nlp if token.is_stop != True and token.is_punct != True and token.pos_ == "NOUN"])
    num_nouns_predicted = len([token.text for token in assembly_nlp if token.is_stop != True and token.is_punct != True and token.pos_ == "NOUN"])
    sim = assembly_nlp.similarity(ground_truth_nlp)
    return num_words_groundtruth, num_words_predicted, num_nouns_groundtruth, num_nouns_predicted, sim


def parse_file_to_str(filename):
    final_str = ""
    with open(filename) as f:
        temp = [line.strip() for line in f.readlines()]
        final_str = ' '.join(temp)
    return final_str
