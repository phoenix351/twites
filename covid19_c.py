# Create an Object Called 'customStreamListener' with the Function Below
import tweepy
import csv
import sys

# Fill the API Key
consumer_key = "JPBmvXnfwZs2gXtdjGfKQDffw"
consumer_secret = "e0XM9D1BiItnQgPM5OaoVQ88W8SeZyi0Bn3qFQji041leexsWs"
access_token = "1237633057084952576-TMKq3gKSQOlaqqfDqmI1c6JI6i7x2u"
access_token_secret = "2ZDeuiDNFKuiBIniEafNALL4YnXgok0BZnUK01xzr3MR1"

# Auth.
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
api

import pymysql.cursors
connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='phoenix',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

class twit:
    def __init__(self,time='Kosong',desc='Kosong',Usertweets='Kosong',Source='Kosong',Target='Kosong',Verified='Kosong',Text='Kosong',HashTags='Kosong',Location='Kosong',Following='Kosong',Followers='Kosong',Retweets="Kosong"):

        self.Time=time
        self.Description = desc
        self.Usertweets=Usertweets
        self.Source= Source
        self.Target=Target
        self.Verified=Verified
        self.Text=Text
        self.Hashtags=HashTags
        self.Location=Location
        self.Following=Following
        self.Followers=Followers
        self.Retweets=Retweets

    def insert_db(self):
        with connection.cursor() as cursor:
            sql = "INSERT INTO `corona_twit` (`Time`, `Description`,`Usertweets`,`Source`,`Target`,`Verified`,`Text`,`Hashtag`,`Location`,`Following`,`Followers`,`Retweets`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, (
            self.Time, self.Description, self.Usertweets, self.Source, self.Target, self.Verified, self.Text,
            self.Hashtags, self.Location, self.Following, self.Followers, self.Retweets))
        connection.commit()


class CustomStreamListener(tweepy.StreamListener):

    def on_status(self, status):

        twit1 = twit(status.created_at, status.user.description, status.user.statuses_count,
              status.user.screen_name, status.in_reply_to_screen_name, status.user.verified,
              status.text, str(status.entities['hashtags']), status.user.location,
              status.user.friends_count, status.user.followers_count, status.retweet_count)
        twit1.insert_db()
    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True  # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True  # Don't kill the stream

keyword_list = keyword = ['#JatengLawanCorona,jateng lawan corona,indonesia butuh pemimpin,#IndonesiaButuhPemimpin,nkri corona,corona presiden indonesia,corona gubernur jakarta,corona jawa tengah, corona jawa barat, corona bali, corona kalimantan, corona jawa,bupati corona,kuliah corona,kuliah libur,kuliah daring,kuliah online,sekolah corona,sekolah libur corona,lock down,lockdown']
streamingAPI = tweepy.streaming.Stream(auth, CustomStreamListener())
streamingAPI.filter(track=keyword_list)