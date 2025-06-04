"""
Common document settings for templates.
These settings will be shared across different document templates.
"""

DEFAULT_MARGINS = {
    'top': 2.5,
    'bottom': 2.5,
    'left': 3.0,
    'right': 2.0
}

DEFAULT_FONT = {
    'family': 'Times New Roman',
    'size': 12
}

DEFAULT_HEADING_STYLES = {
    'h1': {'size': 16, 'bold': True},
    'h2': {'size': 14, 'bold': True},
    'h3': {'size': 12, 'bold': True}
}

PAGE_SIZE = 'A4'

def get_default_settings():
    """Returns all default document settings as a dictionary"""
    return {
        'margins': DEFAULT_MARGINS,
        'font': DEFAULT_FONT,
        'heading_styles': DEFAULT_HEADING_STYLES,
        'page_size': PAGE_SIZE
    }
