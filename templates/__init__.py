"""
Templates package for document generation.
All templates use common settings from the includes subdirectory.
"""

from .letter_template import LetterTemplate
from .report_template import ReportTemplate

__all__ = ['LetterTemplate', 'ReportTemplate']
