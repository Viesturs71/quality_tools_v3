from myproject.admin import custom_admin_site


def get_standard_admin():
    from quality_docs.admin import StandardAdmin

    return StandardAdmin


__all__ = ["StandardAdmin", "custom_admin_site"]
