"""
This config describes where to find each element we're interested in and how to extract relevant
text from it. It's used by DocumentParser when converting raw HTML to a parsed document.
"""
PARSER_CONFIG = {

    'img': {
        'name': 'Image Tag',
        'plural_name': 'Image Tags',
        'text_config': False,
    },

    'img[src]': {
        'name': 'Image Path',
        'plural_name': 'Image Paths',
        'text_config': {
            'accessor_type': 'attribute',
            'accessor_attribute_name': 'src',
        },
    },

    'img[data-src]': {
        'name': 'Image Path (Lazyloaded)',
        'plural_name': 'Image Paths (Lazyloaded)',
        'text_config': {
            'accessor_type': 'attribute',
            'accessor_attribute_name': 'data-src',
        },
    },

    'img[alt]': {
        'name': 'Image Alt Text',
        'Plural Name': 'Image Alt Texts',
        'text_config': {
            'accessor_type': 'attribute',
            'accessor_attribute_name': 'alt',
        },
    },

    'p': {
        'name': 'Paragraph Tag',
        'plural_name': 'Paragraphs Tags',
        'text_config':  {
            'accessor_type': 'parent_only',
        }

    },

    'a': {
        'name': 'Anchor Tag',
        'plural_name': 'Anchor Tags',
        'text_config':  {
            'accessor_type': 'default',
        },

    },

    'b, strong': {
        'name': 'Bold',
    },

    'i, em': {
        'name': 'Italic',
    },

    'title': {
        'name': 'Meta Title',
        'in_head': True,
    },

    'meta[name=description]': {
        'name': 'Meta Description',
        'in_head': True,
    },

    'h1': {
        'name': 'H1',
    },

    'h2': {
        'name': 'H2',
    },

    'h3': {
        'name': 'H3',
    },

    'h4': {
        'name': 'H4',
    },

    'h5': {
        'name': 'H5',
    },

    'h6': {
        'name': 'H6',
    },

    'ol': {
        'name': 'Ordered List',
        'name_plural': 'Ordered Lists',
        'text_config': False,
    },

    'ol li': {
        'name': 'Ordered List Item',
        'name_plural': 'Ordered List Items',
    },

    'ul': {
        'name': 'Unordered List',
        'name_plural': 'Unordered Lists',
        'text_config': False,
    },

    'ul li': {
        'name': 'Unordered List Item',
        'name_plural': 'Unordered List Items',
    },

    'table': {
        'name': 'Table',
        'name_plural': 'Tables',
        'text_config': False,
    },

    'table th': {
        'name': 'Table Heading',
        'name_plural': 'Table Headings',
    },

    'table tr': {
        'name': 'Table Row',
        'name_plural': 'Table Rows',
    },

}
