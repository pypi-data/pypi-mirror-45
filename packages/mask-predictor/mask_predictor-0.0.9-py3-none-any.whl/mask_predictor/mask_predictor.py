import subprocess
import sys
import torch
import spacy
import numpy as np
import json
import logging
from sklearn.cluster import KMeans
from pytorch_pretrained_bert import BertTokenizer, BertModel, BertForMaskedLM

CLS = " [CLS] "
SEP = " [SEP] "
MASK = "[MASK]"
CLASS_NUMBER = 4
PREDICTION_NUMBER = 50
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class Predictor:

    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertForMaskedLM.from_pretrained('bert-base-uncased')
        try:
            self.spacy_model = spacy.load("en_core_web_lg")
        except:
            subprocess.call([sys.executable,'-m','spacy','download','en_core_web_lg'])
            sys.exit('Please restart the program to take effect.')
        self.model.eval()
        self.class_number = 4

    def __predict(self, sentence):
        predicted_words = []
        predicted_confidence = []

        sentence = CLS + sentence + SEP
        tokenized_text = self.tokenizer.tokenize(sentence)
        masked_index = tokenized_text.index("*")
        tokenized_text[masked_index] = MASK
        indexed_tokens = self.tokenizer.convert_tokens_to_ids(tokenized_text)
        tensor = torch.tensor([indexed_tokens])
        tokens_tensor = tensor.to(device)
        self.model.to(device)
        with torch.no_grad():
            predictions = self.model(tokens_tensor)
        predicted_indexes = [tk.item() for tk in torch.topk(predictions[0, masked_index], PREDICTION_NUMBER)[1]]
        confidence = [tk.item() for tk in torch.topk(predictions[0, masked_index], PREDICTION_NUMBER)[0]]
        [predicted_words.append(t) for t in self.tokenizer.convert_ids_to_tokens(predicted_indexes)]
        [predicted_confidence.append(c) for c in confidence]
        word_confidence_list = list(zip(predicted_words, predicted_confidence))
        return word_confidence_list

    def __one_list_per_example(self, predictions_dict):
        new_prediction_dict = {}
        for example_key, sentence in predictions_dict.items():
            new_prediction_dict[example_key] = {}
            for sentence_key, tuple in sentence.items():
                for word, confidence in tuple.items():
                    if word not in new_prediction_dict[example_key]:
                        new_prediction_dict[example_key][word] = confidence
                    else:
                        new_prediction_dict[example_key][word] += confidence
        return new_prediction_dict

    def __cluster(self, predictions_dict):
        clustered_predictions = {}
        for example_key, word_dict in predictions_dict.items():
            clustered_predictions[example_key] = {}
            doc_list = [self.spacy_model(word) for (word, con) in word_dict.items()]
            kmeans = KMeans(n_clusters=CLASS_NUMBER, random_state=0).fit([d.vector for d in doc_list])
            for i in range(len(kmeans.labels_)):
                class_number = str(kmeans.labels_[i])
                # if not common words or punctuation
                if any(d.is_punct is True or d.is_stop is True or d.is_alpha is False for d in doc_list[i]) is False:
                    # add class number if not existed
                    if class_number not in clustered_predictions[example_key]:
                        clustered_predictions[example_key][class_number] = {}
                    lemma_str = " ".join([d.lemma_ for d in doc_list[i]])
                    if lemma_str not in clustered_predictions[example_key][class_number]:
                        query_key = list(predictions_dict[example_key].keys())[i]
                        clustered_predictions[example_key][class_number][lemma_str] = predictions_dict[example_key][query_key]
        return clustered_predictions

    def __sort(self, clustered_predictions):
        AVERAGE_CONFIDENCE = "AVERAGE_CONFIDENCE"
        #sort word_dict
        for example_key, clustered_class in clustered_predictions.items():
            #average confidence for each class
            for class_i, word_dict in clustered_class.items():
                sorted_word = sorted(word_dict.items(), key = lambda k: k[1], reverse=True)
                sorted_word_dict = dict(sorted_word)
                clustered_predictions[example_key][class_i] = sorted_word_dict
                total_confidence = [c for (w,c) in word_dict.items()]
                average_confidence = sum(total_confidence) / len(total_confidence)
                clustered_predictions[example_key][class_i][AVERAGE_CONFIDENCE] = average_confidence

        for example_key, clustered_class in clustered_predictions.items():
            #sort classes by average confidence
            sorted_classes = sorted(clustered_class.items(), key=lambda k: k[1][AVERAGE_CONFIDENCE], reverse=True)
            #change class number
            sorted_classes = [(i, s[1]) for i, s in enumerate(sorted_classes)]
            sorted_classes_dict = dict(sorted_classes)
            #remove average confidence
            [sorted_classes_dict[i].pop(AVERAGE_CONFIDENCE, None) for i in sorted_classes_dict]
            clustered_predictions[example_key] = sorted_classes_dict

        return clustered_predictions


    def predict(self, input_json):
        input_obj = json.loads(input_json)
        predictions_dict = {}
        for example_key in input_obj:
            example = {}
            for sentence in input_obj[example_key]:
                example[sentence] = {}
                p = self.__predict(sentence)
                for (w,c) in p:
                    example[sentence][w] = c
            predictions_dict[example_key] = example
        predictions_dict = self.__one_list_per_example(predictions_dict)

        clustered_predictions = self.__cluster(predictions_dict)

        clustered_predictions = self.__sort(clustered_predictions)

        return clustered_predictions
