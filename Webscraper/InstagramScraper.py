import json
import requests
from bs4 import BeautifulSoup
import datetime as dt
import emoji
import ctypes
import time
#ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 6 )

class InstagramScraper:
    #gets page html
    def get_html(self, url):
        try:
            response = requests.get(url, timeout = 5)
        except:
            time.sleep(1)
            return self.get_html(url)

        return response.text

    def extract_json_data(self, html):
        soup = BeautifulSoup(html, "html.parser")
        #saves everything in <body> to body var
        body = soup.find("body")

        #saves everything in <script> within <body> to script_tag var
        script_tag = body.find("script")

        #removes whitespace from beginning and end of script text
        raw_string = script_tag.text.strip()

        #deletes any text that says "window._sharedData =" in the script text
        raw_string = raw_string.replace("window._sharedData =", "")

        #deletes any semicolons in script text
        raw_string = raw_string.replace(";", "")

        return json.loads(raw_string)

    def get_profile_full_name(self, profile_username):
        #gets page html for profile
        profile_html = self.get_html("https://instagram.com/" + profile_username)

        #gets json data for profile
        json_data = self.extract_json_data(profile_html)

        #saves profile metrics to metrics var
        metrics = json_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]

        #if key is full_name return the value (which is the profile owners full name)
        for key, value in metrics.items():
            if(key == "full_name"):
                return value

    def get_profile_recent_posts(self, profile_username):
        #gets page html for profile
        profile_html = self.get_html("https://instagram.com/" + profile_username)

        #gets json data for profile
        json_data = self.extract_json_data(profile_html)

        #saves profile metrics to metrics var
        return json_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]['edge_owner_to_timeline_media']["edges"]

    def get_profile_captions(self, profile_username):
        metrics = self.get_profile_recent_posts(profile_username)

        captions = []

        #gets caption for each post
        for post in metrics:
            post = post.get("node")

            #gets container the caption is in and converts to string
            caption_container = post.get("edge_media_to_caption").get("edges")

            #protects against user not having caption on a post
            try:
                caption_container = str(caption_container[0])
            except:
                captions.append("")
                continue

            #substrings caption container to just be the caption
            caption = caption_container[caption_container.index(":") + 1 :]
            caption = caption[caption.index(":") + 1 :]
            caption = caption[caption.index("\'") + 1 : caption.index("}") - 1]
            caption = emoji.demojize(caption)
            #adds caption to array of captions
            captions.append(caption)

        return captions

    def get_profile_picture_urls(self, profile_username):
        metrics = self.get_profile_recent_posts(profile_username)

        picture_urls = []

        #gets caption for each post
        for post in metrics:
            post = post.get("node")

            #gets container the image url is in and converts to string
            current_pic_url = post.get("display_url")
            picture_urls.append(current_pic_url)
        return picture_urls

    def get_profile_picture_dates(self, profile_username):
        metrics = self.get_profile_recent_posts(profile_username)

        picture_dates = []

        #gets caption for each post
        for post in metrics:
            post = post.get("node")
            current_time_stamp = post.get("taken_at_timestamp")
            picture_dates.append(dt.datetime.fromtimestamp(current_time_stamp).strftime('%m/%d/%Y'))
        return picture_dates

    def scrape(self, usernamesFileUrl):
        output = [[], []]

        #opens file of usernames
        usernames_file = open(usernamesFileUrl)
        usernames_text_array = usernames_file.read().splitlines()

        #fills output array with urls and captions
        for username in usernames_text_array:
            current_account_images_array = []
            current_account_captions_array = []

            #makes current username element 0 in both arrays
            current_account_images_array.append(username)
            current_account_captions_array.append(username)

            #makes date/url array for account to append to output array
            urls_array = self.get_profile_picture_urls(username)
            dates_array = self.get_profile_picture_dates(username)

            for i in range(len(urls_array)):
                current_account_images_array.append(dates_array[i])
                current_account_images_array.append(urls_array[i])

            #makes captions array for account to append to output array
            for caption in self.get_profile_captions(username):
                current_account_captions_array.append(caption)

                '''
                try:
                    current_account_captions_array.append(caption)
                except:
                    for n in range (0, len(caption)):
                        try:
                            captions_file.write(caption[n])
                        except:
                            captions_file.write("")
                    captions_file.write("\n")
                '''

            output[0].append(current_account_images_array)
            output[1].append(current_account_captions_array)

        usernames_file.close()
        return output
