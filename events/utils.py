from pathlib import Path

from django.conf import settings

from .models import Activities


def activity_to_css():
    """Generates a css file that will contain a class selector
    for each new activity and will be updated if activity is edited.
    """
    target_folder = settings.BASE_DIR / 'static/css'
    target_file = Path(target_folder / 'activities.css')
    activities = Activities.objects.all()
    file = open(target_file, 'w')
    for activity in activities:
        file.writelines(
            [f'.{activity.activity_class} {{\n', \
            f'\tbackground-color: {activity.background_color};\n', \
            f'\tcolor: {activity.text_color};\n', f'}}\n\n']
        )
    file.close()