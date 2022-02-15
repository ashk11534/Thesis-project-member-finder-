
from django import template
from ..models import User, UserMessage

register = template.Library()

@register.filter
def total_messages(user_id):
    receiver = User.objects.get(id=user_id)
    messages = UserMessage.objects.filter(receiver=receiver)
    return len(messages)
