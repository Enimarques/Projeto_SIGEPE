from django.db import models

class Category(models.Model):
  title=models.CharField(max_length=180)
  image=models.ImageField(upload_to="cat_imgs/")
  
  def __str__(self):
    return self.title
