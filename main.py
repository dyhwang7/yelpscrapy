from scrapingproject.scrapingproject.spiders import ourfirstbot
from scrapy.crawler import CrawlerProcess
import pandas as pd
import csv
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


def read_df(df):
    with open('output.csv', 'r', encoding="utf8") as infile:
        reader = csv.reader(infile)
        header = next(reader)
        if header != None:
            for rows in reader:
                mydict = {
                    'name': rows[0],
                    'description': rows[1],
                    'rating': float(rows[2]),
                    'review_count': float(rows[3])}
                df = df.append(mydict, ignore_index=True)
    df.columns = ['name', 'description', 'rating', 'review_count']

    return df


def print_df(split_list):
    for i in range(len(split_list)):
        print(split_list[i])
    return split_list


def sort_df(split_list):
    for i in range(len(split_list)):
        split_list[i] = split_list[i].sort_values(by='review_count', ascending=False)
    return split_list


def split_df(df):
    print(df)
    split_list = []
    for i in range(5):
        if i < 4:
            split_output = df[(df['rating'] >= i) and (df['rating'] < i + 1)]
        else:
            split_output = df[(df['rating'] >= i) and (df['rating'] <= float(i + 1))]
        split_list.append(split_output)
    return split_list


def word_cloud(df):
    comment_words = ''
    stopwords = set(STOPWORDS)

    for val in df:
        val = str(val)
        tokens = val.split()
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
        comment_words += " ".join(tokens) + " "

    wordcloud = WordCloud(width=800, height=800,
                          background_color='white',
                          stopwords=stopwords,
                          min_font_size=10).generate(comment_words)

    # plot the WordCloud image
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    plt.show()


process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 ' \
                                        '(KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'})
process.crawl(ourfirstbot.OurfirstbotSpider)
process.start()

output = pd.DataFrame()
output = read_df(output)

split_list = []
split_list = split_df(output)
split_list = sort_df(split_list)
print_df(split_list)

output_description = output['description']
word_cloud(output_description)

# try on colab
# no need for 1 function modules combine into one
# reorder indices by .reset_index
