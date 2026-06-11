from main import BooksCollector
import pytest

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_genre, который нам возвращает метод get_books_genre, имеет длину 2
        assert len(collector.get_books_genre()) == 2

    # тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

    @pytest.mark.parametrize("book_name", [
        "Короткий",
        "Книга с названием ровно сорок символов!!"  # 40 символов
    ])
# Проверяет добавление книги с допустимой длиной названия (1–40 символов)
    def test_add_new_book_valid_length(self, book_name):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        assert book_name in collector.books_genre
        assert collector.books_genre[book_name] == ''

    @pytest.mark.parametrize("book_name", [
        "",  # пустая строка
        "A" * 41  # 41 символ
    ])
# Проверяет, что книга с недопустимой длиной названия не добавляется
    def test_add_new_book_invalid_length(self, book_name):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        assert book_name not in collector.books_genre

#Проверяет, что дубликат книги не добавляется
    def test_add_new_book_duplicate(self):
        collector = BooksCollector()
        book_name = "Уникальная книга"
        collector.add_new_book(book_name)
        collector.add_new_book(book_name)
        assert len(collector.get_books_genre()) == 1

# Проверяет установку корректного жанра для книги
    def test_set_book_genre_valid(self):
        collector = BooksCollector()
        book_name = "Тестовая книга"
        genre = "Фантастика"
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.get_book_genre(book_name) == genre

#Проверяет, что нельзя установить жанр для несуществующей книги
    def test_set_book_genre_invalid_book(self):
        collector = BooksCollector()
        collector.set_book_genre("Несуществующая книга", "Фантастика")
        assert "Несуществующая книга" not in collector.books_genre

#Проверяет получение жанра книги по её имени
    def test_get_book_genre(self):
        collector = BooksCollector()
        book_name = "Книга с жанром"
        genre = "Детективы"
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.get_book_genre(book_name) == genre

#Проверяет получение списка книг по определённому жанру
    @pytest.mark.parametrize("genre", ['Фантастика', 'Мультфильмы'])
    def test_get_books_with_specific_genre(self, genre):
        collector = BooksCollector()
        test_books = [f"Книга {i}" for i in range(3)]
        for book in test_books:
            collector.add_new_book(book)
            collector.set_book_genre(book, genre)

        result = collector.get_books_with_specific_genre(genre)
        assert sorted(result) == sorted(test_books)

#Проверяет фильтрацию книг, подходящих детям
    def test_get_books_for_children(self):
        collector = BooksCollector()
        safe_books = ["Винни-Пух", "Ну, погоди!"]
        adult_books = ["Оно", "Молчание ягнят"]

        for book in safe_books:
            collector.add_new_book(book)
            collector.set_book_genre(book, "Мультфильмы")
        for book in adult_books:
            collector.add_new_book(book)
            collector.set_book_genre(book, "Ужасы")

        children_books = collector.get_books_for_children()
        for book in safe_books:
            assert book in children_books
        for book in adult_books:
            assert book not in children_books

#Проверяет операции с избранными книгами: добавление и удаление
    def test_favorites_operations(self):
        collector = BooksCollector()
        book = "Любимая книга"
        collector.add_new_book(book)
        collector.add_book_in_favorites(book)
        assert book in collector.get_list_of_favorites_books()

        collector.delete_book_from_favorites(book)
        assert book not in collector.get_list_of_favorites_books()

#Проверяет получение пустого списка избранных книг
    def test_get_list_of_favorites_books_empty(self):
        collector = BooksCollector()
        assert collector.get_list_of_favorites_books() == []
