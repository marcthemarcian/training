from django import template

from facebook.models import Like

register = template.Library()


@register.simple_tag
def has_liked(user, item):
    if item.likes.filter(user=user):
        return '<a href="" class="toggleLike" name="{0}">Unlike</a>'.format(
            item.id
        )
    else:
        return '<a href="" class="toggleLike" name="{0}">Like</a>'.format(
            item.id
        )


@register.simple_tag
def count_likes(user, post):
    likes = post.likes.all()
    n = len(likes)
    s = ""

    if n == 0:
        s = 'Be the first one to like this post.'
    elif n == 1:
        if likes.last().user == user:
            s = "You like this."
        else:
            s = "{0} likes this.".format(likes.last().user.first_name)
    else:
        if likes.filter(user=user):
            name = "You"
        else:
            name = likes.last().user.first_name

        s = "{0} and {1} other(s) like this.".format(name, n - 1)

    return s
