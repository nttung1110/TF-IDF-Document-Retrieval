from article_processor import *
from tqdm import tqdm
import pdb
import numpy as np
# nltk.download('stopwords')
# nltk.download('wordnet')

def build_standarize_document_repo(json_path_in, json_path_out):
    print("----Building standard documents and constructing frequency of all terms in each document----")
    processor = TextProcessor()

    json_res = {"all_documents": []}

    with open(json_path_in, "r") as fp:
        article_data = json.load(fp)['newspapers']['foxnews']['articles']

    for idx, each_article in enumerate(tqdm(article_data)):
        freq_term_doc = {}
        title_article = each_article["title"]
        text_article = each_article["text"]

        # if title_article != "":
        #     converted_title_article = processor.standard_process_sentence(title_article)

        if text_article != "":
            converted_text_article = processor.standard_process_sentence(text_article)
            for term in converted_text_article.split(" "):
                if term not in freq_term_doc:
                    freq_term_doc[term] = 0
                freq_term_doc[term] += 1
            freq_term_doc = sorted(freq_term_doc.items(), key=lambda x:x[1], reverse=True)
        else:
            converted_text_article = ""
            freq_term_doc = []

        record = {}
        record['id'] = idx
        record['ori_title'] = title_article
        # record['converted_title'] = converted_title_article
        record['ori_text'] = text_article
        record['converted_text'] = converted_text_article
        record['stat_term_freq'] = freq_term_doc

        json_res["all_documents"].append(record)

    with open(json_path_out, "w") as fp:
        json.dump(json_res, fp, indent=4)

    print("----Finish building standard document----")

def build_standardize_corpus(json_path_documents, json_path_corpus_out):
    processor = TextProcessor()

    print("----Building corpus from saved documents and pre-calculate the idf for corpus----")

    list_corpus_with_idf_score = {}

    with open(json_path_documents, "r") as fp:
        article_data = json.load(fp)["all_documents"]

    num_documents = len(article_data)

    for each_article in tqdm(article_data):
        # title_article = each_article["converted_title"]
        text_article = each_article["converted_text"]

        unique_corpus_document = []

        # if title_article != "":
        #     tokenize_sentence = processor.tokenizer(title_article)
        #     for word in tokenize_sentence:
        #         processed_word = processor.standard_process_word(word)
        #         if processed_word is None:
        #             continue

        #         list_corpus_with_idf_score.append(processed_word)
        if text_article != "":
            processed_sentence = text_article.split(" ")
            
            for processed_word in processed_sentence:
                if processed_word is None:
                    continue

                if processed_word not in unique_corpus_document:
                    unique_corpus_document.append(processed_word)
                    if processed_word not in list_corpus_with_idf_score:
                        list_corpus_with_idf_score[processed_word] = 0
                    list_corpus_with_idf_score[processed_word] += 1


    # normalize the idf corpus score
    for word in list_corpus_with_idf_score:
        list_corpus_with_idf_score[word] = np.log(num_documents/(1+list_corpus_with_idf_score[word]))
    # sort the vocab
    list_corpus_with_idf_score = dict(sorted(list_corpus_with_idf_score.items()))
    with open(json_path_corpus_out, "w") as fp:
        json.dump(list_corpus_with_idf_score, fp, indent=4)

    print("----Finish building corpus----")

def test(json_path):
    
    processor = TextProcessor()
    with open(json_path, "r") as fp:
        article_data = json.load(fp)['newspapers']['foxnews']['articles']

    for each_article in article_data:
        title_article = each_article["title"]
        if title_article == "":
            continue

        res = processor.standard_process_sentence(title_article)
        print("Original:", title_article)
        print("Procecssed:", res)
        pdb.set_trace()



if __name__ == "__main__":
    json_path = "./newsPaperData.json"
    json_path_standardized_document = "./standard_all_documents.json"
    json_path_corpus_out = './corpus.json'

    build_standarize_document_repo(json_path)
    build_standardize_corpus(json_path_standardized_document, json_path_corpus_out)
