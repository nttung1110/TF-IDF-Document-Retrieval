# TF-IDF-Document-Retrieval

## Introduction

My self-implementation for TF-IDF algorithm to retrieve documents given text query. 

The process of my retrieval pipeline can be divided into four steps:

+ Crawling the data
+ Building the documents by standardizing texts
+ Building the corpus
+ Perform retrieval by specifying the query

## Environment Settings

```
conda create --name tf_idf python=3.7
conda activate tf_idf
pip install requirements.txt
```

Note that you should run the two lines of code for installing the packages of nltk

You can install it via interactive terminal

```
python
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
exit()
```

## TF-IDF Document Retrieval
### Crawling the data

The very first step in any retrieval problem is to crawling the information. In this problem, I made use of off-the-shelf codes implemented by [] to perform crawling the data
from Internet source. You can specify your crawling options in `web_scrapping/main.py` from line 5 to 10. After that, run the following command to crawl the documents 
and it will be saved in ```newsPaperData.json```

```
cd web_scrapping
python main.py
cd ..
```

### Building documents and corpus
Since documents from Internet source contains unexpected characters which might confuse the machine, we must perform some pre-processing steps: 
+ Lowercase
+ Remove punctuation, stopwords
+ Tokenization

To perform the above steps, specify two variables **json_path** and **json_path_standardized_document** which are the input documents(which will be ```newsPaperData.json``` as above if you don't change the path) and the output documents
being standardized in ```document_corpus_builder.py```. Also, the vocabulary set of documents are extracted(specify variable **json_path_corpus_out**) using similar standardization techniques.

In TF-IDF algorithm, it is more efficient to calculate some prerequisite terms such as the frequencies of term in each document as well as the IDF score for each word in the corpus. The following
script was used to build all of the above stuffs. 

```
python document_corpus_builder.py
```

### Perform retrieval
In this setting, the similarity score of query and document feature vectors were calculated by performing dot product between two vector.
Specify two variables **test_query** and **num_res** which are the query input to the system and number of returned results that you expect. The result will be saved in 
a json file ```retrieved_relevant_text.json``` after running the script:

```
python TFIDF_calculator.py
```

The returned result stored in the file after performing retrieval is a list of dictionary. Each stores text of document being retrieved, relevant scores, document idx, and 
the frequency of interested terms in the document. This frequency points out the distribution of term (which belongs to the query) with respect to specific document. This can be used
to perform analysis on the effects of the algorithm for making any improvement on it.

## Comments
The frequency of existed terms recorded in the results file would help you to identify the reasons of ranking documents in such order. You can map the key $doc_idx$ to corresponding
document index in ```standard_all_documents.json``` file to observe it.

In conclusion, the TF-IDF algorithm is quite effective in retrieving those documents which have similar distribution of terms as the query. You can try the query *president is in dangerous* to
see how it is effective. Those documents which have higher frequency in the existence of query terms does not always have higher score than the remaining ones since the algorithm
tries to balance the. However, the algorithm might fail to capture the semantical meaning of the query as well as the orders in which terms in query are arranged.
