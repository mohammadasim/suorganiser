from django.db import models
from django.urls import reverse


class Tag(models.Model):
    name = models.CharField(max_length=31,
                            unique=True)
    slug = models.SlugField(unique=True,
                            max_length=31,
                            help_text='A label for URL Config')

    def __str__(self):
        # to capitalise the first Character
        return self.name.title()

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('organizers_tag_detail', kwargs={'slug': self.slug})


class Startup(models.Model):
    name = models.CharField(max_length=31,
                            db_index=True)
    slug = models.SlugField(max_length=31,
                            unique=True,
                            help_text='A label for URL Config')
    description = models.TextField()
    founded_date = models.DateField('Date Founded')
    contact = models.EmailField()
    website = models.URLField(max_length=255)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name.title()

    class Meta:
        ordering = ['name']
        get_latest_by = 'founded_date'

    def get_absolute_url(self):
        return reverse('organizers_startup_detail', kwargs={'slug': self.slug})


class NewsLink(models.Model):
    title = models.CharField(max_length=63)
    pub_date = models.DateField('Date Published')
    link = models.URLField(max_length=255)
    startup = models.ForeignKey(Startup,
                                on_delete=models.CASCADE)

    def __str__(self):
        return '{}:{}'.format(
            self.startup,
            self.title
        )

    class Meta:
        verbose_name = 'news article'
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'

    def get_absolute_url(self):
        return reverse('organizers_startup_detail', kwargs={
            'slug': self.slug
        })
