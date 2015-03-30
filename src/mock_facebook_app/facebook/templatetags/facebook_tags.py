from django import template
from facebook.models import Like

register = template.Library()


@register.simple_tag
def hasLiked(user, item):
    if item.like.filter(user=user):
        return '<a href="" class="toggleLike" name="%i">Unlike</a>' % item.id
    else:
        return '<a href="" class="toggleLike" name="{0}">Like</a>'.format(
            item.id
        )


@register.simple_tag
def countLikes(user, post):
    likes = Like.objects.filter(post=post)
    n = len(likes)
    s = ""

    if n == 0:
        s = 'Be the first one to like this post.'
    elif n == 1:
        if likes.last().user == user:
            s = "You like this."
        else:
            s = likes.last().user.first_name + " likes this."
    else:
        if likes.filter(user=user):
            name = "You"
        else:
            name = likes.last().user.first_name

        s = name + " and " + str(n - 1) + " other(s) like this."

    return s
