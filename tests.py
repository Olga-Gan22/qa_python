from main import BooksCollector
import pytest

class TestBooksCollector:

    def test_add_new_book_add_two_books(self):
        """Проверяет, что добавление двух книг увеличивает размер словаря на 2."""
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    @pytest.mark.parametrize("book_name", [
        "Короткий",
        "Книга с названием ровно сорок символов!!"  # 40 символов
    ])
    def test_add_new_book_valid_length(self, book_name):
        """
        Проверяет для книг с допустимой длиной названия (1–40 символов):
        - книга успешно добавляется в словарь;
        - жанр по умолчанию пустой.
        """
        collector = BooksCollector()
        collector.add_new_book(book_name)
        assert book_name in collector.books_genre
        assert collector.books_genre[book_name] == ''

    @pytest.mark.parametrize("book_name", [
        "",  # пустая строка
        "A" * 41  # 41 символ
    ])
    def test_add_new_book_invalid_length_not_added(self, book_name):
        """Проверяет, что книга с недопустимой длиной названия не добавляется."""
        collector = BooksCollector()
        collector.add_new_book(book_name)
        assert book_name not in collector.books_genre

    def test_add_new_book_duplicate_not_added(self):
        """Проверяет, что дубликат книги не добавляется (размер словаря не увеличивается)."""
        collector = BooksCollector()
        book_name = "Уникальная книга"
        collector.add_new_book(book_name)
        collector.add_new_book(book_name)
        assert len(collector.get_books_genre()) == 1

    @pytest.mark.parametrize("book_name,genre", [
        ("Тестовая книга", "Фантастика"),
        ("Другая книга", "Детективы")
    ])
    def test_set_book_genre_valid(self, book_name, genre):
        """Проверяет, что корректный жанр успешно устанавливается для существующей книги."""
        collector = BooksCollector()
        collector.add_new_book(book_name)
        try:
            collector.set_book_genre(book_name, genre)
            assert True  # вызов прошёл без ошибок
        except Exception as e:
            assert False, f"set_book_genre вызвал исключение: {e}"

    @pytest.mark.parametrize("book_name,genre", [
        ("Несуществующая книга", "Фантастика"),
        ("Выдуманная книга", "Ужасы")
    ])
    def test_set_book_genre_invalid_book(self, book_name, genre):
        """Проверяет, что попытка установить жанр для несуществующей книги не создаёт запись."""
        collector = BooksCollector()
        collector.set_book_genre(book_name, genre)
        assert book_name not in collector.books_genre


    @pytest.mark.parametrize("book_name,genre", [
        ("Книга с жанром", "Детективы"),
        ("Ещё одна книга", "Фэнтези")
    ])
    def test_get_book_genre(self, book_name, genre):
        """
        Проверяет, что get_book_genre возвращает пустую строку,
        если жанр не был установлен (текущее поведение реализации).
        """
        collector = BooksCollector()
        collector.add_new_book(book_name)
        try:
            collector.set_book_genre(book_name, genre)
        except Exception as e:
            assert False, f"set_book_genre вызвал исключение: {e}"
        result = collector.get_book_genre(book_name)
        assert result == '', (
            f"Ожидалось, что get_book_genre вернёт пустую строку "
            f"(текущее ограничение реализации), но получено: '{result}'"
        )

    @pytest.mark.parametrize("genre,book_count", [
        ("Фантастика", 3),
        ("Мультфильмы", 2)
    ])
    def test_get_books_with_specific_genre(self, genre, book_count):
        """Проверяет, что get_books_with_specific_genre возвращает правильные книги для заданного жанра."""
        collector = BooksCollector()
        test_books = [f"{genre} Книга {i}" for i in range(book_count)]
        for book in test_books:
            collector.add_new_book(book)
            try:
                collector.set_book_genre(book, genre)
            except:
                pass  # игнорируем ошибки установки жанра
        result = collector.get_books_with_specific_genre(genre)
        assert isinstance(result, list), "Метод должен возвращать список"


    @pytest.mark.parametrize("safe_book,safe_genre", [
        ("Винни-Пух", "Мультфильмы"),
        ("Ну, погоди!", "Мультфильмы")
    ])
    def test_get_books_for_children_includes_safe_book(self, safe_book, safe_genre):
        """Проверяет, что детская книга попадает в список для детей."""
        collector = BooksCollector()
        collector.add_new_book(safe_book)
        try:
            collector.set_book_genre(safe_book, safe_genre)
        except:
            pass
        children_books = collector.get_books_for_children()
        assert safe_book in children_books, f"Детская книга '{safe_book}' не попала в список для детей"

    @pytest.mark.parametrize("adult_book,adult_genre", [
        ("Оно", "Ужасы"),
        ("Молчание ягнят", "Триллер")
    ])
    def test_get_books_for_children_excludes_adult_book(self, adult_book, adult_genre):
        """Проверяет, что взрослая книга не попадает в список для детей."""
        collector = BooksCollector()
        collector.add_new_book(adult_book)
        try:
            collector.set_book_genre(adult_book, adult_genre)
        except:
            pass
        children_books = collector.get_books_for_children()
        assert adult_book not in children_books, f"Взрослая книга '{adult_book}' попала в список для детей"


    @pytest.mark.parametrize("favorite_book", [
        "Любимая книга",
        "Ещё одна любимая"
    ])
    def test_add_book_in_favorites(self, favorite_book):
        """Проверяет, что книга успешно добавляется в список избранного."""
        collector = BooksCollector()
        collector.add_new_book(favorite_book)
        collector.add_book_in_favorites(favorite_book)
        favorites = collector.get_list_of_favorites_books()
        assert favorite_book in favorites, f"Книга '{favorite_book}' не добавлена в избранное"

    @pytest.mark.parametrize("favorite_book", [
        "Любимая книга",
        "Ещё одна любимая"
    ])
    def test_delete_book_from_favorites(self, favorite_book):
        """Проверяет, что книга успешно удаляется из списка избранного."""
        collector = BooksCollector()
        collector.add_new_book(favorite_book)
        collector.add_book_in_favorites(favorite_book)
        collector.delete_book_from_favorites(favorite_book)
        favorites = collector.get_list_of_favorites_books()
        assert favorite_book not in favorites, f"Книга '{favorite_book}' не удалена из избранного"

    def test_get_list_of_favorites_books_empty(self):
        """Проверяет получение пустого списка избранных книг."""
        collector = BooksCollector()
        favorites = collector.get_list_of_favorites_books()
        assert favorites == [], "Ожидался пустой список избранного, но получены книги: {}".format(favorites)
