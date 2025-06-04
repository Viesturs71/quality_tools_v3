# quality_docs/management/commands/init_sections.py

import sys

from django.core.management.base import BaseCommand
from django.db import transaction

from quality_docs.models import DocumentSection, DocumentSubsection

SECTIONS = [
    {"code": "LD-01", "title": "Normatīvās atsauces"},
    {"code": "LD-02", "title": "Termini un definīcijas"},
    {"code": "LD-03", "title": "Vispārīgās prasības"},
    {"code": "LD-04", "title": "Strukturālās un pārvaldības prasības"},
    {"code": "LD-05", "title": "Resursu prasības"},
    {"code": "LD-06", "title": "Procesa prasības"},
    {"code": "LD-07", "title": "Pārvaldības sistēmas prasības"},
    {"code": "LD-08", "title": "Papildu prasības attiecībā uz testēšanu"},
    {"code": "LD-09", "title": "Rīcību plāni neparedzētām situācijām"},
]

SUBSECTIONS = {
    "LD-04": [
        {"code": "LD-04.01", "title": "Juridiskais statuss, organizācija"},
        {"code": "LD-04.02", "title": "Mērķi un politika"},
    ],
    "LD-05": [
        {"code": "LD-05.01", "title": "Personāls"},
        {"code": "LD-05.02", "title": "Telpas un vides apstākļi"},
    ],
}


class Command(BaseCommand):
    help = "Initialize sections independently without requiring documents"

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simulate the operation without making changes to the database',
        )

    def init_section(self, section, dry_run=False):
        """Initialize a single section and its subsections"""
        try:
            if dry_run:
                self.stdout.write(f"Would create section: {section['code']} - {section['title']}")
                return None, True

            section_obj, created = DocumentSection.objects.get_or_create(
                code=section["code"],
                defaults={"title": section["title"]},
            )

            status = 'Created' if created else 'Exists'
            self.stdout.write(self.style.SUCCESS(
                f"{status}: Section {section['code']} - {section['title']}"
            ))

            return section_obj, created
        except Exception as e:
            self.stderr.write(self.style.ERROR(
                f"Error initializing section {section['code']}: {e!s}"
            ))
            return None, False

    def init_subsections(self, section_obj, section_code, dry_run=False):
        """Initialize subsections for a given section"""
        if section_code not in SUBSECTIONS:
            return

        for subsection in SUBSECTIONS[section_code]:
            try:
                if dry_run:
                    self.stdout.write(f"  Would create subsection: {subsection['code']} - {subsection['title']}")
                    continue

                subsection_obj, sub_created = DocumentSubsection.objects.get_or_create(
                    section=section_obj,
                    code=subsection["code"],
                    defaults={"title": subsection["title"]},
                )

                status = 'Created' if sub_created else 'Exists'
                self.stdout.write(self.style.SUCCESS(
                    f"  {status}: Subsection {subsection['code']} - {subsection['title']}"
                ))
            except Exception as e:
                self.stderr.write(self.style.ERROR(
                    f"  Error initializing subsection {subsection['code']}: {e!s}"
                ))

    @transaction.atomic
    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)

        if dry_run:
            self.stdout.write(self.style.WARNING("Running in dry-run mode - no changes will be made"))

        success_count = 0
        error_count = 0

        try:
            with transaction.atomic():
                for section in SECTIONS:
                    section_obj, success = self.init_section(section, dry_run)

                    if success:
                        success_count += 1
                        if section_obj or dry_run:
                            self.init_subsections(section_obj, section["code"], dry_run)
                    else:
                        error_count += 1

                if dry_run:
                    # Roll back the transaction in dry-run mode
                    transaction.set_rollback(True)

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Fatal error during initialization: {e!s}"))
            sys.exit(1)

        # Summary output
        self.stdout.write(self.style.SUCCESS(
            f"\n✅ Initialization {'simulation' if dry_run else 'complete'}: "
            f"{success_count} sections processed successfully, {error_count} errors"
        ))

        if error_count > 0:
            self.stderr.write(self.style.WARNING(
                "Some sections or subsections could not be initialized. Check the logs above."
            ))
            return 1

        return 0
