import praw
import requests
import configparser
from time import sleep

from os import remove, path
from instagrapi import Client

from modules.media_type import *
from modules.sanitize_media import gif_to_mp4, convert_img_to_jpg

posts_list = []

ig_profile = Client()

HASHTAGS = "#meme #meme #explorepage #dankmemes #funnymemes #memesdaily #humor #comedy #dank #lmao #gamer #laugh #memelord #memez #memesrlife #memegod #memeaccount"

def is_reddit_post_duplicate(id):
    return id in posts_list

def upload_reddit_post_to_ig(title, id, image_url):
    media_type = which_media_type(image_url)

    if media_type == MediaType.INVALID:
        return False

    response = requests.get(image_url).content

    file_extension = image_url[image_url.rfind("."):]

    image_path = f'Images/{id}{file_extension}'

    file = open(image_path, "wb")
    file.write(response)
    file.close()

    caption = f'{title}\nhttps://redd.it/{id}\n.\n.\n.\n.\n.\nHASHTAGS:\n{HASHTAGS}'

    match media_type:
        case MediaType.IMAGE:
            if file_extension != ".jpg":
                image_path = convert_img_to_jpg(image_path)
            ig_profile.photo_upload(image_path, caption)
        case MediaType.GIF:
            image_path = gif_to_mp4(image_path)
            ig_profile.video_upload(image_path, caption)
        case MediaType.VIDEO:
            ig_profile.video_upload(image_path, caption)
    
    remove(image_path)

    return True


if __name__ == '__main__':
    # This is where we store config data. Login credentials, subreddits, etc...
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Logging into our Instagram Account.
    ig_profile.login(config["instagram"]["username"], config["instagram"]["password"])

    # Setting up an instance of our Reddit Application
    reddit = praw.Reddit(
        client_id = config["reddit"]["client_id"], 
        client_secret = config["reddit"]["client_secret"],
        user_agent = "MemeParserBot/0.1 by Zabaniya001"
    )

    # If the folder doesn't already exist, we create it.
    if not path.exists("Images"):
        os.mkdir("Images")

    # Some code to retrieve the posts' IDs from a file and then shoving them into a list
    # So we can later on check if we've already posted the meme from the specific post.
    posts_list_file = open("Images/posts.txt", "a+")
    buffer_position = posts_list_file.tell()
    posts_list_file.seek(0)
    posts_list = posts_list_file.read().split(",")
    posts_list_file.seek(buffer_position)

    subreddits = ["memes", "dankmemes", "videomemes", "wholesomememes", "Memes_Of_The_Dank", "darksoulsmemes", "surrealmemes", "dankvideos", "okbuddyretard"]

    while True:
        for item in subreddits:
            index_loop = 0

            for submission in reddit.subreddit(item).hot():
                if index_loop == 5:
                    break

                # The loop iterates through all of the posts, including pinned posts 
                # ( which are most of the time useless garbage meant for moderation or stuff like that)
                if submission.stickied:
                    continue
                
                # If it's over 18, there is a high chance it's not allowed on Instagram.
                if submission.over_18:
                    continue
                
                if is_reddit_post_duplicate(submission.id):
                    continue

                print("Post made by:" + submission.author.name + " | " + submission.title + ": " + submission.url)
                
                # Saving the ID so we know in the future we've posted this post's meme.
                posts_list.append(submission.id)
                posts_list_file.write(submission.id + ",")
                posts_list_file.flush()

                return_value = upload_reddit_post_to_ig(submission.title, submission.id, submission.url)

                if not return_value:
                    continue
                
                index_loop += 1

                # We make it wait X time before making a new post.
                sleep(10)
            sleep(1800) # 30 minutes