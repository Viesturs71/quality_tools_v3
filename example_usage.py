"""
Example usage of the templates system.
"""

from templates import LetterTemplate, ReportTemplate


def main():
    # Create a report using the default settings
    report = ReportTemplate(
        title="Quarterly Analysis",
        author="John Doe"
    )
    report_content = [
        {"section": "Introduction", "text": "This report covers the Q3 performance."},
        {"section": "Results", "text": "The results show a 15% improvement over Q2."}
    ]
    report.generate(report_content)

    # Create a letter
    letter = LetterTemplate(
        sender="Company Inc., 123 Business St.",
        recipient="John Smith, 456 Client Ave.",
        subject="Partnership Proposal"
    )
    letter_body = "Dear Mr. Smith,\n\nWe would like to propose a partnership...\n\nSincerely,\nCEO"
    letter.generate(letter_body)

if __name__ == "__main__":
    main()
