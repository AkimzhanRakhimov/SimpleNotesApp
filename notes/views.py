
from django.shortcuts import render, get_object_or_404, redirect
from .models import Note,Category
from .forms import NoteForm, CategoryForm
from django.contrib.auth import authenticate, login as auth_login,logout
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required
@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user)  # Теперь фильтруем заметки по пользователю

    # Фильтрация и поиск
    category_filter = request.GET.get('category')
    if category_filter:
        notes = notes.filter(category__id=category_filter)

    query = request.GET.get('q')
    if query:
        notes = notes.filter(title__icontains=query) | notes.filter(content__icontains=query)

    categories = Category.objects.all()

    return render(request, 'notes/note_list.html', {'notes': notes, 'categories': categories, 'query': query})


def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'notes/note_detail.html', {'note': note})

def note_create(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note = form.save()
            return redirect('note_detail', pk=note.pk)
    else:
        form = NoteForm()
    return render(request, 'notes/note_edit.html', {'form': form})

def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save()
            return redirect('note_detail', pk=note.pk)
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/note_edit.html', {'form': form})

def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    note.delete()
    return redirect('note_list')
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'notes/category_list.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'notes/category_form.html', {'form': form})

def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'notes/category_form.html', {'form': form})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'notes/category_confirm_delete.html', {'category': category})
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'notes/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('note_list')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, 'notes/login_view.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')