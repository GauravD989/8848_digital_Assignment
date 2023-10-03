from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('books/', views.list_books, name='list_books'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    
    path('members/', views.list_members, name='list_members'),
    path('members/add/', views.add_member, name='add_member'),
    path('members/edit/<int:member_id>/', views.edit_member, name='edit_member'),
    path('members/delete/<int:member_id>/', views.delete_member, name='delete_member'),
    
    path('transactions/issue/', views.issue_book, name='issue_book'),
    path('transactions/return/<int:transaction_id>/', views.return_book, name='return_book'),
    
    path('books/search/', views.search_books, name='search_books'),

    path('import-books/', views.import_books, name='import_books'),
]
