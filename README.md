# inspirationalshitpost
This set of files allows for "inspirational shitposts" to be randomly generated via a Raspberry Pi and displayed on a TV. I created a Python script that pulls images from r/earthporn and other landscape image subreddits and pairs them with posts from r/showerthoughts. The Python script parses the Reddit API for both of these things, and then creates a temporary image. The link to the image is then displayed in a fullscreen Chromium window, with the image refreshing automatically every 30-40 seconds.

## Installation and Use
Clone the repo to a local repository, then run ep_st.py via the terminal. While leaving the terminal running in the background, navigate to and open the ep_st.html file and put into fullscreen mode. The script will run in the background with the current image displaying on screen.

## Future Plans
~~1. Integrate with OpenShift to allow for other people to work on it and improve it.~~
~~2. Set up configuration in which the actual program runs on a server and then the Pi just displays the output.~~
3. Use Javascript to queue up images and pull the next one from the queue (removes most of the delay with rendering images and displaying them at the same time).
