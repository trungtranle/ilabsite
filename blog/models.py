from django.db import models
from django.db.models import F, Count, Value
from django.shortcuts import render
from django.forms import widgets
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.core import blocks
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from taggit.models import TaggedItemBase, Tag as TaggitTag
from modelcluster.tags import ClusterTaggableManager
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from blog.blocks import BaseStreamBlock
# Create your models here.
class HomePage(Page):
    title = RichTextField

    content_panels = Page.content_panels + [
        FieldPanel('title')
    ]

    def serve(self, request):
        # Get blogs
        blogs = BlogPage.objects.child_of(self).live()

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            blogs = blogs.filter(tags__name=tag)

        return render(request, self.template, {
            'page': self,
            'blogs': blogs,
        })
    
    
class BlogPage(Page):
    author = models.CharField(max_length=255)
    date = models.DateField("Post date")
    intro = RichTextField()
    hit_count = models.IntegerField(default= 0)
    '''
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('blockquote', blocks.BlockQuoteBlock()),
    ])
    '''
    body = StreamField(BaseStreamBlock(), verbose_name = 'Page Body')
    tags = ClusterTaggableManager(through='BlogPageTag', blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('date')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        ImageChooserPanel('feed_image'),
        FieldPanel('author'),
        FieldPanel('date'),
        StreamFieldPanel('body'),
        FieldPanel('tags'),
        InlinePanel('related_links', label="Related links"),
        
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        FieldPanel('hit_count', widget = widgets.NumberInput())
        
    ]

    def serve(self, request):
       
        self.hit_count += 1
        self.save()       

        return super().serve(request)
    

class BlogPageRelatedLink(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='related_links')
    name = models.CharField(max_length=255, blank = True)
    url = models.URLField(blank = True)

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]

@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='post_tags')

@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True

    
    
class CustomImage(AbstractImage):
    # Add any extra fields to image here

    # eg. To add a caption field:
    caption = models.CharField(max_length=255, blank=True)

    admin_form_fields = Image.admin_form_fields + (
        # Then add the field names here to make them appear in the form:
        'caption',
    )


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(CustomImage, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )