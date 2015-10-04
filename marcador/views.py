# from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
# Create your views here
from .models import Bookmark
from .forms import BookmarkForm
#request a user
def bookmark_list(request):
    #select all bookmarks
    bookmarks = Bookmark.public.all()
    # set the context to the bookmarks in the dictionary
    context = {'bookmarks': bookmarks}
    # render the request
    return render(request, 'marcador/bookmark_list.html', context)

# request for user spejob/cific bookmarks
@login_required
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

@login_required
def bookmark_create(request):
    if request.method == 'POST':
        form = BookmarkForm(data=request.POST)
        if form.is_valid():
            bookmark = form.save(commit=False)
            bookmark.owner = request.user
            bookmark.save()
            form.save_m2m()
            return redirect('marcador_bookmark_user',
                username=request.user.username)
    else:
        form = BookmarkForm()
    context = {'form': form, 'create': True}
    return render(request, 'marcador/form.html', context)



@login_required
def bookmark_edit(request, pk):
    bookmark = get_object_or_404(Bookmark, pk=pk)
    if bookmark.owner != request.user and not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        form = BookmarkForm(instance=bookmark, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('marcador_bookmark_user',
                username=request.user.username)
    else:
        form = BookmarkForm(instance=bookmark)
    context = {'form': form, 'create': False}
    return render(request, 'marcador/form.html', context)
