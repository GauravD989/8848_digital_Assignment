from django import forms
from .models import Book, Member, Transaction

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'publisher', 'page_count', 'stock', 'price']

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'email']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['book', 'member', 'issue_date', 'return_date', 'quantity']

class SearchForm(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    author = forms.CharField(max_length=100, required=False)

class ImportBooksForm(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    authors = forms.CharField(max_length=100, required=False)
    isbn = forms.CharField(max_length=20, required=False)
    publisher = forms.CharField(max_length=100, required=False)
    page = forms.IntegerField(required=False)
    num_books = forms.IntegerField(min_value=1)
