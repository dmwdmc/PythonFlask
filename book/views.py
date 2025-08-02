#book/views.py
import logging

from flask import render_template, flash, redirect, url_for
from flask_babel import gettext as _
from flask_login import login_required

from book import bp
from book.forms import BookForm
from book.models import Book
from dbs import db

# Configure logging
logger = logging.getLogger(__name__)

@bp.route('/books', methods=['POST'])
@login_required
def create_book():
    """Display books list and handle book creation"""
    form = BookForm()
    # Optimization: If Book model has user association, can use joinedload
    books = Book.query.all()
    if form.validate_on_submit():
        book = Book(
            name=form.name.data,
            content=form.content.data
        )
        db.session.add(book)
        db.session.commit()
        logger.info(f'Book created: {book.name}')
        flash(_('Book_created'), 'success')
        return redirect(url_for('book.books'))
    else:
        logger.warning('Form validation failed!')
        flash(_('Form_validation_failed'), 'error')
    
    return render_template('books.html', books=books, form=form)


@bp.route('/books', methods=['GET'])
@login_required
def books():
    form = BookForm()
    books = Book.query.all()
    return render_template('books.html', books=books, form=form)