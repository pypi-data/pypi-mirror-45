# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cms.models.fields import PlaceholderField
from cms.utils.i18n import get_current_language
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _
from filer.fields.image import FilerImageField
from mptt.models import MPTTModel, TreeForeignKey
from parler.managers import TranslatableManager
from parler.models import TranslatableModel, TranslatedFields
from parler.utils.context import switch_language

from blogit import settings as bs
from blogit.managers import PostManager
from blogit.utils import get_text_from_placeholder

try:
    from django.utils.encoding import force_unicode
except ImportError:
    from django.utils.encoding import force_text as force_unicode


USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


@python_2_unicode_compatible
class Category(MPTTModel, TranslatableModel):
    """
    Category
    """
    active = models.BooleanField(_('Active'), default=True, help_text=bs.ACTIVE_FIELD_HELP_TEXT)
    date_added = models.DateTimeField(_('Date added'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

    parent = TreeForeignKey(
        'self',
        models.SET_NULL,
        blank=True,
        null=True,
        related_name='children',
        verbose_name=_('Parent'),
    )

    translations = TranslatedFields(
        name=models.CharField(_('Name'), max_length=255),
        slug=models.SlugField(_('Slug'), db_index=True),
        description=models.TextField(_('description'), blank=True),
        meta={'unique_together': [('slug', 'language_code')]},
    )

    objects = TranslatableManager()

    class Meta:
        db_table = 'blogit_categories'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)

    def get_absolute_url(self, language=None):
        if not language:
            language = get_current_language()

        with switch_language(self, language):
            return reverse('blogit_category_detail', args=[self.get_path()])

    def get_path(self):
        """
        Returns ful url path for category.
        """
        path = []
        for obj in self.get_ancestors(include_self=True):
            path.append(obj.safe_translation_getter('slug', ''))
        return '/'.join(path)


@python_2_unicode_compatible
class Tag(TranslatableModel):
    """
    Tag
    """
    active = models.BooleanField(_('Active'), default=True, help_text=bs.ACTIVE_FIELD_HELP_TEXT)
    date_added = models.DateTimeField(_('Date added'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

    translations = TranslatedFields(
        name=models.CharField(_('Name'), max_length=255),
        slug=models.SlugField(_('Slug'), db_index=True),
        description=models.TextField(_('description'), blank=True),
        meta={'unique_together': [('slug', 'language_code')]},
    )

    objects = TranslatableManager()

    class Meta:
        db_table = 'blogit_tags'
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)

    def get_absolute_url(self, language=None):
        if not language:
            language = get_current_language()

        with switch_language(self, language):
            return reverse('blogit_tag_detail', kwargs={'slug': self.safe_translation_getter('slug')})


@python_2_unicode_compatible
class Post(TranslatableModel):
    """
    Post
    """
    DRAFT = 0  # Post is visible to staff
    PRIVATE = 1  # Post is visible to author only
    PUBLIC = 2  # Post is public
    HIDDEN = 3  # Post is hidden from everybody

    STATUS_CODES = (
        (DRAFT, _('Draft')),
        (PRIVATE, _('Private')),
        (PUBLIC, _('Public')),
        (HIDDEN, _('Hidden')),
    )

    date_added = models.DateTimeField(_('Date added'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last modified'), auto_now=True)

    status = models.IntegerField(_('Status'), choices=STATUS_CODES, default=DRAFT, help_text=_(
        'When draft post is visible to staff only, when private to author only, and when public to everyone.'))

    date_published = models.DateTimeField(_('Published on'), default=timezone.now)
    category = TreeForeignKey(Category, models.SET_NULL, blank=True, null=True, verbose_name=_('Category'))
    tags = models.ManyToManyField(Tag, blank=True, related_name='tagged_posts', verbose_name=_('Tags'))
    author = models.ForeignKey(USER_MODEL, models.SET_NULL, blank=True, null=True, verbose_name=_('Author'))

    featured_image = FilerImageField(
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_('Featured Image'),
    )

    translations = TranslatedFields(
        title=models.CharField(_('Title'), max_length=255),
        slug=models.SlugField(_('Slug'), db_index=True),
        description=models.TextField(_('Description'), blank=True),
        meta_title=models.CharField(_('Meta title'), max_length=255, blank=True),
        meta_description=models.TextField(_('Meta description'), max_length=155, blank=True, help_text=_(
            'The text displayed in search engines.')),
        meta={'unique_together': [('slug', 'language_code')]},
    )

    body = PlaceholderField('blogit_post_body', related_name='post_body_set')

    objects = PostManager()

    class Meta:
        db_table = 'blogit_posts'
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ('-date_published', )
        get_latest_by = 'date_published'

    def __str__(self):
        return self.name

    def get_absolute_url(self, language=None):
        if not language:
            language = get_current_language()

        with switch_language(self, language):
            if bs.POST_DETAIL_DATE_URL:
                return reverse('blogit_post_detail_date', kwargs={
                    'year': self.date_published.year,
                    'month': self.date_published.month,
                    'day': self.date_published.day,
                    'slug': self.safe_translation_getter('slug'),
                })

            return reverse('blogit_post_detail', kwargs={
                'slug': self.safe_translation_getter('slug')})

    def get_search_data(self, language=None, request=None):
        """
        Returns search text data for current object
        """
        if not self.pk:
            return ''

        bits = [self.name]
        description = self.safe_translation_getter('description')
        if description:
            bits.append(force_unicode(strip_tags(description)))

        if self.category:
            bits.append(self.category.safe_translation_getter('name'))
            description = self.category.safe_translation_getter('description')
            if description:
                bits.append(force_unicode(strip_tags(description)))

        for tag in self.tags.all():
            bits.append(tag.safe_translation_getter('name'))
            description = tag.safe_translation_getter('description', '')
            if description:
                bits.append(force_unicode(strip_tags(description)))

        bits.append(get_text_from_placeholder(self.body, language, request))
        return ' '.join(bits).strip()

    def get_meta_title(self):
        return self.safe_translation_getter('meta_title') or self.name

    def get_meta_description(self):
        return self.safe_translation_getter('meta_description') or self.safe_translation_getter('description')

    @property
    def name(self):
        return self.safe_translation_getter('title', any_language=True)

    @property
    def is_published(self):
        return self.status == self.PUBLIC and self.date_published <= timezone.now()

    @property
    def previous_post(self):
        return self.previous_next_posts[0]

    @property
    def next_post(self):
        return self.previous_next_posts[1]

    @property
    def previous_next_posts(self):
        previous_next = getattr(self, 'previous_next', None)

        if previous_next is None:
            if not self.is_published:
                previous_next = (None, None)
                setattr(self, 'previous_next', previous_next)
                return previous_next

            posts = list(Post.objects.public().published())
            index = posts.index(self)

            try:
                previous = posts[index + 1]
            except IndexError:
                previous = None

            if index:
                next = posts[index - 1]
            else:
                next = None
            previous_next = (previous, next)
            setattr(self, 'previous_next', previous_next)
        return previous_next
