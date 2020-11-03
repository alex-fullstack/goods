import os


def create_tag(user_client):
    result = []
    data = {'name': 'Недвижимость', 'slug': 'realty'}
    result.append(data)
    user_client.post('/api/v1/tags/', data=data)
    data = {'name': 'Услуги', 'slug': 'service'}
    result.append(data)
    user_client.post('/api/v1/tags/', data=data)
    data = {'name': 'Транспорт', 'slug': 'transport'}
    result.append(data)
    user_client.post('/api/v1/tags/', data=data)
    return result


def create_photo(user_client, photo, photo_save_path):
    data = {'image': photo}
    response = user_client.post('/api/v1/photos/', data=data)
    os.remove(photo_save_path)
    return response.json()['id']


def create_advertisements(user_client, photo, photo_save_path):
    tags = create_tag(user_client)
    photo_id = create_photo(user_client, photo, photo_save_path)
    result = []
    data = {'name': 'Коттедж', 'price': 100000, 'tag': [tags[0]['slug'], tags[1]['slug']], 'photo': photo_id,
            'description': 'Куплю коттедж'}
    response = user_client.post('/api/v1/advertisements/', data=data)
    result.append(data)
    data['id'] = response.json()['id']
    data = {'name': 'Авто', 'price': 50000, 'tag': [tags[2]['slug']], 'photo': photo_id,
            'description': 'Куплю машину'}
    response = user_client.post('/api/v1/advertisements/', data=data)
    result.append(data)
    data['id'] = response.json()['id']
    return result, tags, photo_id
