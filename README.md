# Reddit Instagram Poster

**This script fetches Reddit posts to automatically post to an Instagram account. It takes into account whether or not the post in question has been posted to IG. 
Images, GIFs and MP4s are supported.**

A use case could be meme accounts. Rather than having to fetch memes yourself, you can let this script find and post them for you.

## Note
This is my first serious Python script and I have barely any prior Python knowledge, so it's bound to have some edge cases or unoptimizations.
Feel free to let me know if I could have done something differently or stuff like that.

## Future Plans
- Move the hashtags and subreddits from being hardcoded to a config file.
- Move the time between posts from being hardcoded to a config file.
- Give the possibility to make albums rather than making one post per item.
- Compare images so we don't accidentally repost.

## Dependencies
- [Praw](https://praw.readthedocs.io/en/stable/index.html) - Reddit API
- [Instagrapi](https://pypi.org/project/instagrapi/) - Instagram API
- [Pillow](https://pypi.org/project/Pillow/) - Library to mess with images ( Convert image formats to JPG, since IG supports only that )
- [MoviePy](https://pypi.org/project/moviepy/) - Library to mess with videos ( GIF to MP4 )
