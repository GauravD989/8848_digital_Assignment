from django.shortcuts import render, redirect
from .models import Book, Transaction, Member
from .forms import BookForm, MemberForm, TransactionForm, SearchForm, ImportBooksForm

# Create your views here.

#  *****  For the Book Crud *****
def home(request):
    books = Book.objects.all()
    trans = Transaction.objects.all()
    return render(request, 'home.html', {'books': books, 'trans':trans})

def list_books(request):
    books = Book.objects.all()
    trans = Transaction.objects.all()
    return render(request, 'book_list.html', {'books': books, 'trans':trans})

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'book_form.html', {'form': form})

def edit_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'book_form.html', {'form': form})

def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('list_books')

#  *****  For the Member Crud and all *****

def list_members(request):
    members = Member.objects.all()
    return render(request, 'member_list.html', {'members': members})

def add_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_members')
    else:
        form = MemberForm()
    return render(request, 'member_form.html', {'form': form})

def edit_member(request, member_id):
    member = Member.objects.get(id=member_id)
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('list_members')
    else:
        form = MemberForm(instance=member)
    return render(request, 'member_form.html', {'form': form})

def delete_member(request, member_id):
    member = Member.objects.get(id=member_id)
    member.delete()
    return redirect('list_members')

# ***** Issue a Book for the User ******

def issue_book(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():

            book = form.cleaned_data['book']
            member = form.cleaned_data['member']
            quantity = form.cleaned_data['quantity']

            if book.stock >= quantity:
                transaction = form.save()

                book.stock -= quantity
                book.save()
                return redirect('home')
    else:
        form = TransactionForm()
    return render(request, 'transaction_form.html', {'form': form})

# ** Issue a Book Return from a Member **

def return_book(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)

    if request.method == 'POST':
        returned_quantity = int(request.POST.get('returned_quantity', 0))

        if 0 <= returned_quantity <= transaction.quantity:
            outstanding_fees = transaction.calculate_outstanding_fees

            transaction.quantity -= returned_quantity
            transaction.save()

            transaction.book.stock += returned_quantity
            transaction.book.save()

            return redirect('home')

    return render(request, 'transaction_return.html', {'transaction': transaction})

# ** Search for a Book by Name and Author **

def search_books(request):
    if request.method == 'GET':
        title = request.GET.get('title', '')
        author = request.GET.get('author', '')
        books = Book.objects.filter(title__icontains=title, author__icontains=author)
    else:
        books = Book.objects.all()
    return render(request, 'book_search.html', {'books': books})


import requests

def import_books(request):
    if request.method == 'POST':
        form = ImportBooksForm(request.POST)
        if form.is_valid():
            num_books_to_import = form.cleaned_data['num_books']
            title = form.cleaned_data['title']
            authors = form.cleaned_data['authors']
            isbn = form.cleaned_data['isbn']
            publisher = form.cleaned_data['publisher']
            page = form.cleaned_data['page']

            # Create the API URL with all the specified parameters
            api_url = f"https://frappe.io/api/method/frappe-library?page=1&title={title}&authors={authors}&isbn={isbn}&publisher={publisher}&page={page}"

            try:
                response = requests.get(api_url)
                data = response.json()

                if "message" in data:
                    books = data["message"]
                    
                    # Limit the number of imported books to num_books_to_import
                    books = books[:num_books_to_import]
                    
                    # Loop through the books and create records in your database
                    for book_data in books:
                        Book.objects.create(
                            title=book_data.get('title', ''),
                            author=book_data.get('authors', ''),
                            isbn=book_data.get('isbn', ''),
                            publisher=book_data.get('publisher', ''),
                            page_count=int(book_data.get('num_pages', 0)),
                        )

                    num_books_imported = len(books)
                    return render(request, 'import_success.html', {'num_books_imported': num_books_imported})
                else:
                    return render(request, 'import_books.html', {'form': form, 'error_message': 'No books found in the API response.'})
            except requests.exceptions.RequestException as e:
                return render(request, 'import_books.html', {'form': form, 'error_message': str(e)})
    else:
        form = ImportBooksForm()

    return render(request, 'import_books.html', {'form': form})
