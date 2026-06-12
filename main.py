class BooksCollector:
    def __init__(self):
        self.books_genre = {}
        self.favorites = []

    def add_new_book(self, name):
        # Проверяем длину и отсутствие только пробелов
        if 0 < len(name) < 41 and name.strip() != '':
            self.books_genre[name] = ''

    def set_book_genre(self, book_name, genre):
        if book_name in self.books_genre:
            self.books_genre[book_name] = genre

    def get_book_genre(self, book_name):
        return self.books_genre.get(book_name, None)

    def get_books_with_specific_genre(self, genre):
        return [book for book, book_genre in self.books_genre.items() if book_genre == genre]

    def get_books_for_children(self):
        age_restricted_genres = ['Ужасы', 'Детективы']
        return [
            book for book, genre in self.books_genre.items()
            if genre not in age_restricted_genres
        ]

    def add_book_in_favorites(self, book_name):
        if book_name in self.books_genre and book_name not in self.favorites:
            self.favorites.append(book_name)

    def delete_book_from_favorites(self, book_name):
        if book_name in self.favorites:
            self.favorites.remove(book_name)

    def get_list_of_favorites_books(self):
        return self.favorites

    def get_books_genre(self):
        return self.books_genre
