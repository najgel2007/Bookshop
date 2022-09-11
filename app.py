import os
import pickle

from flask import Flask, render_template, abort, url_for, request
from werkzeug.utils import secure_filename, redirect

from book import Book
from config import Config
from forms import BookForm

app = Flask(__name__)
app.config.from_object(Config)

with open('all_books.bin', 'rb') as file:
    all_books = pickle.load(file)
    Book.max_id = len(all_books)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html', title='О сайте')


@app.route('/books')
@app.route('/catalog')
@app.route('/books/index')
def books():
    return render_template('books/index.html', books=all_books, title='Книги')


@app.route('/books/<int:id>')
def book(id):
    b = all_books.get(id)
    print(b)
    if not b:
        return abort(404)
    return render_template(f'books/book.html', book=b, title=f'{b.name} - {b.author}')


@app.route('/books/create', methods=['GET', 'POST'])
def create_book():
    form = BookForm
    if form.validate_on_submit():
        img_dir = os.path.join(os.path.dirname(app.instance_path), 'static', 'img')
        f = form.image.data
        filename = ''
        if f:
            filename = secure_filename(f.filename)
            f.save(os.path.join(img_dir, 'cover_' + filename))

        new_book = Book(name=form.name.data, author=form.author.data,
                        price=float(round(form.price.data, 2)), amount=form.amount.data,
                        genre=form.genre.data, description=form.description.data,
                        filename=filename)
        all_books[new_book.id] = new_book
        with open('all_books.bin', 'wb') as file:
            pickle.dump(all_books, file)
        return redirect(url_for('books'))
    return render_template('books/book_form.html', form=form, action_name='Создание')


@app.route('/books/<int:id>/edit', methods=['GET', 'POST'])
def edit_book(id):
    form = BookForm()

    editable_book = all_books.get(id)
    print(editable_book)
    if not editable_book:
        return abort(404)

    if form.validate_on_submit():
        img_dir = os.path.join(os.path.dirname(app.instance_path), 'static', 'img')
        f = form.image.data
        filename = secure_filename(f.filename)
        if filename and filename != editable_book.filename:
            f.save(os.path.join(img_dir, 'cover_' + filename))

            old_file = os.path.join(img_dir, 'cover_' + editable_book.filename)
            editable_book.filename = filename
            if os.path.exists(old_file):
                os.remove(old_file)
        editable_book.name = form.name.data
        editable_book.author = form.author.data
        editable_book.genre = form.genre.data
        editable_book.price = float(round(form.price.data, 2))
        editable_book.amount = form.amount.data
        editable_book.description = form.description.data
        with open('all_books.bin', 'wb') as file:
            pickle.dump(all_books, file)
        return redirect(url_for('books'))

    form.name.data = editable_book.name
    form.genre.data = editable_book.genre
    form.image = editable_book.filename
    form.description.data = editable_book.description
    form.price.data = editable_book.price
    form.author.data = editable_book.author

    return render_template('books/book_form.html',book = editable_book, form=form, file=editable_book.cover, action_name='Редактирование')


@app.route('/books/<int:id>/remove', methods=['GET', 'POST'])
def remove_book(id):
    removable_book = all_books.get(id)
    if not removable_book:
        return abort(404)

    if request.method == 'POST':
        img_dir = os.path.join(os.path.dirname(app.instance_path), 'static', 'img')
        old_file = os.path.join(img_dir, 'cover_' + removable_book.filename)
        if os.path.exists(old_file):
            os.remove(old_file)
        del all_books[id]
        with open('all_books.bin', 'wb') as file:
            pickle.dump(all_books, file)
        return redirect(url_for('books'))

    return render_template('books/remove_book.html', book=removable_book)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
