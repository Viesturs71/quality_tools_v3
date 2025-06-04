from django.db import connection


def check_fields():
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'equipment_equipment'
        """)
        [row[0] for row in cursor.fetchall()]


if __name__ == "__main__":
    check_fields()
