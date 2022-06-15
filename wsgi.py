# CUNT (Continutally Updating Nature Textposts)
# By: jackzachson (Zach Jackson)

import random
import requests
import time
import operator
import logging
import praw
import config
import json
import urllib.request
from bs4 import BeautifulSoup

from flask import Flask, render_template
from multiprocessing import Pool
from requests import ReadTimeout
from PIL import Image
from io import BytesIO

app = Flask(config.APP_NAME)

# Open Reddit API
r = praw.Reddit(user_agent=config.REDDIT_USER_AGENT, client_id=config.REDDIT_CLIENT_ID,
                client_secret=config.REDDIT_CLIENT_SECRET)

# logging config
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
log_levels = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warn': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL}

try:
    logger.setLevel(log_levels[config.LOG_LEVEL])
except KeyError:
    logger.setLevel(logging.INFO)
    logger.error('Invalid logging level, log level set to INFO')
    logger.info("Valid values: 'debug', 'info', 'warn', 'error', or 'critical'")

logger.debug("Logging configuration complete")


################################################################################


def get_posts(sub):
    """Gets the content from requested subreddit (len >= 1)
    
    :param str sub: subreddit to scrape posts from
    :return: list of posts in given subs
    :rtype: list
    """

    logger.info('Getting posts from sub: {}'.format(sub))
    s = r.subreddit(sub)
    while True:  # Repeat until we don't get an error
        try:
            p = s.top(time_filter="week", limit=config.REDDIT_NUM_POSTS)
            break  # Exits the while loop once content is retrieved successfully

        # Had trouble with TypeError raised when connection is buffering too
        # long, which one would think is the same as ReadTimeout.
        except (TypeError, ReadTimeout) as e:
            logger.error('{}: {}'.format(type(e).__name__, str(e)))

    return list(p)


def get_new_list(l):
    """Builds a list of posts
    based on input list of subs
    
    :param list l: list of subs to get content from
    :return: list of Reddit posts
    :rtype: list
    """

    logger.info('Getting new list of posts')
    start_time = time.time()

    p = Pool(processes=len(l))
    data = p.map(get_posts, l)
    p.close()

    # p.map returns 2D list, return for this function needs to be 1D
    # the code below flattens it.
    ret = [item for sublist in data for item in sublist]

    end_time = time.time()
    logger.info('Finished in {0:.2f} seconds'.format(end_time - start_time))
    return ret


'''def get_album_image(url):
    """Given an imgur album URL, returns a valid direct
            Imgur URL to a random image in the album

        :param str url: the url of the album
        :return: url direct to the image
        :rtype: str
        """
    logger.info('Expanding imgur album.  URL: {}'.format(url))
    album_id = url.split('/')[-1]
    images = imgur_client.get_album_images(album_id=album_id)
    return random.choice(images).link'''

'''def get_gallery_image(url):
     """Given an imgur gallery URL, returns a valid direct
            Imgur URL to a random image in the gallery

        :param str url: the url of the gallery
        :return: url direct to the image
        :rtype: str
        """

    gallery_id = url.split('/')[-1]
    images = imgur_client.get_custom_gallery(gallery_id=gallery_id)
    return random.choice(images).link'''


def fix_imgur(img_url):
    """Given an URL, checks if it is an Imgur URL, and returns a valid
        direct Imgur URL
    
    :param str img_url: the url of the image to check
    :return: corrected url direct to the image
    :rtype: str
    """

    # logger.debug('URL is: {}'.format(img_url))
    if '?' in img_url and 'imgur' in img_url:
        img_url = img_url.split('?')[0]

    if 'imgur.com/a/' in img_url:
        pass
        # return get_album_image(img_url)
    # elif 'imgur.com/gallery/' in url:
    #    return get_gallery_image(url)
    elif 'imgur' in img_url and 'i.i' not in img_url and 'iob.i' not in img_url:
        if 'https' in img_url:
            img_url = img_url[0:8] + 'i.' + img_url[8:] + '.png'
        else:
            img_url = img_url[0:7] + 'i.' + img_url[7:] + '.png'
    return img_url


