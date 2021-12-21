import newspaper
import requests
import json

class myNewsCrawler():
    data = {}
    
    def __init__(self,companies):
        self.companies = companies
        self.newsPaper = {}
        self.data['newspapers'] = {}
        self.limit = 100

    def downloadHtml(self):    
        for company, value in self.companies.items():
            count = 1
            newsPaper = {
                "articles": []
            }

            articleList = []
            if company == "cnn":
                articleList = self.get_cnn_url(value["link"])
            elif company == "foxnews":
                articleList = self.get_fox_url(value["link"])

            for content in articleList: 
                if count > self.limit:
                    break

                content = newspaper.Article(content)
                article = {}
                article['link'] = content.url
                try:
             
                    content.download()
                    print(count, "download articles from", company, "url: ", content.url)
                    
                except:
                    continue

                article.update(self.cleanHtml(content.html))
                count +=1 

                newsPaper['articles'].append(article)
                   
            self.data['newspapers'][company] = newsPaper
            with open("./newsPaperData.json", "w") as fp:
                json.dump(self.data, fp, indent=4)
            # open("newsPaperData.json","wb").write(str(self.data).encode('UTF-8'))
            print(".....................................................")



    def findWord(self,word):  
        find = 0

        d = open("newsPaperData.json","rb").read()
        newsArticles = eval(d)
        newsArticles = newsArticles["newspapers"]
        for x ,y in newsArticles.items():
            for article in y["articles"]:
                findInTitle = article["title"].find(word)                
                findInText = article["text"].find(word)
                if findInTitle != -1 or findInText != -1:
                    find +=1
                    
                    print(find ,"find","'"+word+"'" ,"in " +x+" url:",article["link"])






    def cleanHtml(self,h):
        article = newspaper.Article(url='')
        article.set_html(h)
        article.parse()

        articleJ = {}
        articleJ['title'] = article.title
        articleJ['text'] = article.text
        return articleJ


    def get_cnn_url(self,url):
        r = requests.get(url)
        
        st = str(r.content)
        artiIndex = st.find('{"articleList":')
        st = st[artiIndex:]
        artiIndex = st.find(", registryURL:")
        st = st[:artiIndex]
        l  = st.split('"uri":"')
        cnn_urls = []
        for x in l:
            htmlStart = x.find('index.html')
            if htmlStart != -1   :
                htmlStart =  htmlStart + len('index.html')  
                cnn_urls.append(url + x[:htmlStart])

        return cnn_urls


    def get_fox_url(self,url):
        paper = newspaper.build(url,memoize_articles=False)
        fox_urls = []
        for content in paper.articles:
            fox_urls.append(content.url)
        return fox_urls