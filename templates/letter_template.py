"""
Business letter template.
This template uses common settings from the includes directory.
"""

from .includes.document_settings import get_default_settings


class LetterTemplate:
    def __init__(self, sender, recipient, subject):
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.settings = get_default_settings()

        # Letters typically have different margins
        self.settings['margins'] = {
            'top': 2.0,
            'bottom': 2.0,
            'left': 2.5,
            'right': 2.5
        }

    def generate(self, body_text, include_signature=True):
        """Generate a letter based on this template and the provided content"""
        letter = {
            'sender': self.sender,
            'recipient': self.recipient,
            'subject': self.subject,
            'settings': self.settings,
            'body': body_text,
            'include_signature': include_signature
        }
        return letter
