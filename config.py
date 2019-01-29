from os import environ as env

APP_NAME = env.get("EPST_APP_NAME", "inspirationalshitpost")

IMAGE_LOGIC = env.get("EPST_IMAGE_LOGIC", "and")
IMAGE_MIN_WIDTH = int(env.get("EPST_IMAGE_MIN_WIDTH", "1920"))
IMAGE_MIN_HEIGHT = int(env.get("EPST_IMAGE_MIN_HEIGHT", "1080"))

REDDIT_CLIENT_ID = env.get("EPST_REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = env.get("EPST_REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = env.get("EPST_REDDIT_USER_AGENT", "inspirationalshitposts by /u/xx.zjackson")
REDDIT_IMAGE_SUBS = [sub.strip() for sub in
                     env.get("EPST_REDDIT_IMAGE_SUBS", "earthporn,skyporn,lakeporn,ruralporn,spaceporn").split(",")]
REDDIT_TEXT_SUB = [sub.strip() for sub in env.get("EPST_REDDIT_IMAGE_SUBS", "showerthoughts").split(",")]
REDDIT_NUM_POSTS = int(env.get("EPST_REDDIT_NUM_POSTS", "1000"))

# Valid values are 'debug', 'info', 'warn', 'error', or 'critical'
LOG_LEVEL = env.get("EPST_LOG_LEVEL", "info").lower()
