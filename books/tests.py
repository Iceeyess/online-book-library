import json

from rest_framework.exceptions import APIException
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from books.models import Genre, Author, Book, Rent
from users.models import User


class AuthorGenreBookRentTestCase(APITestCase):
    """CRUD User model testing"""

    def get_http_response_for_my_tests(self, method, path, headers1, headers2, expected_status_1,
                                       expected_status_2, data={}, format='json'):
        """This method gets parameters for ClientAPI requests and makes verification for permissions allowed
        for simple or superuser, in the block try there are headers provided for specific user and waiting for
        answer provided in the 'answer'.
        Parameters description:
        method - The APIClient HTTP method
        path - path for APIClient HTTP method
        headers1 - header1 for APIClient HTTP method for 'try' block
        headers2 - header2 for APIClient HTTP method for 'else' block
        expected_status_1 - expected_status_1 for APIClient HTTP method for 'try' block
        expected_status_1 - expected_status_1 for APIClient HTTP method for 'else' block
        data - data for APIClient HTTP method
        format - format for APIClient HTTP method"""

        try:
            print(f'Обрабатываю через block try для {data if data else dict(data="no data found")}')
            answer = method(path=path, data=data, format='json', headers=headers1)
            self.assertEqual(answer.status_code, expected_status_1)
        except AssertionError:
            raise ValueError('Unexpected status code.')
        else:
            answer = method(path=path, data=data, format='json', headers=headers2)
            print(f'Обрабатываю через block else для {data if data else dict(data="no data found")}')
            self.assertEqual(answer.status_code, expected_status_2)
        return answer

    def setUp(self) -> None:
        # Superuser and simple user creation
        self.superuser_data = dict(username='iceeyes', password='1234', email='admin@test.com', is_staff=True,
                                   is_superuser=True)
        self.simpleuser_data = dict(username='vasily', password='1234', email='vasily@test.com', is_staff=False,
                                    is_superuser=False)
        self.client = APIClient()
        self.superuser = User.objects.create_user(**self.superuser_data)
        self.simpleuser = User.objects.create_user(**self.simpleuser_data)
        # Both users authorization
        auth_url = reverse('users:token-obtain-pair')
        self.super_user_token = self.client.post(path=auth_url, data={
            'email': self.superuser_data['email'],
            'password': self.superuser_data['password']
        }).data.get('access')
        self.simple_user_token = self.client.post(path=auth_url, data={
            'email': self.simpleuser_data['email'],
            'password': self.simpleuser_data['password']
        }).data.get('access')
        self.super_user_headers = {
            'Authorization': f'Token {self.super_user_token}'
        }
        self.simple_user_headers = {
            'Authorization': f'Token {self.simple_user_token}'
        }
        self.genre = Genre.objects.create(name='Роман')
        self.author_dict_data = dict(full_name='Михаил Афанасьевич Булгаков', birth_date='19400310',
                                     biography="Русский писатель советского периода, врач, драматург, театральный "
                                               "режиссёр и актёр. Родился 3 (15)")
        self.author = Author.objects.create(**self.author_dict_data)
        self.book_data = dict(title='Мастер и Маргарита', publication_date='19670714',
                              description='В книге рассказывается о том, как Мастер и Маргарита, две известные истории,'
                                          'встречаются в самом сердце Канады. Мастер отправляется на поиски Маргариты, '
                                          'которая была нашей героиней в прошлом.',
                              genre=[self.genre.id],
                              author=[self.author.id],
                              retail_amount=100,
                              term=3,
                              publication_book_year=1967)

    def test_crud_genre(self):
        """Testing for CRUD of Genre model"""
        path = reverse('lib:genres-list')
        data = [dict(name='Фантастика'), dict(name='Новелла'), dict(name='Сага')]
        for genre in data:
            self.get_http_response_for_my_tests(self.client.post, path, self.simple_user_headers,
                                                self.super_user_headers, status.HTTP_403_FORBIDDEN,
                                                status.HTTP_201_CREATED,
                                                data=genre)

        ################################################################
        # Test update genre
        genre = Genre.objects.all().first()
        path_update = reverse('lib:genres-detail', kwargs={'pk': genre.id})
        data_update = dict(name='Классика')
        self.get_http_response_for_my_tests(self.client.patch, path_update, self.simple_user_headers,
                                            self.super_user_headers, status.HTTP_403_FORBIDDEN, status.HTTP_200_OK,
                                            data=data_update)
        ################################################################
        # Test get genre
        path_get = reverse('lib:genres-list')
        self.get_http_response_for_my_tests(self.client.get, path_get, self.simple_user_headers,
                                            self.super_user_headers, status.HTTP_403_FORBIDDEN, status.HTTP_200_OK)
        ################################################################
        # Test delete genre
        genre_delete = Genre.objects.all().last()
        path_delete = reverse('lib:genres-detail', kwargs={'pk': genre_delete.id})
        self.get_http_response_for_my_tests(self.client.delete, path_delete, self.simple_user_headers,
                                            self.super_user_headers, status.HTTP_403_FORBIDDEN,
                                            status.HTTP_204_NO_CONTENT)

    def test_crud_author(self):
        """Testing for CRUD of Author model"""
        path = reverse('lib:authors-list')
        author = dict(full_name='Стивен Кинг', birth_date='19470921',
                      biography='Стивен Эдвин Кинг (род. 21 сентября 1947, Портленд, Мэн, США) '
                                '— американский писатель, работающий в разнообразных жанрах, включая ужасы, триллер, '
                                'фантастику, фэнтези, мистику, драму, детектив. Получил прозвище «Король ужасов».')
        self.get_http_response_for_my_tests(self.client.post, path, self.simple_user_headers,
                                            self.super_user_headers, status.HTTP_403_FORBIDDEN, status.HTTP_201_CREATED,
                                            data=author)
        ########################################################################
        # Test update author
        author = Author.objects.all().first()
        path_update = reverse('lib:authors-detail', kwargs={'pk': author.id})
        data_update = dict(full_name='Джордж Оруэлл')
        self.get_http_response_for_my_tests(self.client.patch, path_update, self.simple_user_headers,
                                            self.super_user_headers, status.HTTP_403_FORBIDDEN, status.HTTP_200_OK,
                                            data=data_update)
        ##########################################################################
        # Test get author
        path_get = reverse('lib:authors-list')
        self.get_http_response_for_my_tests(self.client.get, path_get, self.simple_user_headers,
                                            self.super_user_headers, status.HTTP_403_FORBIDDEN, status.HTTP_200_OK)
        #######################################################################
        # Test delete author
        author_delete = Author.objects.all().last()
        path_delete = reverse('lib:authors-detail', kwargs={'pk': author_delete.id})
        self.get_http_response_for_my_tests(self.client.delete, path_delete, self.simple_user_headers,
                                            self.super_user_headers, status.HTTP_403_FORBIDDEN,
                                            status.HTTP_204_NO_CONTENT)

    def test_crud_books(self):
        """Testing for CRUD of Book model"""
        path = reverse('lib:books-list')
        self.get_http_response_for_my_tests(self.client.post, path, self.simple_user_headers,
                                            self.super_user_headers, status.HTTP_403_FORBIDDEN, status.HTTP_201_CREATED,
                                            data=self.book_data)
        ####################################################################################
        # Test update book
        book = Book.objects.all().first()
        path_update = reverse('lib:books-detail', kwargs={'pk': book.id})
        data_update = dict(title='Звездные войны')
        response_update = self.get_http_response_for_my_tests(self.client.patch, path_update, self.simple_user_headers,
                                                              self.super_user_headers, status.HTTP_403_FORBIDDEN,
                                                              status.HTTP_200_OK,
                                                              data=data_update)
        self.assertEqual(json.loads(response_update.content)['title'], data_update.get('title'))
        ################################################################################################
        # Test get book
        path_get = reverse('lib:books-list')
        response_get = self.get_http_response_for_my_tests(self.client.get, path_get, self.simple_user_headers,
                                                               self.simple_user_headers, status.HTTP_200_OK,
                                                               status.HTTP_200_OK)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        ################################################################################################
        # Test delete book
        book_delete = Book.objects.all().last()
        path_delete = reverse('lib:books-detail', kwargs={'pk': book_delete.id})
        self.get_http_response_for_my_tests(self.client.delete, path_delete, self.simple_user_headers,
                                            self.super_user_headers, status.HTTP_403_FORBIDDEN,
                                            status.HTTP_204_NO_CONTENT)

    def test_crud_rent(self):
        """Testing for CRUD of Rent model"""
        book = self.client.post(path=reverse('lib:books-list'), data=self.book_data, headers=self.super_user_headers,
                                format='json')
        rent_path = reverse('lib:rent-list')
        rent_data = dict(books=[json.loads(book.content).get('id')], retail_amount=200, term=1)
        self.get_http_response_for_my_tests(self.client.post, rent_path, self.simple_user_headers,
                                            self.super_user_headers, status.HTTP_403_FORBIDDEN,
                                            status.HTTP_201_CREATED, data=rent_data)
        ##############################################################################################
        #  Test update Rent
        rent = Rent.objects.all().first()
        rent_path_update = reverse('lib:rent-detail', kwargs={'pk': rent.id})
        rent_data_update = dict(retail_amount=300, term=2)
        self.get_http_response_for_my_tests(self.client.patch, rent_path_update, self.simple_user_headers,
                                            self.super_user_headers, status.HTTP_403_FORBIDDEN,
                                            status.HTTP_200_OK, data=rent_data_update)
        ################################################################################################
        #  Test get Rent
        path_get = reverse('lib:rent-list')
        try:
            response_get = self.get_http_response_for_my_tests(self.client.get, path_get, self.simple_user_headers,
                                                               self.super_user_headers, status.HTTP_403_FORBIDDEN,
                                                               status.HTTP_200_OK)
        except AssertionError:
            print(f'Считываю через block try для списка объекта {Rent.__name__}')
            response_get = self.client.get(path=path_get, format='json', headers=self.super_user_headers)
        finally:
            self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        ################################################################################################
        #  Test return Rent
        rent_return_path = reverse('lib:return-book', kwargs={'pk': rent.id})
        try:
            print(f'Возвращаю книгу назад на полку через block try для списка объекта {Rent}')
            response = self.client.patch(path=rent_return_path, format='json', headers=self.simple_user_headers)
        except AssertionError:
            raise ValueError('Unexpected status code.')
        else:
            print(f'Не получилось сделать изначально, поскольку пользователь являлся не создавший запись или суперюзер.'
                  f'Возвращаю книгу назад на полку через block else для списка объекта {Rent}')
            response = self.client.patch(path=rent_return_path, format='json', headers=self.super_user_headers)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            response_dictionary = json.loads(response.content)
            self.assertTrue(response_dictionary.get('are_books_returned'))
            for book in Book.objects.all():
                self.assertTrue(book.is_available)
        ################################################################################################
        #  Test delete Rent
        rent_delete = Rent.objects.all().last()
        path_delete = reverse('lib:rent-detail', kwargs={'pk': rent_delete.id})
        self.get_http_response_for_my_tests(self.client.delete, path_delete, self.simple_user_headers,
                                            self.super_user_headers, status.HTTP_403_FORBIDDEN,
                                            status.HTTP_204_NO_CONTENT)
