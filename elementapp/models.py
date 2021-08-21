from django.db import models

# Create your models here.
class information(models.Model):
    title = models.CharField(max_length=300, default='Default Title') # have put this limit after observing the data from spreadsheet
    description =  models.TextField(default='Default Description')
    image = models.URLField(max_length=500,default='http://www.google.com') # by default picture will be saved into images folder in root folder

    def __str__(self) -> str:
        return self.title