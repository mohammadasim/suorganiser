from datetime import date

from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property


class TagManager(models.Manager):
    """
    Custom manager class for Tag model.
    """

    def get_by_natural_key(self, slug):
        """
        Method to use natural key in
        deserialization.
        :param slug:
        :return:
        """
        return self.get(
            slug=slug
        )


class Tag(models.Model):
    name = models.CharField(max_length=31,
                            unique=True)
    slug = models.SlugField(unique=True,
                            max_length=31,
                            help_text='A label for URL Config')

    def __str__(self):
        # to capitalise the first Character
        return self.name.title()

    objects = TagManager()

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('organizers_tag_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('organizers_tag_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('organizers_tag_delete', kwargs={'slug': self.slug})

    @cached_property
    def published_posts(self):
        """
        Method to return a queryset to
        filter for published posts only.
        The method helps with showing future
        articles only for those users with
        having the corresponding permission,
        the template
        The resulting queryset is changed
        into a tuple, as tuple has a smaller
        memory footprint.
        :return:
        """
        return tuple(self.blog_posts.filter(
            pub_date__lt=date.today()
        ))

    def natural_key(self):
        """
        Method to create human friendly
        serialized data
        This method must return a tuple
        :return:
        """
        return (
            self.slug
        )


class StartupManager(models.Model):
    """
    Custom manager class for Startup model
    """

    def get_by_natural_key(self, slug):
        """
        Method to be used in deserialization
        of startup objects
        :param slug:
        :return:
        """
        return self.get(slug=slug)


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
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name.title()

    objects = StartupManager()

    class Meta:
        ordering = ['name']
        get_latest_by = 'founded_date'

    def get_absolute_url(self):
        return reverse('organizers_startup_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('organizers_startup_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('organizers_startup_delete', kwargs={'slug': self.slug})

    def get_newslink_create_url(self):
        return reverse(
            'organizers_newslink_create',
            kwargs={
                'startup_slug': self.slug
            })

    def natural_key(self):
        """
        Method used to create human friendly
        serialized data
        This method must return a tuple, hence
        the parenthesis
        :return:
        """
        return (self.slug)

    @cached_property
    def published_posts(self):
        """
        Method to return a queryset to
        filter for published posts only.
        The method helps with showing future
        articles only for those users with
        having the corresponding permission,
        the template
        The resulting queryset is changed
        into a tuple, as tuple has a smaller
        memory footprint.
        :return:
        """
        return tuple(self.blog_posts.filter(
            pub_date__lt=date.today()
        ))


class NewsLinkManager(models.Model):
    """
    Custom manager class for NewsLink
    """

    def get_by_natural_key(self, startup_slug, slug):
        """
        Method to be used for deserialization of data
        :param startup_slug:
        :param slug:
        :return:
        """
        return self.get(
            startup_slug=self.startup_slug,
            slug=self.slug
        )


class NewsLink(models.Model):
    title = models.CharField(max_length=63)
    pub_date = models.DateField('Date Published')
    link = models.URLField(max_length=255)
    startup = models.ForeignKey(Startup,
                                on_delete=models.CASCADE)
    slug = models.SlugField(max_length=63)

    def __str__(self):
        return '{}:{}'.format(
            self.startup,
            self.title
        )

    objects = NewsLinkManager()

    class Meta:
        verbose_name = 'news article'
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'
        unique_together = ('slug', 'startup')

    def get_absolute_url(self):
        return reverse('organizers_startup_detail', kwargs={
            'slug': self.startup.slug
        })

    def get_update_url(self):
        return reverse('organizers_newslink_update',
                       kwargs={
                           'startup_slug': self.startup.slug,
                           'newslink_slug': self.slug
                       })

    def get_delete_url(self):
        return reverse('organizers_newslink_delete',
                       kwargs={
                           'startup_slug': self.startup.slug,
                           'newslink_slug': self.slug
                       })

    def natural_key(self):
        """
        Method used to serialize
        Newslink object in a human friendly
        way.
        :return:
        """
        return (
            self.startup.natural_key(),
            self.slug
        )

    natural_key.dependencies = [
        'organizers.startup',
        'organizers.tag',
        'users.user'
    ]
