from article_processor import TextProcessor
from tqdm import tqdm

import json
import numpy as np
import sys
import copy as copy
import pdb

class TFIDFCalculator():
    def __init__(self, idf_record_file, document_record_file):
        self.processor = TextProcessor()
        self.idf_record_file = idf_record_file
        self.document_record_file = document_record_file

        with open(self.idf_record_file, "r") as fp:
            self.idf_record = json.load(fp)

        with open(self.document_record_file, "r") as fp:
            self.document_record = json.load(fp)["all_documents"]

        self.total_vocab = len(self.idf_record.keys())
        self.vocab_list = list(self.idf_record.keys())

        # get the initialized feature vector to calculate tf
        # using the corpus size
        self.feat_vec = np.zeros((self.total_vocab))

        self.idf_vec = self.construct_idf_vec()
        self.tf_doc = self.tf_cal_doc()

        self.tf_idf_feat_doc = self.tf_doc*self.idf_vec

    def tf_cal_doc(self):
        
        # get the corpus feature vector
        all_doc_tf_vec = []
        print("---Calculating document tf---")
    
        for doc_id, doc_content in enumerate(tqdm(self.document_record)):
            this_feat_vec = copy.copy(self.feat_vec)
            stat_term_doc = doc_content["stat_term_freq"]
            max_occur = 0
            for [word, score] in stat_term_doc:
                idx_word_corpus = self.vocab_list.index(word)
                this_feat_vec[idx_word_corpus] = score
                max_occur = max(max_occur, this_feat_vec[idx_word_corpus])

            # normalize the vector 
            if max_occur != 0:
                this_feat_vec /= max_occur
            all_doc_tf_vec.append(this_feat_vec)

        return np.array(all_doc_tf_vec)

    def construct_idf_vec(self):
        idf_vec = copy.copy(self.feat_vec)
        for word in self.idf_record:
            idx_word = self.vocab_list.index(word)
            idf_vec[idx_word] = self.idf_record[word]

        return idf_vec

    def tf_cal_query(self, query):
        processed_query = self.processor.standard_process_sentence(query).split(" ")
        print("Processed query:", processed_query)

        query_tf_feat = copy.copy(self.feat_vec)
        max_occur = 0
        for word in processed_query:
            if word not in self.vocab_list:
                # ignore new word
                continue

            idx_word = self.vocab_list.index(word)
            query_tf_feat[idx_word] += 1
            max_occur = max(max_occur, query_tf_feat[idx_word])

        query_tf_feat /= max_occur
        return query_tf_feat, processed_query

    def rank_result(self, terms_of_query, tf_idf_query_feat, num_res, res_file_json):
        # method 1: dot product
        ranking_score = np.dot(self.tf_idf_feat_doc, tf_idf_query_feat)


        res_doc_idx = np.argsort(ranking_score)[::-1][:num_res]
        res_doc_score = ranking_score[res_doc_idx]

        res = []
        # Constructing result and reasoning
        for doc_idx, score in zip(res_doc_idx, res_doc_score):
            # get frequency of query term in each document for reasoning
            selected_freq_terms = {}
            for [each_term, freq_term] in self.document_record[doc_idx]['stat_term_freq']:
                if each_term in terms_of_query:
                    selected_freq_terms[each_term] = freq_term

            res.append({'Text': self.document_record[doc_idx]["ori_text"], 
                        'Score': score,
                        'freq_terms_in_query': selected_freq_terms, 
                        'doc_idx': str(doc_idx)})



        with open(res_file_json, "w") as fp:
            json.dump(res, fp, indent=4)

    def retrieve_result(self, query, num_res, res_file_json):
        tf_feat_vec, terms_of_query = self.tf_cal_query(query)
        tf_idf_feat_query = tf_feat_vec*self.idf_vec

        self.rank_result(terms_of_query, tf_idf_feat_query, num_res, res_file_json)




if __name__ == "__main__":
    idf_record_file = 'D:\ICT\Coursework\IR\W3_ex_TFIDF\corpus.json'
    document_record_file = 'D:\ICT\Coursework\IR\W3_ex_TFIDF\standard_all_documents.json'
    res_file_json = './retrieved_relevant_text.json'
    test = TFIDFCalculator(idf_record_file, document_record_file)

    test_query = "president in dangerous"
    num_res = 20

    test.retrieve_result(test_query, num_res, res_file_json)
    print("Returned results in ", res_file_json)



