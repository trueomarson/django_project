from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib import auth

from .forms import Signup, Login, Edit

from .models import Song, Playlist

# Create your views here.


my_songs = [
    {"id": 1, "Track": "thank u, next", "Artist": "Ariana Grande",
        "Album": "thank u, next", "Length": "3:27", "playlist_id": 1},
    {"id": 2, "Track": "One Kiss, next", "Artist": "Dua Lipa, Calvin Harris",
     "Album": "One Kiss", "Length": "3:34", "playlist_id": 1},
    {"id": 3, "Track": "Better Now", "Artist": "Post Malone",
     "Album": "beerbongs & bentleys", "Length": "3:51", "playlist_id": 1},
    {"id": 4, "Track": "The Middle", "Artist": "Grey,Marren Morris, ZEDD",
     "Album": "The Middle", "Length": "3:04", "playlist_id": 1},
    {"id": 5, "Track": "Love Lies", "Artist": "Normani, Khalid",
     "Album": "Love Lies", "Length": "3:21", "playlist_id": 2},
    {"id": 6, "Track": "Rise", "Artist": "Jack & Jack, Jonas Blue",
     "Album": "Blue", "Length": "3:14", "playlist_id": 2},
]

my_playlists = [
    {"id": 1, "name": "Car Playlist", "numberOfSongs": 4},
    {"id": 2, "name": "Coding Playlist", "numberOfSongs": 2}
]

users = [
    {"id": 1, "full_name": "john", "email": "john123@gmail.com", "password": "adminpass"},
]


def home(request):

    playlists = Playlist.objects.all()
    return render(request, 'zing_it/home.html', {"my_playlists": playlists})


def about(request):

    try:
        thankyou_next = Song.objects.create(
            track="thank u, next", artist="Ariana Grande", album="thank u, next", length="3:27", playlist_id=1)
        one_kiss_next = Song.objects.create(
            track="One Kiss, next", artist="Dua Lipa, Calvin Harris", album="One Kiss", length="3:34", playlist_id=1)
        better_now = Song.objects.create(
            track="Better Now", artist="Post malone", album="beerbongs & bentleys", length="3:51", playlist_id=1)
        the_middle = Song.objects.create(
            track="The Middle", artist="Grey,Marren Morris, ZEDD", album="The Middle", length="3:04", playlist_id=1)
        love_lies = Song.objects.create(
            track="Love Lies", artist="Normani, Khalid", album="Love Lies", length="3:21", playlist_id=2)
        rise = Song.objects.create(
            track="Rise", artist="Jack & Jack, Jonas Blue", album="Blue", length="3:14", playlist_id=2)

        car_playlist = Playlist.objects.create(
            name="Car Playlist", number_of_songs=4)
        coding_playlist = Playlist.objects.create(
            name="Coding Playlist", number_of_songs=2)

        thankyou_next.save()
        one_kiss_next.save()
        better_now.save()
        the_middle.save()
        love_lies.save()
        rise.save()
        car_playlist.save()
        coding_playlist.save()
    except Exception as e:
        print(e)

    return HttpResponse("""<h1>About Us:</h1><p>With Zing, you can easily find the music of your choice and easily share it with other people. You can also browse through the collections of friends, artists, and celebrities, or create a playlist of your own.
      Soundtrack your life with Zing. Subscribe or listen for free.</p>""")


def playlist(request, id):
    songs = []
    playlist_name = ''

    playlist = Playlist.objects.get(pk=id)

    playlist_name = playlist.name

    if len(playlist_name) == 0:
        raise Http404("Such playlist does not exist")

    all_songs = Song.objects.all()

    for song in all_songs:
        if(id == song.playlist_id):
            songs.append(song)

    return render(request, 'zing_it/songs.html', {"songs": songs, "playlist_name": playlist_name})


def edit(request, id):
    form = Edit(request.POST or None)
    if form.is_valid():
        track = form.cleaned_data.get("track")
        album = form.cleaned_data.get("album")
        artist = form.cleaned_data.get("artist")
        length = form.cleaned_data.get("length")
        playlist_id = form.cleaned_data.get("playlist_id")

        song = Song.objects.get(id=id)

        song.track = track
        song.album = album
        song.artist = artist
        song.length = length
        song.playlist_id = playlist_id

        song.save()

        return render(request, 'zing_it/edit.html', {"form": form, "status": "Your song is updated successfully!"})

    return render(request, 'zing_it/edit.html', {"form": form})


def signup(request):
    form = Signup(request.POST or None)
    if form.is_valid():
        password = form.cleaned_data.get("password")
        confirm_password = form.cleaned_data.get("confirm_password")
        name = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        if(password != confirm_password):
            return render(request, 'zing_it/signup.html', {"form": form, "status": "Your passwords don't match!"})
        else:
            try:
                user = User.objects.get(email=email)
                return render(request, 'zing_it/signup.html', {"form": form, "status": "This email already exists in the system! Please log in instead."})
            except Exception as e:
                print(e)
                new_user = User.objects.create_user(
                    username=name, email=email, password=password)
                new_user.save()
                return render(request, 'zing_it/signup.html', {"form": form, "status": "Signed up Successfully!"})
    return render(request, 'zing_it/signup.html', {"form": form})


def login(request):
    form = Login(request.POST or None)
    status = " "
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            status = "You have successfully logged in!"
        else:
            status = "You credentials are not valid. Try again!"
    return render(request, 'zing_it/login.html', {"form": form, "status": status})
