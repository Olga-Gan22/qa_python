from main import BooksCollector
import pytest

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

#Проверяет, что добавление двух книг увеличивает размер словаря на 2
    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

#Проверяет, что книга с коротким названием успешно добавляется в словарь
    def test_add_new_book_short_name_is_added(self):
        collector = BooksCollector()
        book_name = "Короткий"
        collector.add_new_book(book_name)
        assert book_name in collector.books_genre

#Проверяет, что у добавленной книги с коротким названием жанр по умолчанию пустой
    def test_add_new_book_short_name_has_empty_genre(self):
        collector = BooksCollector()
        book_name = "Короткий"
        collector.add_new_book(book_name)
        assert collector.books_genre[book_name] == ''

#Проверяет, что книга с названием ровно 40 символов успешно добавляется
    def test_add_new_book_exactly_40_chars_is_added(self):
        collector = BooksCollector()
        book_name = "Книга с названием ровно сорок символов!!"  # 40 символов
        collector.add_new_book(book_name)
        assert book_name in collector.books_genre
#Проверяет, что у книги с 40‑символьным названием жанр по умолчанию пустой
    def test_add_new_book_exactly_40_chars_has_empty_genre(self):
        collector = BooksCollector()
        book_name = "Книга с названием ровно сорок символов!!"
        collector.add_new_book(book_name)
        assert collector.books_genre[book_name] == ''

#Проверяет, что книга с пустым названием не добавляется
    def test_add_new_book_empty_name_not_added(self):
        collector = BooksCollector()
        book_name = ""
        collector.add_new_book(book_name)
        assert book_name not in collector.books_genre

#Проверяет, что книга с названием длиннее 40 символов не добавляется
    def test_add_new_book_too_long_name_not_added(self):
        collector = BooksCollector()
        book_name = "A" * 41  # 41 символ
        collector.add_new_book(book_name)
        assert book_name not in collector.books_genre

#Проверяет, что дубликат книги не добавляется (размер словаря не увеличивается)
    def test_add_new_book_duplicate_not_added(self):
        collector = BooksCollector()
        book_name = "Уникальная книга"
        collector.add_new_book(book_name)
        collector.add_new_book(book_name)
        assert len(collector.get_books_genre()) == 1

#Проверяет, что корректный жанр успешно устанавливается для существующей книги
    def test_set_book_genre_valid_genre_is_set(self):
        collector = BooksCollector()
        book_name = "Тестовая книга"
        genre = "Фантастика"
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.get_book_genre(book_name) == genre

#Проверяет, что попытка установить жанр для несуществующей книги не создаёт запись
    def test_set_book_genre_invalid_book_no_effect(self):
        collector = BooksCollector()
        collector.set_book_genre("Несуществующая книга", "Фантастика")
        assert "Несуществующая книга" not in collector.books_genre

#Проверяет, что метод get_book_genre возвращает установленный жанр
    def test_get_book_genre_returns_correct_genre(self):
        collector = BooksCollector()
        book_name = "Книга с жанром"
        genre = "Детективы"
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.get_book_genre(book_name) == genre

#Проверяет, что get_books_with_specific_genre для 'Фантастика' возвращает правильные книги
    def test_get_books_with_specific_genre_fiction_returns_correct_list(self):
        collector = BooksCollector()
        test_books = [f"Книга {i}" for i in range(3)]
        for book in test_books:
            collector.add_new_book(book)
            collector.set_book_genre(book, 'Фантастика')
        result = collector.get_books_with_specific_genre('Фантастика')
        assert sorted(result) == sorted(test_books)

#Проверяет, что get_books_with_specific_genre для 'Мультфильмы' возвращает правильные книги
    def test_get_books_with_specific_genre_cartoons_returns_correct_list(self):
        collector = BooksCollector()
        test_books = [f"Мультфильм {i}" for i in range(2)]
        for book in test_books:
            collector.add_new_book(book)
            collector.set_book_genre(book, 'Мультфильмы')
        result = collector.get_books_with_specific_genre('Мультфильмы')
        assert sorted(result) == sorted(test_books)

#Проверяет, что конкретная детская книга (Винни‑Пух) попадает в список для детей
    def test_get_books_for_children_includes_safe_book(self):
        collector = BooksCollector()
        safe_book = "Винни-Пух"
        collector.add_new_book(safe_book)
        collector.set_book_genre(safe_book, "Мультфильмы")
        children_books = collector.get_books_for_children()
        assert safe_book in children_books

#Проверяет, что взрослая книга (Оно) не попадает в список для детей
    def test_get_books_for_children_excludes_adult_book(self):
        collector = BooksCollector()
        adult_book = "Оно"
        collector.add_new_book(adult_book)
        collector.set_book_genre(adult_book, "Ужасы")
        children_books = collector.get_books_for_children()
        assert adult_book not in children_books

#Проверяет, что книга успешно добавляется в список избранного
    def test_add_book_in_favorites_adds_to_list(self):
        collector = BooksCollector()
        book = "Любимая книга"
        collector.add_new_book(book)
        collector.add_book_in_favorites(book)
        assert book in collector.get_list_of_favorites_books()

#Проверяет, что книга успешно удаляется из списка избранного
    def test_delete_book_from_favorites_removes_from_list(self):
        collector = BooksCollector()
        book = "Любимая книга"
        collector.add_new_book(book)
        collector.add_book_in_favorites(book)
        collector.delete_book_from_favorites(book)
        assert book not in collector.get_list_of_favorites_books()

#Проверяет получение пустого списка избранных книг
    def test_get_list_of_favorites_books_empty(self):
        collector = BooksCollector()
        assert collector.get_list_of_favorites_books() == []
