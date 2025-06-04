import pandas as pd
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Importē ĀKK katalogu no CSV vai Excel"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Ceļš uz CSV vai Excel failu")

    def handle(self, *args, **options):
        file_path = options["file_path"]
        self.stdout.write(self.style.SUCCESS(f"📥 Importējam datus no: {file_path}"))

        try:
            # 📌 Izvēlas faila tipu un nolasa datus
            if file_path.endswith(".csv"):
                df = pd.read_csv(file_path, delimiter=",")
            elif file_path.endswith(".xlsx"):
                df = pd.read_excel(file_path)
            else:
                self.stderr.write(self.style.ERROR("❌ Nepareizs faila formāts!"))
                return

            # 📌 Nepieciešamās kolonnas
            required_columns = [
                "Gads",
                "Pakalpojuma sniedzējs",
                "Izmeklējamais materiāls",
                "Kods",
                "Cena",
            ]

            if not all(col in df.columns for col in required_columns):
                self.stderr.write(
                    self.style.ERROR(
                        f"❌ Trūkst kolonnas! Nepieciešamas: {', '.join(required_columns)}"
                    )
                )
                return

            # 📌 Notīra un pārveido skaitliskos laukus
            df["Cena"] = pd.to_numeric(df["Cena"], errors="coerce").fillna(
                0
            )  # Pārvērš cenu par skaitli, aizstāj NaN ar 0

            with transaction.atomic():
                for _, row in df.iterrows():
                    AkkKatalogs.objects.update_or_create(
                        gads=row["Gads"],
                        kods=row["Kods"],
                        defaults={
                            "pakalpojuma_sniedzejs": row["Pakalpojuma sniedzējs"],
                            "izmeklejamais_materials": row["Izmeklējamais materiāls"],
                            "cena": row["Cena"],
                        },
                    )

            self.stdout.write(
                self.style.SUCCESS("✅ ĀKK katalogs veiksmīgi importēts!")
            )

        except ValidationError as e:
            self.stderr.write(self.style.ERROR(f"❌ Validācijas kļūda: {e}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ Kļūda importēšanas laikā: {e}"))
