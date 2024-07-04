from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
import random
from wikinow.models import *
from wikinow.forms import EntryForm
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

def index(request):
    index_entries = Entry.objects.all()
    return render(request, 'wikinow/index.html', {'index_entries': index_entries})


def random_page(request):
   total = Entry.objects.all().count()
   pk = random.randint(1, total)
   random_page = Entry.objects.filter(pk=pk)
   return render(request, 'wikinow/random_page.html', {'random_page': random_page})
    
@login_required
def new_page(request):
    response_message = ''
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            if Entry.objects.filter(title__iexact=title).exists():
                response_message = f"An entry with title '{title}' already exists."
            else:
                form.save()
                response_message = 'Entry created successfully!'
                form = EntryForm()
        else:
            response_message = 'Form is invalid. Please correct the errors.'
    else:
        form = EntryForm()
    return render(request, 'wikinow/new_page.html', {'form': form, 'response_message': response_message})
    
@login_required
def edit_page(request, page_id):
    page = get_object_or_404(Entry, id=page_id)

    if request.method == 'POST':
        form = EntryForm(request.POST, instance=page)
        if form.is_valid():
            form.save()
            return redirect('view_page', page_id=page.id)
    else:
        form = EntryForm(instance=page)

    return render(request, 'wikinow/edit_page.html', {'form': form, 'page': page})

def view_page(request, page_id):
    entry = get_object_or_404(Entry, id=page_id)
    return render(request, 'wikinow/view_page.html', {'entry': entry})

def search(request):
    query = request.GET.get('q', '')
    if query:
        entries = Entry.objects.filter(title__icontains=query).values('title', 'id')[:10]
        suggestions = list(entries)
    else:
        suggestions = []
    return JsonResponse(suggestions, safe=False)

def indexes(request):
    content_list = list(Entry.objects.all())
    random.shuffle(content_list)
    return render(request, 'wikinow/Indexes.html', {'content_list': content_list})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        print(username)
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "wikinow/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "wikinow/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "wikinow/register.html", {
                "message": "Passwords must match."
            })
        else:
            # Attempt to create new user
            try:
                user = CustomUser.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            except IntegrityError as e:
                print(e)
                return render(request, "wikinow/register.html", {
                    "message": "Email address already taken."
                })
    else:
        return render(request, "wikinow/register.html")
