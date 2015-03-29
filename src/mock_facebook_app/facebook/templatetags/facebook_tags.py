from django import template
from facebook.models import Like

register = template.Library()


@register.simple_tag
def hasLiked(user, item):
    if item.like.filter(user=user):
        return '<a href="" class="toggleLike" name="%i">Unlike</a>' % item.id
    else:
        print item.id
        print "eeeeek"
        return '<a href="" class="toggleLike" name="{0}">Like</a>'.format(item.id)


@register.simple_tag
def countLikes(user, item):
    likes = Like.objects.filter(post=item)
    n = len(likes)

    if n == 0:
        return 'Be the first one to like this post.'
    elif n == 1:
        return "You like this." if likes.last().user == user else likes.last().user.first_name + " likes this."
    else:
        name = "You" if item.like.filter(user=user) else likes.last().user.first_name
        return name + " and " + str(n - 1) + " other(s) like this."
