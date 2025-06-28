from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.contrib.auth.models import Group

@staff_member_required
def admin_group_test(request):
    """
    Test view to verify that the Group model is accessible
    and display information about available groups
    """
    groups = Group.objects.all()
    group_info = "\n".join([f"- {group.name} (id: {group.id})" for group in groups])
    
    response_text = f"""
    <h1>Group Admin Test</h1>
    <p>Number of groups: {groups.count()}</p>
    <h2>Available Groups:</h2>
    <pre>{group_info}</pre>
    <p><a href="/admin/auth/group/">Return to Group Admin</a></p>
    """
    
    return HttpResponse(response_text)
