from django.db import models
from django.db.models import F, Count, Value
from django.shortcuts import render
from django.forms import widgets
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.core import blocks
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel, FieldRowPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from taggit.models import TaggedItemBase, Tag as TaggitTag
from modelcluster.tags import ClusterTaggableManager
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from blog.blocks import BaseStreamBlock
from modelcluster.models import ClusterableModel
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
    
class BlogPeopleRelationship(Orderable, models.Model):
   
    page = ParentalKey(
        'BlogPage', related_name='blog_person_relationship', on_delete=models.CASCADE
    )
    people = models.ForeignKey(
        'blog.People', related_name='person_blog_relationship', on_delete=models.CASCADE
    )
    panels = [
        SnippetChooserPanel('people')
    ] 


@register_snippet
class People(index.Indexed, ClusterableModel):
    
    name = models.CharField("Name", max_length=254)
    
    job_title = models.CharField("Job title", max_length=254, blank = True)

    image = models.ForeignKey(
        'blog.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('name'),
                
            ])
        ], "Name"),
        FieldPanel('job_title'),
        ImageChooserPanel('image'),
    ]

    search_fields = [
        index.SearchField('name'),
        
    ]

    @property
    def thumb_image(self):
        # Returns an empty string if there is no profile pic or the rendition
        # file can't be found.
        try:
            return self.image
        except:
            return ''

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'

   
class BlogPage(Page):
    #author = models.CharField(max_length=255)
    date = models.DateField("Post date")
    intro = RichTextField(blank = True)
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
        'blog.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text = 'Hình theo chiều ngang, kích thước > 1000 px'
    )

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('date')
    ]

    content_panels = Page.content_panels + [
        InlinePanel(
            'blog_person_relationship', label="Author(s)",
            panels=None, min_num=1),
        ImageChooserPanel('feed_image'),
        FieldPanel('intro'),
        #FieldPanel('author'),
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
    
    def authors(self):
        """
        Returns the BlogPage's related People. Again note that we are using
        the ParentalKey's related_name from the BlogPeopleRelationship model
        to access these objects. This allows us to access the People objects
        with a loop on the template. If we tried to access the blog_person_
        relationship directly we'd print `blog.BlogPeopleRelationship.None`
        """
        authors = [
            n.people for n in self.blog_person_relationship.all()
        ]

        return authors


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