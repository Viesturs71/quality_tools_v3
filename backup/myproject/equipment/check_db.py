import os
import sys

import django

# Add the project directory to the Python path
sys.path.append('c:\\Users\\Viesturs\\anaconda_projects\\quality_tools_v2\\myproject')
# Or using relative paths:
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.db import connection


def check_maintenance_fields():
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'equipment_equipment'
        """)
        columns = [row[0] for row in cursor.fetchall()]
        maintenance_fields = [
            'daily_maintenance', 'weekly_maintenance', 'monthly_maintenance',
            'quarterly_maintenance', 'annual_maintenance'
        ]

        [field for field in maintenance_fields if field in columns]
        missing = [field for field in maintenance_fields if field not in columns]


        return len(missing) == 0  # All fields are present

def check_equipment_type_field():
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT
            column_name,
            data_type,
            character_maximum_length,
            is_nullable
        FROM information_schema.columns
        WHERE table_name = 'equipment_equipment' AND column_name = 'equipment_type'
        """)
        column_info = cursor.fetchone()

        if column_info:
            column_name, data_type, max_length, is_nullable = column_info

            # Check for the values in the equipment_type field
            cursor.execute("""
            SELECT DISTINCT equipment_type_id FROM equipment_equipment
            """)
            cursor.fetchall()

            # Get information about the equipment_type table
            cursor.execute("""
            SELECT id, name, requires_metrological_control
            FROM equipment_equipmenttype
            """)
            types = cursor.fetchall()
            for _type_id, _name, _req_metro in types:
                pass
        else:
            pass

if __name__ == "__main__":
    all_present = check_maintenance_fields()

    check_equipment_type_field()
