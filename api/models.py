from django.db import models

# Create your models here.

class Tweet(models.Model):

    Time = models.CharField(max_length=20,primary_key=True)
    Description = models.TextField()
    Usertweets = models.IntegerField()
    Source = models.CharField(max_length=25)
    Target = models.CharField(max_length=25)
    Verified=models.CharField(max_length=6)
    Text = models.TextField()
    HashTag = models.TextField()
    Location = models.CharField(max_length=50)
    Following = models.IntegerField()
    Followers = models.IntegerField()
    Retweets = models.IntegerField()

    class Meta:
        db_table = "corona_twit"
        unique_together = (('Time', 'Usertweets','Text'),)

    def setattr(self, time='Kosong', desc='Kosong', Usertweets='Kosong', Source='Kosong', Target='Kosong',
                 Verified='Kosong', Text='Kosong', HashTags='Kosong', Location='Kosong', Following='Kosong',
                 Followers='Kosong', Retweets="Kosong"):
        self.Time = time
        self.Description = desc
        self.Usertweets = Usertweets
        self.Source = Source
        self.Target = Target
        self.Verified = Verified
        self.Text = Text
        self.Hashtags = HashTags
        self.Location = Location
        self.Following = Following
        self.Followers = Followers
        self.Retweets = Retweets



