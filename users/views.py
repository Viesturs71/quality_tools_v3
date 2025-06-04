from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from quality_docs.models.logs import DocumentLog  # Adjust import if necessary


@login_required
def profile_view(request):
    return render(request, 'user/profile.html')

@login_required
def activity_log(request):
    # Get user's activities, order by timestamp (not created_at)
    activities = DocumentLog.objects.filter(user=request.user).order_by('-timestamp')

    return render(request, 'user/activity_log.html', {
        'activities': activities
    })
