import pytest, os

from tests.common import create_photo


class TestPhotoAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_photo(self, user_client, photo, photo_save_path):
        data = {}
        response = user_client.post('/api/v1/photos/', data=data)
        assert response.status_code == 400, \
            'Проверьте, что при POST запросе `/api/v1/photos/` с не правильными данными возвращает статус 400'
        data = {'image': photo}
        response = user_client.post('/api/v1/photos/', data=data)
        os.remove(photo_save_path)
        assert response.status_code == 201, \
            'Проверьте, что при POST запросе `/api/v1/photos/` с правильными данными возвращает статус 201'
        response = user_client.get('/api/v1/photos/')
        assert response.status_code == 200, \
            'Проверьте, что при GET запросе `/api/v1/photos/` возвращает статус 200'
        data = response.json()
        assert 'count' in data, \
            'Проверьте, что при GET запросе `/api/v1/photos/` возвращаете данные с пагинацией. ' \
            'Не найден параметр `count`'
        assert 'next' in data, \
            'Проверьте, что при GET запросе `/api/v1/photos/` возвращаете данные с пагинацией. ' \
            'Не найден параметр `next`'
        assert 'previous' in data, \
            'Проверьте, что при GET запросе `/api/v1/photos/` возвращаете данные с пагинацией. ' \
            'Не найден параметр `previous`'
        assert 'results' in data, \
            'Проверьте, что при GET запросе `/api/v1/photos/` возвращаете данные с пагинацией. ' \
            'Не найден параметр `results`'
        assert data['count'] == 1, \
            'Проверьте, что при GET запросе `/api/v1/photos/` возвращаете данные с пагинацией. ' \
            'Значение параметра `count` не правильное'
        assert type(data['results']) == list, \
            'Проверьте, что при GET запросе `/api/v1/photos/` возвращаете данные с пагинацией. ' \
            'Тип параметра `results` должен быть список'
        assert len(data['results']) == 1, \
            'Проверьте, что при GET запросе `/api/v1/photos/` возвращаете данные с пагинацией. ' \
            'Значение параметра `results` не правильное'
        assert f'http://testserver/{photo_save_path}' in data['results'][0].values(), \
            'Проверьте, что при GET запросе `/api/v1/photos/` возвращаете данные с пагинацией. ' \
            'Значение параметра `results` не правильное'

    @pytest.mark.django_db(transaction=True)
    def test_02_photos_delete(self, user_client, photo, photo_save_path):
        photo_id = create_photo(user_client, photo, photo_save_path)
        response = user_client.delete(f'/api/v1/photos/{photo_id}/')
        assert response.status_code == 204, \
            'Проверьте, что при DELETE запросе `/api/v1/photos/{id}/` возвращаете статус 204'
        response = user_client.get('/api/v1/photos/')
        test_data = response.json()['results']
        assert len(test_data) == 0, \
            'Проверьте, что при DELETE запросе `/api/v1/photos/{id}/` удаляете данные'
        response = user_client.patch(f'/api/v1/photos/{photo_id}/')
        assert response.status_code == 405, \
            'Проверьте, что при PATCH запросе `/api/v1/photos/{id}/` возвращаете статус 405'
        response = user_client.get(f'/api/v1/photos/{photo_id}/')
        assert response.status_code == 405, \
            'Проверьте, что при GET запросе `/api/v1/photos/{id}/` возвращаете статус 405'
