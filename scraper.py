import csv
import datetime as dt

import seaborn as sns

sns.set(style='darkgrid', context='talk', palette='Dark2')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import praw
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

client_id = 'FaqB-B_IZsJKmA'
client_secret = 'mXRNwvS6tFy36uuyJnYunDqw0jkRvw'
user_agent = 'scraper'
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

sia = SIA()
characters = ['albedo', 'amber', 'ayaka', 'barbara', 'beidou', 'bennett', 'chongyun', 'diluc', 'diona', 'fischl',
              'ganyu', 'hu tao', 'jean', 'kaeya', 'keqing', 'klee', 'lisa', 'mona', 'ningguang', 'noelle', 'qiqi',
              'razor', 'sucrose', 'tartaglia', 'traveler', 'venti', 'xiangling', 'xiao', 'xingqiu', 'xinyan', 'zhongli']


def get_date(created):
    return dt.datetime.fromtimestamp(created)


# .search('flair:"discussion"', sort='top', time_filter='month', limit=100):
def allTopPosts():
    result = {}
    propernouns = {}
    topChars = {}

    char_scores = csv.writer(
        open('C:/Users/Jerry/Desktop/RedditScraper/char_scores.csv', 'w', encoding='utf-8', newline=''))
    char_scores.writerow(['Flair', 'Character', 'Score'])

    post_scores = csv.writer(
        open('C:/Users/Jerry/Desktop/RedditScraper/post_scores.csv', 'w', encoding='utf-8', newline=''))
    post_scores.writerow(['Flair', 'Negative', 'Neutral', 'Positive', 'Compound'])

    for post in reddit.subreddit('Genshin_Impact').top(limit=100, time_filter='month'):
        flair = post.link_flair_text
        if flair not in result:
            result[flair] = {'count': 1, 'post_scores': [], 'total_score': 0, 'pos_posts': 0, 'neg_posts': 0}
        else:
            result[flair]['count'] += 1

        taggedtitle = pos_tag(word_tokenize(post.title))
        nnps = ''
        for word, pos in taggedtitle:
            if pos == 'NNP':
                nnps += word + ' '
        score = sia.polarity_scores(post.title)
        if score['compound'] != 0:
            result[flair]['post_scores'].append(score)
            result[flair]['total_score'] += score['compound']
            post_scores.writerow([flair, score['neg'], score['neu'], score['pos'], score['compound']])
        if score['compound'] < 0:
            result[flair]['neg_posts'] += 1
        elif score['compound'] > 0:
            result[flair]['pos_posts'] += 1

        # if nnps != '':
        #     nnps = nnps[:-1]
        #     if nnps not in propernouns:
        #         propernouns[nnps] = post.score
        #     else:
        #         propernouns[nnps] += post.score

        for word in list(set(word_tokenize(post.title.lower()))):
            if word in characters:
                char_scores.writerow([flair, word, post.score])
                if word not in topChars:
                    topChars[word] = post.score
                    result[flair][word] = post.score
                else:
                    topChars[word] += post.score
                    if word in result[flair]:
                        result[flair][word] += post.score
                    else:
                        result[flair][word] = post.score

    for flair in result:
        result[flair]['avg_score'] = round(
            (result[flair]['total_score'] / max(len(result[flair]['post_scores']), 1)), 2)

    # print(result)

    # with open('C:/Users/Jerry/Desktop/RedditScraper/result.json', 'w') as outfile:
    #     json.dump(result, outfile)


# .search('flair:"discussion"', sort='top', time_filter='month', limit=100):
# def topDiscussionPosts():
#     result = {}
#     propernouns = {}
#     topChars = {}
#
#     # char_scores = csv.writer(
#     #     open('C:/Users/Jerry/Desktop/RedditScraper/disc_char_scores.csv', 'w', encoding='utf-8', newline=''))
#     # char_scores.writerow(['Flair', 'Character', 'Score'])
#     #
#     # post_scores = csv.writer(
#     #     open('C:/Users/Jerry/Desktop/RedditScraper/disc_post_scores.csv', 'w', encoding='utf-8', newline=''))
#     # post_scores.writerow(['Flair', 'Negative', 'Neutral', 'Positive', 'Compound'])
#
#     for post in reddit.subreddit('Genshin_Impact').search('flair:"discussion"', sort='top', time_filter='month', limit=100):
#         flair = post.link_flair_text
#         if flair not in result:
#             result[flair] = {'count': 1, 'post_scores': [], 'total_score': 0, 'pos_posts': 0, 'neg_posts': 0}
#         else:
#             result[flair]['count'] += 1
#
#         taggedtitle = pos_tag(word_tokenize(post.title))
#         nnps = ''
#         for word, pos in taggedtitle:
#             if pos == 'NNP':
#                 nnps += word + ' '
#         score = sia.polarity_scores(post.title)
#         if score['compound'] != 0:
#             result[flair]['post_scores'].append(score)
#             result[flair]['total_score'] += score['compound']
#             # post_scores.writerow([flair, score['neg'], score['neu'], score['pos'], score['compound']])
#         if score['compound'] < 0:
#             result[flair]['neg_posts'] += 1
#         elif score['compound'] > 0:
#             result[flair]['pos_posts'] += 1
#
#         if nnps != '':
#             nnps = nnps[:-1]
#             if nnps not in propernouns:
#                 propernouns[nnps] = post.score
#             else:
#                 propernouns[nnps] += post.score
#     print(result)
#     print(propernouns)

            # for word in list(set(word_tokenize(post.title.lower()))):
            #     if word in characters:
            #         char_scores.writerow([flair, word, post.score])
            #         if word not in topChars:
            #             topChars[word] = post.score
            #             result[flair][word] = post.score
            #         else:
            #             topChars[word] += post.score
            #             if word in result[flair]:
            #                 result[flair][word] += post.score
            #             else:
            #                 result[flair][word] = post.score

    # for flair in result:
    #     result[flair]['avg_score'] = round(
    #         (result[flair]['total_score'] / max(len(result[flair]['post_scores']), 1)), 2)

    # title = word_tokenize(re.sub('[^a-zA-Z]+', ' ', post.title))
    # for word in title:
    #     word = word.lower()
    #     if word not in stopwords.words():
    #         if word not in title_words:
    #             title_words[word] = 1
    #         else:
    #             title_words[word] += 1
    # print(title_words)

    # body = word_tokenize(re.sub(r'\W+', ' ', post.selftext))
    # for word in body:
    #     word = word.lower()
    #     if word not in stopwords.words():
    #         if word not in body_words:
    #             body_words[word] = 1
    #         else:
    #             body_words[word] += 1

    # print(reddit.submission(id="ks37c4").link_flair_text)
    # pprint(vars(reddit.submission(id="jeo9hj")))

    # with open('C:/Users/Jerry/Desktop/RedditScraper/topPostTitleWords.json', 'w') as outfile:
    #     sortedTitles = dict(sorted(title_words.items(), key=lambda item: item[1], reverse=True))
    #     json.dump(sortedTitles, outfile)
    #
    # with open('C:/Users/Jerry/Desktop/RedditScraper/topPostBodyWords.json', 'w') as outfile:
    #     sortedBody = dict(sorted(body_words.items(), key=lambda item: item[1], reverse=True))
    #     json.dump(sortedBody, outfile)
    #
    # with open('C:/Users/Jerry/Desktop/RedditScraper/topresult.json', 'w') as outfile:
    #     sortedresult = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
    #     json.dump(sortedresult, outfile)


if __name__ == "__main__":
    allTopPosts()
    # topDiscussionPosts()