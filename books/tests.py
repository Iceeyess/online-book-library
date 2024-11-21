import json

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from books.models import Genre, Author, Book, Rent
from users.models import User


class AuthorGenreBookRentTestCase(APITestCase):
    """CRUD User model testing"""

    def setUp(self) -> None:
        # Superuser and simple user creation
        self.superuser_data = dict(username='iceeyes', password='1234', email='admin@test.com', is_staff=True,
                                   is_superuser=True)
        self.simpleuser_data = dict(username='valisy', password='1234', email='vasily@test.com', is_staff=False,
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
                         description='В книге рассказывается о том, как Мастер и Маргарита, две известные истории, '
                                     'встречаются в самом сердце Канады. Мастер отправляется на поиски Маргариты, '
                                     'которая была нашей героиней в прошлом.',
                         genre=[self.genre.id],
                         author=[self.author.id],
                         retail_amount = 100,
                         term=3,
                         publication_book_year=1967)

    def test_crud_genre(self):
        """Testing for CRUD of Genre model"""
        path = reverse('lib:genres-list')
        data = [dict(name='Фантастика'), dict(name='Новелла'), dict(name='Сага')]
        response = []
        for genre in data:
            try:
                print('создаюсь через block try для genres: {0}'.format(genre))
                answer = self.client.post(path=path, data=genre, format='json', headers=self.simple_user_headers)
                self.assertEqual(answer.status_code, status.HTTP_403_FORBIDDEN)
            except:
                raise ValueError('Unexpected status code.')
            else:
                answer = self.client.post(path=path, data=genre, format='json', headers=self.super_user_headers)
                print('создаюсь через block else для genres: {0}'.format(genre))
                response.append(answer)
        for resp in response:
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
            self.assertEqual(len(response), 3)
        ################################################################
        # Test update genre
        genre = Genre.objects.all().first()
        path_update = reverse('lib:genres-detail', kwargs={'pk': genre.id})
        data_update = dict(name='Классика')
        try:
            print(f'обновляюсь через block try для {data_update}')
            response_update = self.client.patch(path=path_update, data=data_update, format='json',
                                                headers=self.simple_user_headers)
            self.assertEqual(response_update.status_code, status.HTTP_403_FORBIDDEN)
        except:
            raise ValueError('Unexpected status code.')
        else:
            response_update = self.client.patch(path=path_update, data=data_update, format='json',
                                                headers=self.super_user_headers)
            print(f'обновляюсь через block else для {data_update}')
            self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        ################################################################
        # Test get genre
        path_get = reverse('lib:genres-list')
        try:
            print(f'Считываю через block try для списка объекта {Genre.__name__}')
            response_get = self.client.get(path=path_get, format='json', headers=self.simple_user_headers)
            self.assertEqual(response_get.status_code, status.HTTP_403_FORBIDDEN)
        except:
            raise ValueError('Unexpected status code.')
        else:
            response_get = self.client.get(path=path_get, format='json', headers=self.super_user_headers)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        ################################################################
        # Test delete genre
        genre_delete = Genre.objects.all().last()
        path_delete = reverse('lib:genres-detail', kwargs={'pk': genre_delete.id})
        try:
            print(f'Удаляю через block try для объекта {genre_delete}')
            response_delete = self.client.delete(path=path_delete, format='json', headers=self.simple_user_headers)
            self.assertEqual(response_delete.status_code, status.HTTP_403_FORBIDDEN)
        except:
            raise ValueError('Unexpected status code.')
        else:
            response_delete = self.client.delete(path=path_delete, format='json', headers=self.super_user_headers)
            print(f'Удаляю {genre_delete} через block else')
            self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

    def test_crud_author(self):
        """Testing for CRUD of Author model"""
        path = reverse('lib:authors-list')
        author = dict(full_name='Стивен Кинг', birth_date='19470921',
                      biography='Стивен Эдвин Кинг (род. 21 сентября 1947, Портленд, Мэн, США) '
                                '— американский писатель, работающий в разнообразных жанрах, включая ужасы, триллер, '
                                'фантастику, фэнтези, мистику, драму, детектив. Получил прозвище «Король ужасов».')
        try:
            print(f'создаюсь через {self.simpleuser} через block try для {author}')
            response = self.client.post(path=path, data=author, format='json', headers=self.simple_user_headers)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        except:
            raise ValueError('Unexpected status code.')
        else:
            response = self.client.post(path=path, data=author, format='json', headers=self.super_user_headers)
            print(f'создаюсь через {self.superuser} через block else для {author}')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        ########################################################################
        # Test update author
        author = Author.objects.all().first()
        path_update = reverse('lib:authors-detail', kwargs={'pk': author.id})
        data_update = dict(full_name='Джордж Оруэлл')
        try:
            print(f'обновляюсь через block try для {data_update}')
            response_update = self.client.patch(path=path_update, data=data_update, format='json',
                                                headers=self.simple_user_headers)
            self.assertEqual(response_update.status_code, status.HTTP_403_FORBIDDEN)
        except:
            raise ValueError('Unexpected status code.')
        else:
            response_update = self.client.patch(path=path_update, data=data_update, format='json',
                                                headers=self.super_user_headers)
            print(f'обновляюсь через block else для {data_update}')
            self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        ##########################################################################
        # Test get author
        path_get = reverse('lib:authors-list')
        try:
            print(f'Считываю через block try для списка объекта {Author.__name__}')
            response_get = self.client.get(path=path_get, format='json', headers=self.simple_user_headers)
            self.assertEqual(response_get.status_code, status.HTTP_403_FORBIDDEN)
        except:
            raise ValueError('Unexpected status code.')
        else:
            response_get = self.client.get(path=path_get, format='json', headers=self.super_user_headers)
            self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        #######################################################################
        # Test delete author
        author_delete = Author.objects.all().last()
        path_delete = reverse('lib:authors-detail', kwargs={'pk': author_delete.id})
        try:
            print(f'Удаляю через block try для объекта {author_delete}')
            response_delete = self.client.delete(path=path_delete, format='json', headers=self.simple_user_headers)
            self.assertEqual(response_delete.status_code, status.HTTP_403_FORBIDDEN)
        except:
            raise ValueError('Unexpected status code.')
        else:
            response_delete = self.client.delete(path=path_delete, format='json', headers=self.super_user_headers)
            print(f'Удаляю {author_delete} через block else')
            self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

    def test_crud_books(self):
        """Testing for CRUD of Book model"""
        path = reverse('lib:books-list')

        try:
            print(f'создаюсь через {self.simpleuser} через block try для {self.book_data}')
            response = self.client.post(path=path, data=self.book_data, format='json', headers=self.simple_user_headers)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        except:
            raise ValueError('Unexpected status code.')
        else:
            response = self.client.post(path=path, data=self.book_data, format='json', headers=self.super_user_headers)
            print(f'создаюсь через {self.superuser} через block else для {self.book_data}')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        ####################################################################################
        # Test update book
        book = Book.objects.all().first()
        path_update = reverse('lib:books-detail', kwargs={'pk': book.id})
        data_update = dict(title='Звездные войны')
        try:
            print(f'обновляюсь через block try для {data_update}')
            response_update = self.client.patch(path=path_update, data=data_update, format='json',
                                                headers=self.simple_user_headers)
            self.assertEqual(response_update.status_code, status.HTTP_403_FORBIDDEN)
        except:
            raise ValueError('Unexpected status code.')
        else:
            response_update = self.client.patch(path=path_update, data=data_update, format='json',
                                                headers=self.super_user_headers)
            print(f'обновляюсь через block else для {data_update}')
            self.assertEqual(response_update.status_code, status.HTTP_200_OK)
            self.assertEqual(json.loads(response_update.content)['title'], data_update.get('title'))
        ################################################################################################
        # Test get book
        path_get = reverse('lib:books-list')
        try:
            print(f'Считываю через block try для списка объекта {Book.__name__}')
            response_get = self.client.get(path=path_get, format='json', headers=self.simple_user_headers)
            self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        except:
            raise ValueError('Unexpected status code.')
        ################################################################################################
        # Test delete book
        book_delete = Book.objects.all().last()
        path_delete = reverse('lib:books-detail', kwargs={'pk': book_delete.id})
        try:
            print(f'Удаляю через block try для объекта {book_delete}')
            response_delete = self.client.delete(path=path_delete, format='json', headers=self.simple_user_headers)
            self.assertEqual(response_delete.status_code, status.HTTP_403_FORBIDDEN)
        except:
            raise ValueError('Unexpected status code.')
        else:
            response_delete = self.client.delete(path=path_delete, format='json', headers=self.super_user_headers)
            print(f'Удаляю {book_delete} через block else')
            self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)


    def test_crud_rent(self):
        """Testing for CRUD of Rent model"""
        book = self.client.post(path=reverse('lib:books-list'), data=self.book_data, headers=self.super_user_headers,
                                format='json')
        rent_path = reverse('lib:rent-list')
        rent_data = dict(books=[json.loads(book.content).get('id')], retail_amount=200, term=1)

        try:
            print(f'Создаю через block try для {rent_data}')
            response = self.client.post(path=rent_path, data=rent_data, headers=self.simple_user_headers, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        except:
            raise ValueError('Unexpected status code.')
        else:
            print(f'Создаю через block else для {rent_data}')
            response = self.client.post(path=rent_path, data=rent_data, headers=self.super_user_headers, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        ##############################################################################################
        #  Test update Rent
        rent = Rent.objects.all().first()
        rent_path_update = reverse('lib:rent-detail', kwargs={'pk': rent.id})
        rent_data_update = dict(retail_amount=300, term=2)
        try:
            print(f'Обновляю через block try для {rent_data_update}')
            response_update = self.client.patch(path=rent_path_update, data=rent_data_update,
                                                headers=self.simple_user_headers, format='json')
            self.assertEqual(response_update.status_code, status.HTTP_403_FORBIDDEN)
        except:
            raise ValueError('Unexpected status code.')
        else:
            print(f'Обновляю через block else для {rent_data_update}')
            response_update = self.client.patch(path=rent_path_update, data=rent_data_update,
                                                headers=self.super_user_headers, format='json')
            self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        ################################################################################################
        #  Test get Rent
        path_get = reverse('lib:rent-list')
        try:
            print(f'Считываю через block try для списка объекта {Rent}')
            response_get = self.client.get(path=path_get, format='json', headers=self.super_user_headers)
            self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        except:
            raise ValueError('Unexpected status code.')
        ################################################################################################
        #  Test return Rent
        rent_return_path = reverse('lib:return-book', kwargs={'pk': rent.id})
        try:
            print(f'Возвращаю книгу назад на полку через block try для списка объекта {Rent}')
            response = self.client.patch(path=rent_return_path, format='json', headers=self.simple_user_headers)
        except:
            raise ValueError('Unexpected status code.')
        else:
            print(f'Не получилось сделать изначально, поскольку пользователь был не создавший запись или суперюзер.'
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
        try:
            print(f'Удаляю через block try для объекта {rent_delete}')
            response_delete = self.client.delete(path=path_delete, format='json', headers=self.simple_user_headers)
            self.assertEqual(response_delete.status_code, status.HTTP_403_FORBIDDEN)
        except:
            raise ValueError('Unexpected status code.')
        else:
            response_delete = self.client.delete(path=path_delete, format='json', headers=self.super_user_headers)
            print(f'Удаляю {rent_delete} через block else')
            self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)