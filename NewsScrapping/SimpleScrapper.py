from newspaper import Article

# url = "https://www.bloomberg.com/news/articles/2020-08-01"
url = "https://www.nytimes.com/2020/03/20/business/coronavirus-news-sites.html"

# download and parse article
article = Article(url)
article.download()
article.parse()
article.nlp()

# print article text
print(article.text)
# print(article.keywords)
# print(article.summary)
print(article.authors)