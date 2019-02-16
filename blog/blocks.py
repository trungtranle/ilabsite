from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.core.blocks import (
    CharBlock, ChoiceBlock, RichTextBlock, StreamBlock, StructBlock, TextBlock,
)


class ImageBlock(StructBlock):
    
    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    

    class Meta:
        icon = 'image'
        template = "blog/image_block.html"


class HeadingBlock(StructBlock):
    
    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(choices=[
        ('', 'Select a header size'),
        ('h1', 'H1'),
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4'),
        ('h5', 'H5'),
        ('h6', 'H6'),
    ], blank=True, required=False)

    class Meta:
        icon = "title"
        


class BlockQuote(StructBlock):
    
    text = TextBlock()
    author = CharBlock(
        blank=True, required=False, label='Author')
    
    class Meta:
        template = 'blog/blockquote_block.html'


# StreamBlocks
class BaseStreamBlock(StreamBlock):
    
    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock()
    image_block = ImageBlock()
    block_quote = BlockQuote()
    embed_block = EmbedBlock(
        help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks',
        
        template="blocks/embed_block.html")