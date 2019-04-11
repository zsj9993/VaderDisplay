# VaderDisplay
This set of files allows for "inspirational shitposts" to be randomly generated via a virtual container on OpenShift, which is pushed to a Raspberry Pi and displayed on a TV. I created a Python script that pulls images from r/earthporn and other landscape image subreddits and pairs them with posts from r/showerthoughts. The Python script parses the Reddit API for both of these things, and then creates a temporary image. The link to the image is then displayed fullscreen on the Pi, with the image refreshing automatically every 5 minutes.

## Installation and Use
The program runs remotely on OpenShift. In order to install and make changes to the files, clone the repo locally and edit wsgi.py and config.py as needed, then push back up to the GitHub. OpenShift will then automatically rebuild the container and display the image on the Pi. The project is listed as "inspirationalshitposts" on OpenShift, and I'm too lazy to rename that, so that's how it is.

## Future Plans
~~1. Integrate with OpenShift to allow for other people to work on it and improve it.~~

~~2. Set up configuration in which the actual program runs on a server and then the Pi just displays the output.~~

3. Use Javascript to queue up images and pull the next one from the queue (removes most of the delay with rendering images and displaying them at the same time).

## What I Learned
- How to use a Raspberry Pi and start it up from scratch
- How to write a program in Python 2 and migrate it to Python 3
- How to make and use a template and config file
- How to host my project on OpenShift and display it remotely on a Pi
- How to troubleshoot a program
- How to parse an API
- HOW TO ASK FOR HELP
