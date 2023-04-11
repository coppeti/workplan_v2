from pathlib import Path

from django.conf import settings

from .models import Activities, Events
from accounts.models import CustomUser


def activity_to_css():
    """Generates a css file that will contain a class selector
    for each new activity and will be updated if activity is edited.
    """
    target_folder = settings.BASE_DIR / 'static/css'
    target_file = Path(target_folder / 'activities.css')
    activities = Activities.objects.all()
    file = open(target_file, 'w')
    for activity in activities:
        if 'wochenende' in activity.activity_class or 'feiertag' in activity.activity_class:
            file.writelines(
                [f'.{activity.activity_class} {{\n', \
                f'\tbackground-color: {activity.background_color};\n', f'}}\n\n'
                f'.{activity.activity_class}_card {{\n', \
                f'\tborder: {activity.background_color} 1px solid;\n', f'}}\n\n']
            )
        else:
            file.writelines(
                [f'.{activity.activity_class} {{\n', \
                f'\tbackground-color: {activity.background_color};\n', \
                f'\tcolor: {activity.text_color};\n', f'}}\n\n'
                f'.{activity.activity_class}_card {{\n', \
                f'\tborder: {activity.background_color} 1px solid;\n', f'}}\n\n']
            )
    file.close()


def admin_emails():
    """Returns an email list of all users who have a permission level equal to or greater than ADMIN."""
    admins = CustomUser.objects.filter(role__gte=CustomUser.ADMIN)
    emails = [admin.email for admin in admins]
    return emails

