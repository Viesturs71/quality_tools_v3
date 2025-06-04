"""
Standard report template.
This template uses common settings from the includes directory.
"""

from .includes.document_settings import get_default_settings


class ReportTemplate:
    def __init__(self, title, author, custom_settings=None):
        self.title = title
        self.author = author
        self.settings = get_default_settings()

        # Override default settings with custom settings if provided
        if custom_settings:
            for key, value in custom_settings.items():
                if key in self.settings:
                    self.settings[key] = value

    def generate(self, content):
        """Generate a report based on this template and the provided content"""
        report = {
            'title': self.title,
            'author': self.author,
            'settings': self.settings,
            'content': content
        }
        return report
