from datetime import date
from django.db import models
from django.urls import reverse
from django.conf import settings

from organizers.models import Tag, Startup


class PostQueryset(models.QuerySet):
    """
    A custom queryset class with a
    published method.

    The reason we had to define a custom
    queryset class for post and not other
    models was because we have a method
    published. Other models don't have
    a custom method, like this.
    """

    def published(self):
        """
        A method to find all the post objects
        with pub_date from before today
        :return:
        """
        return self.filter(
            pub_date__lte=date.today()
        )


class BasePostManager(models.Manager):
    """
    Custom manager class for Post.
    """

    def get_by_natural_key(self, pub_date, slug):
        """
        Method to be used when loading data to
        database from fixtures.
        :param pub_date:
        :param slug:
        :return:
        """
        return self.get(
            pub_date=pub_date,
            slug=slug
        )


# The PostQueryset object needs to be
# linked to BasePostManager object.
# We could define get_queryset method
# in BasePostManager class or use the
# following easy approach.
PostManager = BasePostManager.from_queryset(
    PostQueryset
)


class Post(models.Model):
    title = models.CharField(max_length=63)
    slug = models.SlugField(
        max_length=63,
        help_text='A label for URL config',
        unique_for_month='pub_date'
    )
    text = models.TextField()
    pub_date = models.DateField(
        'Date Published',
        auto_now_add=True
    )
    tags = models.ManyToManyField(Tag,
                                  related_name='blog_posts',
                                  blank=True)
    startups = models.ManyToManyField(Startup,
                                      related_name='blog_posts',
                                      blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='blog_posts',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return 'Post {} published on {}'.format(
            self.title,
            self.pub_date.strftime('%Y-%m-%d')
        )

    def natural_key(self):
        """
        A method to return natural key tuple
        uniquely identifying the post object
        We also define dependencies that post
        has on tag and startup so they are
        serialized first.
        This method must return a tuple
        :return:
        """
        return (
            self.pub_date,
            self.slug
        )
    natural_key.dependencies = [
            'organizers.startup',
            'organizers.tag',
            'users.user'
        ]

    # we use the PostManager generated class
    # as manager for Post model.
    objects = PostManager()

    class Meta:
        verbose_name = 'blog post'
        ordering = ['-pub_date', 'title']
        get_latest_by = 'pub_date'
        permissions = (
            ('view_future_post',
             'Can view unpublished Post'),
        )
        # Post objects are unique based on
        # slug and pub-date. While slug and
        # pk are automatically indexed, in
        # order to speed up the db queries
        # and optimise our app, we want both
        # slug and pub-date to be indexed.
        # This will do exactly that. After
        # making this change will need to
        # run the makemigration/migration command.
        # If we need to do further SQL changes
        # django offers the benefit of RUNSQL
        # in migration file, just like we used
        # RUNPYTHON
        index_together = (
            ('slug', 'pub_date'),
        )

    def get_absolute_url(self):
        return reverse('blogs_post_detail',
                       kwargs={
                           'slug': self.slug,
                           'year': self.pub_date.year,
                           'month': self.pub_date.month
                       })

    def get_update_url(self):
        return reverse('blogs_post_update',
                       kwargs={
                           'slug': self.slug,
                           'year': self.pub_date.year,
                           'month': self.pub_date.month
                       })

    def get_delete_url(self):
        return reverse('blogs_post_delete', kwargs={
            'slug': self.slug,
            'year': self.pub_date.year,
            'month': self.pub_date.month
        })

    def get_archive_year_url(self):
        return reverse(
            'blogs_post_archive_year',
            kwargs={'year': self.pub_date.year}
        )

    def get_archive_month_url(self):
        return reverse('blogs_post_archive_month',
                       kwargs={
                           'year': self.pub_date.year,
                           'month': self.pub_date.month
                       }
                       )
