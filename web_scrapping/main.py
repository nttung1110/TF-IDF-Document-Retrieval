from newsCrawler import myNewsCrawler
import sys


word = "Trump"
num_limit = 100
newsPapers = {
    "foxnews": {"link": "http://www.foxnews.com/"}
    #, "cnn": {"link": "https://edition.cnn.com"}
}

def main():
    # if len(sys.argv) == 2:
    #     word = sys.argv[1]
    s = myNewsCrawler(newsPapers, num_limit)
    s.downloadHtml()
    # s.findWord(word)


if __name__ == "__main__":
    main()

    # https://github.com/adielw8/news-crawler