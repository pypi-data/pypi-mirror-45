from sgwc import get_hot_articles

for article in get_hot_articles(10):
    article.save_article('markdown')
