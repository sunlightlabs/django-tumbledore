import datetime
import glob
import os

from django.conf import settings
from django.db import models
from django.utils.html import escapejs
from jsonfield import JSONField


DEFAULT_POSTS_PER_PAGE = 10

THEME_PATHS = glob.glob(os.path.join(os.path.dirname(__file__),
                                     'templates', 'tumbledore', 'themes', '*'))
for location in settings.TEMPLATE_DIRS:
    THEME_PATHS += glob.glob(os.path.join(location, 'tumbledore', 'themes', '*'))
TUMBL_THEME_CHOICES = [(path, path.split('/')[-1]) for path in THEME_PATHS]

SORT_BY_CHOICES = (
    ('D', 'Date',),
    ('O', 'Order',),
)


class Tumblelog(models.Model):
    name = models.CharField(max_length=200,
                            help_text='This will display in the header area of your tumblelog.')
    description = models.TextField(blank=True, default='',
                                   help_text='This will display below the name.')
    mount_on = models.CharField(max_length=200, blank=True, default='',
                                unique=True, db_index=True,
                                help_text="The root url of your tumblelog.")
    theme = models.CharField(max_length=255, choices=TUMBL_THEME_CHOICES)
    posts_per_page = models.IntegerField(default=DEFAULT_POSTS_PER_PAGE)
    sort_posts_by = models.CharField(max_length=1, choices=SORT_BY_CHOICES, default='D')
    widgets = models.ManyToManyField('TumblelogWidget', through='TumblelogWidgetPlacement')
    extra_styles = models.TextField(blank=True, default='',
                                    help_text='Inserted before the close of the head tag.')
    extra_scripts = models.TextField(blank=True, default='',
                                     help_text='Inserted before the close of the body tag.')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __unicode__(self):
        return unicode(self.name)

    def save(self, **kwargs):
        self.mount_on = self.mount_on.strip('/')

        super(Tumblelog, self).save(**kwargs)


class TumblelogPostManager(models.Manager):
    def published(qset):
        return qset.filter(is_published=True)

    def drafts(qset):
        return qset.filter(is_published=False)


class TumblelogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, db_index=True)
    tumblelog = models.ForeignKey(Tumblelog, related_name='posts',
                                  verbose_name='Post in')
    author = models.CharField(max_length=200, blank=True, default='',
                              help_text='HTML is allowed.')
    content = models.TextField(blank=True, default='')
    excerpt = models.TextField(blank=True, default='',
                               help_text='Only needed if this post has a permalink.')
    sort_order = models.IntegerField(blank=True, default=0,
                                     help_text='Set this if your tumblelog is using custom ordering.')
    custom_data = JSONField(default="{}", blank=True,
                                   help_text='As JSON; will override context variables, e.g., permalink')
    is_published = models.BooleanField(default=False)
    is_sticky = models.BooleanField(default=False)
    has_permalink = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    published_at = models.DateTimeField(blank=True, null=True, db_index=True)

    objects = TumblelogPostManager()

    class Meta:
        ordering = ('-is_sticky', '-published_at')
        unique_together = ('slug', 'tumblelog')

    def __unicode__(self):
        return unicode("%s, by %s" % (self.title, self.author))

    def save(self, **kwargs):
        if self.is_published and self.published_at is None:
            self.published_at = datetime.datetime.now()

        super(TumblelogPost, self).save(**kwargs)


class TumblelogWidget(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    description = models.TextField(blank=True, default='')
    content = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __unicode__(self):
        return unicode(self.name)

    @property
    def as_javascript(self):
        return ('document.write("%s");' % escapejs(self.content))


class TumblelogWidgetPlacement(models.Model):
    tumblelog = models.ForeignKey(Tumblelog, related_name='placement_set')
    widget = models.ForeignKey(TumblelogWidget, related_name='placement_set')
    order = models.IntegerField(default=1)

    class Meta:
        ordering = ('order',)

    def __unicode__(self):
        return unicode('%s on %s' % (self.widget.name, self.tumblelog.name))

    def save(self, **kwargs):
        # increment pre-existing widget with this order, if it exists
        try:
            conflict = TumblelogWidgetPlacement.objects.get(tumblelog=self.tumblelog, order=self.order)
            conflict.order += 1
            conflict.save()
        except TumblelogWidgetPlacement.DoesNotExist:
            pass
        super(TumblelogWidgetPlacement, self).save(**kwargs)
