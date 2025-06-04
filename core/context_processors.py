def admin_navigation(request):
    return {
        "navigation_sections": [
            {
                "title": "Authentication and Authorization",
                "icon": "fa-user-lock",
                "items": [
                    {"label": "Users", "url": "/admin/auth/user/"},
                    {"label": "Groups", "url": "/admin/auth/group/"},
                    {"label": "Permissions", "url": "/admin/auth/permission/"},
                ],
            },
            {
                "title": "Companies",
                "icon": "fa-building",
                "items": [
                    {"label": "Companies", "url": "/admin/company/company/"},
                    {"label": "Departments", "url": "/admin/company/department/"},
                    {"label": "Locations", "url": "/admin/company/location/"},
                ],
            },
            {
                "title": "Equipment Management",
                "icon": "fa-tools",
                "items": [
                    {"label": "Equipment Registry", "url": "/admin/equipment/equipment/"},
                    {"label": "Equipment Categories", "url": "/admin/equipment/equipmentcategory/"},
                    {"label": "Maintenance Records", "url": "/admin/equipment/maintenancerecord/"},
                    {"label": "Equipment Documents", "url": "/admin/equipment/equipmentdocument/"},
                ],
            },
            {
                "title": "Management Documentation",
                "icon": "fa-file-alt",
                "items": [
                    {"label": "Quality Documents", "url": "/admin/quality_docs/qualitydocument/"},
                    {"label": "Document Types", "url": "/admin/quality_docs/documenttype/"},
                    {"label": "Document Sections", "url": "/admin/quality_docs/documentsection/"},
                ],
            },
            {
                "title": "Personnel Management",
                "icon": "fa-users",
                "items": [
                    {"label": "Staff Records", "url": "/admin/personnel/employee/"},
                    {"label": "Qualifications", "url": "/admin/personnel/qualification/"},
                    {"label": "Training Records", "url": "/admin/personnel/trainingrecord/"},
                ],
            },
            {
                "title": "Standards",
                "icon": "fa-book",
                "items": [
                    {"label": "Standards", "url": "/admin/standards/standard/"},
                    {"label": "Standard Sections", "url": "/admin/standards/standardsection/"},
                    {"label": "Standard Subsections", "url": "/admin/standards/standardsubsection/"},
                ],
            },
            {
                "title": "User Accounts",
                "icon": "fa-user-cog",
                "items": [
                    {"label": "User Profiles", "url": "/admin/accounts/userprofile/"},
                    {"label": "User Roles", "url": "/admin/accounts/userrole/"},
                    {"label": "User Permissions", "url": "/admin/accounts/userpermission/"},
                ],
            },
        ]
    }
