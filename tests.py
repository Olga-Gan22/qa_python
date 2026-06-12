from main import BooksCollector
import pytest

class TestBooksCollector:

# Добавляет две книги и проверяет их количество
    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    @pytest.mark.parametrize("book_name", [
        '',  # пустая строка
        'A' * 41,  # 41 символ
    ])
#Не добавляет книгу с некорректным названием (пустая строка или слишком длинное)
    def test_add_new_book_invalid_name_not_added(self, book_name):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        assert book_name not in collector.get_books_genre()

#Не добавляет книгу, название которой состоит только из пробелов
    def test_add_new_book_only_spaces_not_added(self):
        collector = BooksCollector()
        book_name = '   '
        collector.add_new_book(book_name)
        # Проверяем, что книга с пробелами не добавлена в словарь
        assert book_name not in collector.get_books_genre()

    @pytest.mark.parametrize("book_name,genre", [
        ('1984', 'Фантастика'),
        ('Винни-Пух', 'Мультфильмы'),
        ('Оно', 'Ужасы'),
        ('Шерлок Холмс', 'Детективы'),
        ('Один дома', 'Комедии')
    ])
#Устанавливает и получает жанр для книги
    def test_set_and_get_book_genre(self, book_name, genre):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.get_book_genre(book_name) == genre

    @pytest.mark.parametrize("book_name", [
        'Несуществующая книга',
        'Выдуманный роман'
    ])
#Возвращает None для несуществующей книги
    def test_get_book_genre_nonexistent_book_returns_none(self, book_name):
        collector = BooksCollector()
        assert collector.get_book_genre(book_name) is None

    @pytest.mark.parametrize("genre,books", [
        ('Фантастика', ['1984', 'Дюна']),
        ('Мультфильмы', ['Винни-Пух', 'Король Лев'])
    ])
#Находит книги заданного жанра
    def test_get_books_with_specific_genre(self, genre, books):
        collector = BooksCollector()
        for book in books:
            collector.add_new_book(book)
            collector.set_book_genre(book, genre)

        result = collector.get_books_with_specific_genre(genre)
        for book in books:
            assert book in result

#Возвращает пустой список для несуществующего жанра
    def test_get_books_with_specific_genre_invalid_genre_returns_empty_list(self):
        collector = BooksCollector()
        result = collector.get_books_with_specific_genre('Неизвестный жанр')
        assert result == []

#Книги с возрастным рейтингом отсутствуют в списке книг для детей
    def test_get_books_for_children_only_safe_genres(self):
        collector = BooksCollector()

        # Безопасные книги (не в genre_age_rating)
        safe_books = [
            ('Винни-Пух', 'Мультфильмы'),
            ('Король Лев', 'Мультфильмы'),
            ('Один дома', 'Комедии'),
            ('Гарри Поттер', 'Фантастика')  # Фантастика не в age_rating
        ]
        for book_name, genre in safe_books:
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, genre)

        # Возрастные книги (в genre_age_rating: Ужасы, Детективы)
        adult_books = [
            ('Оно', 'Ужасы'),
            ('Молчание ягнят', 'Детективы')
        ]
        for book_name, genre in adult_books:
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, genre)

        children_books = collector.get_books_for_children()

        # Проверяем, что безопасные книги присутствуют
        for book_name, _ in safe_books:
            assert book_name in children_books

        # Проверяем, что возрастные книги отсутствуют
        for book_name, _ in adult_books:
            assert book_name not in children_books

    @pytest.mark.parametrize("favorite_books", [
        ['Любимая книга 1'],
        ['Книга A', 'Книга B'],
        ['Первая', 'Вторая', 'Третья']
    ])
#Добавляет книги в избранное и получает список избранного
    def test_add_and_get_favorites_books(self, favorite_books):
        collector = BooksCollector()
        for book in favorite_books:
            collector.add_new_book(book)
            collector.add_book_in_favorites(book)

        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == len(favorite_books)
        for book in favorite_books:
            assert book in favorites

#Удаляет книгу из избранного
    def test_delete_book_from_favorites(self):
        collector = BooksCollector()
        book_name = 'Удаляемая книга'
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        collector.delete_book_from_favorites(book_name)
        favorites = collector.get_list_of_favorites_books()
        assert book_name not in favorites

#У добавленной книги нет жанра по умолчанию
    def test_new_book_has_no_genre(self):
        collector = BooksCollector()
        book_name = 'Новая книга без жанра'
        collector.add_new_book(book_name)
        assert collector.get_book_genre(book_name) == ''

#Не добавляет дубликат книги в избранное
    def test_add_existing_book_to_favorites_ignores_duplicate(self):
        collector = BooksCollector()
        book_name = 'Любимая книга'
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        collector.add_book_in_favorites(book_name)  # Повторная попытка добавления
        favorites = collector.get_list_of_favorites_books()
        assert favorites.count(book_name) == 1
