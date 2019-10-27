from django import template


register = template.Library()

@register.filter
def duration(value):
    try:
        hours, rem = divmod(value.total_seconds(), 3600)
        minutes, seconds = divmod(rem, 60)
        if hours == 0:
            return '{} minutes {} seconds'.format(round(minutes), round(seconds))
        elif minutes == 0:
            return '{} seconds'.format(round(seconds))
        return '{} hours {} minutes'.format(round(hours), round(minutes))
    except AttributeError:
        return 'You\'ve just registered'
