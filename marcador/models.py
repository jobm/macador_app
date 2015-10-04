from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
# Create your models here.
#this is the tag model that contains the mapping to the table Tag in the database
@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=200,unique=True)
    #this is metadata for the tag and how it is stored
    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"
        ordering = ["name"]
    #what the column dislay name will be eg value stored in name, thus the name of the tag
    def __str__(self):
        return self.name
#code that manages the Bookmark table by querying all public bookmarks
class PublicBookmarkManager(models.Manager):
    def get_queryset(self):
        qs = super(PublicBookmarkManager, self).get_queryset()
        return qs.filter(is_public=True)
#this is the bookmark model containing the mapping date to the table Bookmark in the database
@python_2_unicode_compatible
class Bookmark(models.Model):
    url = models.URLField()
    title = models.CharField('title', max_length = 255)
    description = models.TextField('description', max_length = 255)
    is_public = models.BooleanField('public',default = True)
    date_created = models.DateField('date created')
    date_updated= models.DateField('date updated')
    owner = models.ForeignKey(User, verbose_name = 'owner',
        related_name = 'bookmarks')
    tags = models.ManyToManyField(Tag, blank = True)

    #adding the models manager class that converts python queries into sql and commands
    manager = models.Manager()
    #instantiating bookmark query manager
    public = PublicBookmarkManager()

    #this is metadata for the tag and how it is stored
    class Meta:
        verbose_name = "bookmark"
        verbose_name_plural = "bookmarks"
        ordering = ["date_created"]
    #what the column dislay name will be eg value stored in title and concat it with the url,
    #thus the name of the bookmark and url of the bookmark
    def __str__(self):
        return '%s (%s)' % (self.title, self.url)
    #save the url a fresh if one doesnt exist else call save from bookmark
    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = now()
        self.date_updated = now()
        super(Bookmark, self).save(*args, **kwargs)
