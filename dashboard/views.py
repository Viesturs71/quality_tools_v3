from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone


@login_required
def index(request):
    """Main dashboard view"""

    # You can populate these with actual database queries once models are available
    context = {
        'working_equipment_count': 0,
        'repair_equipment_count': 0,
        'calibration_equipment_count': 0,
        'outofservice_equipment_count': 0,
        'recent_documents': [],
        'upcoming_audits': [],
        'user_tasks': [],
        'recent_activities': [],
        'pending_approvals': [],
    }

    # Example data for testing - you can remove this in production
    if settings.DEBUG:
        today = timezone.now().date()

        # Example equipment counts
        from random import randint
        context.update({
            'working_equipment_count': randint(10, 30),
            'repair_equipment_count': randint(1, 5),
            'calibration_equipment_count': randint(2, 8),
            'outofservice_equipment_count': randint(0, 3),
        })

        # Example documents
        context['recent_documents'] = [
            {'title': 'Equipment Maintenance Procedure', 'updated_at': today - timezone.timedelta(days=2)},
            {'title': 'Quality Manual v2.3', 'updated_at': today - timezone.timedelta(days=5)},
            {'title': 'Laboratory Testing Protocol', 'updated_at': today - timezone.timedelta(days=7)},
        ]

        # Example audits
        context['upcoming_audits'] = [
            {'title': 'Internal Quality Audit', 'scheduled_date': today + timezone.timedelta(days=15)},
            {'title': 'ISO 9001 Surveillance', 'scheduled_date': today + timezone.timedelta(days=30)},
        ]

        # Example tasks
        context['user_tasks'] = [
            {'title': 'Complete equipment inventory', 'due_date': today + timezone.timedelta(days=3), 'priority': 'high'},
            {'title': 'Review maintenance records', 'due_date': today + timezone.timedelta(days=7), 'priority': 'medium'},
            {'title': 'Update equipment documentation', 'due_date': today + timezone.timedelta(days=10), 'priority': 'low'},
        ]

    return render(request, 'dashboard/index.html', context)

@login_required
def home_view(request):
    """Main dashboard home view"""
    context = {
        'page_title': 'Dashboard',
        'user': request.user,
    }
    return render(request, 'dashboard/home.html', context)

@login_required  
def dashboard_view(request):
    """Dashboard overview with widgets"""
    context = {
        'page_title': 'Dashboard Overview',
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def index_view(request):
    """Dashboard index with module access"""
    context = {
        'page_title': 'System Overview',
    }
    return render(request, 'dashboard/index.html', context)
