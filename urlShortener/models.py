from django.db import models


class shortURL(models.Model):
  url = models.URLField(unique=False)
  short_code = models.CharField(max_length=10, unique=True)
  click_count = models.IntegerField(default=0)
  author = models.CharField(max_length=150, default="null")

  def __str__(self):
    return f"{self.short_code} -> {self.url}"

