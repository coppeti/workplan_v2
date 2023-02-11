from pathlib import Path

from django.conf import settings


def activities_css(activities):
    """Generates a css file that will contain a class selector
    for each activity contained in the dict passed as argument.
    """
    target_folder = settings.BASE_DIR / 'static/css'
    file = open(target_folder / 'activities.css', 'w')
    for activity in activities:
        file.writelines(
            [f'.{activity.activity_class} {{\n', f'\tbackground-color: {activity.background_color};\n', f'\tcolor: {activity.text_color};\n', f'}}\n\n']
            )
    file.close()
    