def create_check_size(min_w, min_h, logic_='and'):
    """Create a function to check the minimum size of images.

    Acceptable values for ``logic`` are 'and' or 'or'. All other values
    are silently ignored. The default is 'and'.

    :param str logic_: whether one ('or') or both ('and') minimums must be met
    :param int min_w: minimum width in pixels
    :param int min_h: minimum height in pixels
    :return: function that accepts a URL and returns False if the image does 
             not meet requirements.
    :rtype: function
    """

    # Get the right logic function. We'll use it later.
    op = operator.__and__
    if logic_ == 'or':
        op = operator.__or__

    # Define our custom checksize function.
    def check_size_inner(url):
        """Given a url, return True if the image meets size requirements.

        :param str url: the url of the image to check
        :return: True if the image meets size requirements, False otherwise
        :rtype: bool
        """
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
        except (OSError, IOError) as e:
            logger.error('{}: {}'.format(type(e).__name__, e))
            logger.error('Image URL = {}'.format(url))
            logger.debug('In check_size')
            return False

        # Here's where we use the right logic.
        w, h = img.size
        logger.debug('Image size is {}x{}'.format(w, h))
        return op(w >= min_w, h >= min_h)

    # Return the custom function to the caller.
    return check_size_inner


def is_good_image(img_url):
    """Given an URL, determine if the url points to a file of type jpg or png,
    is greater than a desired size, and does not point to a gallery
    
    :param str img_url: url to determine if points to valid image
    :return: True if valid image, False otherwise
    :rtype: bool
    """

    logger.debug('Check if URL is good image: {}'.format(img_url))
    return 'gallery' not in img_url and \
           ('.jpg' in img_url[-5:] or '.png' in img_url[-5:]) and \
           check_size(img_url)


check_size = create_check_size(config.IMAGE_MIN_HEIGHT, config.IMAGE_MIN_WIDTH, config.IMAGE_LOGIC)


def get_shitpostbot_twitter_post():
    """Get a random tweet'd image from ShitPostBot5000 and return the url.
    This is relativly repeat safe since ShitPostBot5000 tweets a lot, thus
    we also don't have to go beyond the first page of tweets
    """
    logger.info("Getting tweets from shitpostbot5000")
    try:
        tweets_json = urllib.request.urlopen('https://twitter.com/i/profiles/show/shitpostbot5000/timeline/tweets?include_available_features=1&include_entities=1&reset_error_state=false').read()
        tweets_data = json.loads(tweets_json)['items_html']
        tweets_html = BeautifulSoup(tweets_data, 'html.parser')
        tweets_list = tweets_html.find_all("div", attrs={'class','js-adaptive-photo'}) #only get the photos present on the timeline (shitpostbot only posts photos)
        tweet_chosen = tweets_list[random.randint(0, len(tweets_list)-1)] #randomly get tweet
        return tweet_chosen.find("img")['src']
    except:
        logger.info("Bug getting shitpostbot5000 tweet")
        return None

@app.route("/")
def index():
    logger.info('Script Start')

    shitpostbot_img = get_shitpostbot_twitter_post()
    #random coinflip for source
    if random.randint(0,1) == 0 and shitpostbot_img is not None:
        return render_template('shitpostbot.html', img_url=shitpostbot_img)

    #reddit source
    else:
        sfw_porn_list = get_new_list(config.REDDIT_IMAGE_SUBS)
        shower_thought_list = get_new_list(config.REDDIT_TEXT_SUB)

        # img_url = ''
        while True:  # Repeat until we get a valid image in the proper size
            img_post = random.choice(sfw_porn_list)
            img_url = fix_imgur(img_post.url)
            if is_good_image(img_url):
                logger.debug('Image is from: {}'.format(img_post.url))
                # download_image(img_url)
                # want to get the subreddit a submission is from
                break

        witty_text = random.choice(shower_thought_list).title
        # They're supposed to all be in the title

        txt_len = len(witty_text)

        if txt_len > 146:
            middle = int(txt_len / 2)
            split = witty_text[:middle].rfind(' ')
            witty_text = witty_text[:split] + witty_text[split:]

        return render_template('inspiration.html', img_url=img_url, text=witty_text)


if __name__ == '__main__':
    app.run()

application = app
