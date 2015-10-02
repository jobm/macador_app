# from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
# Create your views here

#request a user
def bookmark_list(request):
    #select all bookmarks
    bookmarks = Bookmark.public.all()
    # set the context to the bookmarks in the dictionary
    context = {'bookmarks': bookmarks}
    # render the request
    return render(request, 'marcador/bookmark_list.html', context)

# request for user specific bookmarks
def bookmark_user(request, username):
    # GET the user and the name
    user = get_object_or_404(User, username=username)
    # check if the reuested user is the user
    # if so then return that users bookmarks
    if request.user == user:
        bookmarks = user.bookmarks.all()
    # if not then return the public bookmarks for that user
    else:
        bookmarks = Bookmark.public.filter(owner__username=username)
    # set the context
    context = {'bookmarks': bookmarks, 'owner': user}
    # retun the view
    return render(request, 'marcador/bookmark_user.html', context)
