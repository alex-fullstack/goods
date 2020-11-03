import pytest

from tests.common import create_tag, create_photo, create_advertisements


class TestAdvertisementAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_advertisement(self, user_client, photo, photo_save_path):
        tags = create_tag(user_client)
        photo_id = create_photo(user_client, photo, photo_save_path)
        data = {}
        response = user_client.post('/api/v1/advertisements/', data=data)
        assert response.status_code == 400, \
            'Проверьте, что при POST запросе `/api/v1/advertisements/` с не правильными данными возвращает статус 400'
        data = {'name': 'Коттедж', 'price': 100000, 'tag': [tags[0]['slug'], tags[1]['slug']], 'photo': photo_id,
                'description': 'Куплю коттедж'}
        response = user_client.post('/api/v1/advertisements/', data=data)
        assert response.status_code == 201, \
            'Проверьте, что при POST запросе `/api/v1/advertisements/` с правильными данными возвращает статус 201'
        response = user_client.get('/api/v1/advertisements/')
        assert response.status_code == 200, \
            'Проверьте, что при GET запросе `/api/v1/advertisements/` возвращает статус 200'
        data = response.json()
        assert 'count' in data, \
            'Проверьте, что при GET запросе `/api/v1/advertisements/` возвращаете данные с пагинацией. ' \
            'Не найден параметр `count`'
        assert 'next' in data, \
            'Проверьте, что при GET запросе `/api/v1/advertisements/` возвращаете данные с пагинацией. ' \
            'Не найден параметр `next`'
        assert 'previous' in data, \
            'Проверьте, что при GET запросе `/api/v1/advertisements/` возвращаете данные с пагинацией. ' \
            'Не найден параметр `previous`'
        assert 'results' in data, \
            'Проверьте, что при GET запросе `/api/v1/advertisements/` возвращаете данные с пагинацией. ' \
            'Не найден параметр `results`'
        assert data['count'] == 1, \
            'Проверьте, что при GET запросе `/api/v1/advertisements/` возвращаете данные с пагинацией. ' \
            'Значение параметра `count` не правильное'
        assert type(data['results']) == list, \
            'Проверьте, что при GET запросе `/api/v1/advertisements/` возвращаете данные с пагинацией. ' \
            'Тип параметра `results` должен быть список'
        assert len(data['results']) == 1, \
            'Проверьте, что при GET запросе `/api/v1/advertisements` возвращаете данные с пагинацией. ' \
            'Значение параметра `results` не правильное'
        if data['results'][0].get('name') == 'Коттедж':
            advertisement = data['results'][0]
        else:
            assert False, \
                'Проверьте, что при GET запросе `/api/v1/advertisements/` возвращаете данные с пагинацией. ' \
                'Значение параметра `results` неправильное, `name` не найдено или не сохранилось при POST запросе.'
        assert advertisement.get('description') == 'Куплю коттедж', \
            'Проверьте, что при GET запросе `/api/v1/advertisements/` возвращаете данные с пагинацией. ' \
            'Значение параметра `results` неправильное, значение `description` неправильное ' \
            'или не сохранилось при POST запросе.'
        assert tags[0] in advertisement.get('tag', []) and tags[1] in advertisement.get('tag', []), \
            'Проверьте, что при GET запросе `/api/v1/advertisements/` возвращаете данные с пагинацией. ' \
            'Значение параметра `results` неправильное, значение `tag` неправильное ' \
            'или не сохранилось при POST запросе.'
        assert advertisement.get('price') == '100000.00', \
            'Проверьте, что при GET запросе `/api/v1/advertisements/` возвращаете данные с пагинацией. ' \
            'Значение параметра `results` неправильное, значение `price` неправильное ' \
            'или не сохранилось при POST запросе.'
        assert type(advertisement.get('id')) == int, \
            'Проверьте, что при GET запросе `/api/v1/advertisements/` возвращаете данные с пагинацией. ' \
            'Значение параметра `results` неправильное, значение `id` нет или не является целым числом.'
        data = {'name': 'Авто', 'price': 50000, 'tag': [tags[2]['slug']], 'photo': photo_id,
                'description': 'Куплю машину'}
        user_client.post('/api/v1/advertisements/', data=data)
        response = user_client.get(f'/api/v1/advertisements/?tag={tags[2]["slug"]}')
        data = response.json()
        assert len(data['results']) == 1, \
            'Проверьте, что при GET запросе `/api/v1/advertisements/` фильтуется по `tag` параметру `slug` тэга'
        response = user_client.get(f'/api/v1/advertisements/?price__min=40000&price__max=60000')
        data = response.json()
        assert len(data['results']) == 1, \
            'Проверьте, что при GET запросе `/api/v1/advertisements/` фильтуется по `price`'

    @pytest.mark.django_db(transaction=True)
    def test_02_advertisement_detail(self, user_client, photo, photo_save_path):
        advertisements, tags, photo_id = create_advertisements(user_client, photo, photo_save_path)
        response = user_client.get(f'/api/v1/advertisements/{advertisements[0]["id"]}/')
        assert response.status_code != 404, \
            'Страница `/api/v1/advertisements/{advertisement_id}/` не найдена, проверьте этот адрес в *urls.py*'
        assert response.status_code == 200, \
            'Проверьте, что при GET запросе `/api/v1/advertisements/{advertisement_id}/` ' \
            'без токена авторизации возвращается статус 200'
        data = response.json()
        assert type(data.get('id')) == int, \
            'Проверьте, что при GET запросе `/api/v1/advertisements/{advertisement_id}/` возвращаете данные объекта. ' \
            'Значение `id` нет или не является целым числом.'
        assert data.get('tag')[0] in tags and data.get('tag')[1] in tags, \
            'Проверьте, что при GET запросе `/api/v1/advertisements/{advertisement_id}/` возвращаете данные объекта. ' \
            'Значение `tag` неправильное.'
        assert data.get('name') == advertisements[0]['name'], \
            'Проверьте, что при GET запросе `/api/v1/advertisements/{advertisement_id}/` возвращаете данные объекта. ' \
            'Значение `name` неправильное.'
        data = {
            'name': 'Новое название',
            'tag': [tags[2]['slug']]
        }
        response = user_client.patch(f'/api/v1/advertisements/{advertisements[0]["id"]}/', data=data)
        assert response.status_code == 200, \
            'Проверьте, что при PATCH запросе `/api/v1/advertisements/{advertisement_id}/` возвращается статус 200'
        data = response.json()
        assert data.get('name') == 'Новое название', \
            'Проверьте, что при PATCH запросе `/api/v1/advertisements/{advertisement_id}/`' \
            ' возвращаете данные объекта. Значение `name` изменено.'
        assert data.get('tag')[0] in tags, \
            'Проверьте, что при PATCH запросе `/api/v1/advertisements/{advertisement_id}/`' \
            ' изменяете значение `tag`.'
        response = user_client.delete(f'/api/v1/advertisements/{advertisements[0]["id"]}/')
        assert response.status_code == 204, \
            'Проверьте, что при DELETE запросе `/api/v1/advertisements/{advertisement_id}/` возвращаете статус 204'
        response = user_client.get('/api/v1/advertisements/')
        test_data = response.json()['results']
        assert len(test_data) == len(advertisements) - 1, \
            'Проверьте, что при DELETE запросе `/api/v1/advertisements/{advertisement_id}/` удаляете объект'

