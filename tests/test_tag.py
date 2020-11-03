import pytest

from tests.common import create_tag


class TestTagAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_tag(self, user_client):
        data = {}
        response = user_client.post('/api/v1/tags/', data=data)
        assert response.status_code == 400, \
            'Проверьте, что при POST запросе `/api/v1/tags/` с не правильными данными возвращает статус 400'
        data = {'name': 'Недвижимость', 'slug': 'realty'}
        response = user_client.post('/api/v1/tags/', data=data)
        assert response.status_code == 201, \
            'Проверьте, что при POST запросе `/api/v1/tags/` с правильными данными возвращает статус 201'
        data = {'name': 'Услуги', 'slug': 'realty'}
        response = user_client.post('/api/v1/tags/', data=data)
        assert response.status_code == 400, \
            'Проверьте, что при POST запросе `/api/v1/tags/` нельзя создать 2 категории с одинаковым `slug`'
        data = {'name': 'Транспорт', 'slug': 'transport'}
        response = user_client.post('/api/v1/tags/', data=data)
        assert response.status_code == 201, \
            'Проверьте, что при POST запросе `/api/v1/tags/` с правильными данными возвращает статус 201'
        response = user_client.get('/api/v1/tags/')
        assert response.status_code == 200, \
            'Проверьте, что при GET запросе `/api/v1/tags/` возвращает статус 200'
        data = response.json()
        assert 'count' in data, \
            'Проверьте, что при GET запросе `/api/v1/tags/` возвращаете данные с пагинацией. ' \
            'Не найден параметр `count`'
        assert 'next' in data, \
            'Проверьте, что при GET запросе `/api/v1/tags/` возвращаете данные с пагинацией. ' \
            'Не найден параметр `next`'
        assert 'previous' in data, \
            'Проверьте, что при GET запросе `/api/v1/tags/` возвращаете данные с пагинацией. ' \
            'Не найден параметр `previous`'
        assert 'results' in data, \
            'Проверьте, что при GET запросе `/api/v1/tags/` возвращаете данные с пагинацией. ' \
            'Не найден параметр `results`'
        assert data['count'] == 2, \
            'Проверьте, что при GET запросе `/api/v1/tags/` возвращаете данные с пагинацией. ' \
            'Значение параметра `count` не правильное'
        assert type(data['results']) == list, \
            'Проверьте, что при GET запросе `/api/v1/tags/` возвращаете данные с пагинацией. ' \
            'Тип параметра `results` должен быть список'
        assert len(data['results']) == 2, \
            'Проверьте, что при GET запросе `/api/v1/tags/` возвращаете данные с пагинацией. ' \
            'Значение параметра `results` не правильное'
        assert {'name': 'Недвижимость', 'slug': 'realty'} in data['results'], \
            'Проверьте, что при GET запросе `/api/v1/tags/` возвращаете данные с пагинацией. ' \
            'Значение параметра `results` не правильное'

    @pytest.mark.django_db(transaction=True)
    def test_02_tags_delete(self, user_client):
        tags = create_tag(user_client)
        response = user_client.delete(f'/api/v1/tags/{tags[0]["slug"]}/')
        assert response.status_code == 204, \
            'Проверьте, что при DELETE запросе `/api/v1/tags/{slug}/` возвращаете статус 204'
        response = user_client.get('/api/v1/tags/')
        test_data = response.json()['results']
        assert len(test_data) == len(tags) - 1, \
            'Проверьте, что при DELETE запросе `/api/v1/tags/{slug}/` удаляете категорию '
        response = user_client.get(f'/api/v1/tags/{tags[0]["slug"]}/')
        assert response.status_code == 405, \
            'Проверьте, что при GET запросе `/api/v1/tags/{slug}/` возвращаете статус 405'
        response = user_client.patch(f'/api/v1/tags/{tags[0]["slug"]}/')
        assert response.status_code == 405, \
            'Проверьте, что при PATCH запросе `/api/v1/tags/{slug}/` возвращаете статус 405'

