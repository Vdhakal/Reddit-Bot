import os
import re
import requests
import praw
import configparser
import concurrent.futures
import argparse


class redditImageScraper:
    def __init__(self, nsfw=False):
        config = configparser.ConfigParser()
        config.read('conf.ini')
        self.sub = 'dankmemes'
        self.limit = 10
        self.order = 'hot'
        self.nsfw = nsfw
        self.path = f'images/{self.sub}/'
        self.reddit = praw.Reddit(client_id=config['REDDIT']['client_id'],
                                  client_secret=config['REDDIT']['client_secret'],
                                  user_agent='Multithreaded Reddit Image Downloader v2.0 (by u/impshum)')

    def download(self, image):
        r = requests.get(image['url'])
        with open(image['fname'], 'wb') as f:
            f.write(r.content)

    def start(self):
        images = []
        try:
            comment = self.reddit.subreddit(self.sub).hot(limit=None)
            submissionList = []
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                submissionList.append(comment)

            for submission in submissionList:
                print(submission.url)
                if not submission.stickied and submission.over_18 == self.nsfw \
                        and submission.permalink.endswith(('jpg', 'jpeg', 'png')):
                    fname = self.path + \
                        re.search('(?s:.*)\w/(.*)',
                                  submission.url).group(1)
                    if not os.path.isfile(fname):
                        images.append(
                            {'url': submission.url, 'fname': fname})
                        print(submission.title)
            if len(images):
                if not os.path.exists(self.path):
                    os.makedirs(self.path)
                with concurrent.futures.ThreadPoolExecutor() as ptolemy:
                    ptolemy.map(self.download, images)
        except Exception as e:
            print(e)

    def imgProcessor(self):
        print(1)


def main():
    scraper = redditImageScraper()
    scraper.start()
    scraper.imgProcessor()


if __name__ == '__main__':
    main()
