import uuid
from settings import test_settings

TEST_DATA = {
    'id': str(uuid.uuid4()),
    'imdb_rating': 8.5,
    'genre': ['Action', 'Sci-Fi'],
    'title': 'The Star',
    'description': 'New World',
    'director': {'id': 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95', 'name': 'Ann'},
    'actors_names': ['Ann', 'Bob'],
    'writers_names': ['Ben', 'Howard'],
    'actors': [
        {'id': 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95', 'name': 'Ann'},
        {'id': 'fb111f22-121e-44a7-b78f-b19191810fbf', 'name': 'Bob'}
    ],
    'writers': [
        {'id': 'caf76c67-c0fe-477e-8766-3ab3ff2574b5', 'name': 'Ben'},
        {'id': 'b45bd7bc-2e16-46d5-b125-983d356768c6', 'name': 'Howard'}
    ]
}

TEST_DATA_GENRE = {
    'id': 'adb5ffa8-7dbc-4088-8e5f-44311680a75c',
    'name': 'Action',
    'description': 'description'
}

PARAMETERS = {
    'phrase': [
        (
            {'films/search': 'Star'},
            {'status': 200, 'length': 6}
        ),
        (
            {'films/search': 'Roger'},
            {'status': 200, 'length': 4}
        ),
        (
            {'films/search': 'Philips'},
            {'status': 200, 'length': 1}
        )
    ],
    'limit': [
        (
            {'films/search': 'The Star'},
            {'status': 200, 'length': 10}
        ),
        (
            {'films/search': 'Marched Potato'},
            {'status': 200, 'length': 0}
        )
    ],
    'validation': [
        (
            {'films/search': 'The Star'},
            {'status': 200, 'length': 3}
        ),
    ],
    'existing_film_id': [
        (
            test_settings.es_id_field,
            {'status': 200, 'answer': test_settings.es_id_field}
        )
    ],
    'not_existing_film_id': [
        (
            '123e4567-e89b-12d3-a456-426655440000',
            {'status': 404, 'answer': {'detail': 'film not found'}}
        )
    ],
    'limit_genres': [
        (
            {'genres': ''},
            {'status': 200, 'length': 10}
        )
    ],
    'search_genre': [
        (
            {
                'id': 'adb5ffa8-7dbc-4088-8e5f-44311680a75c',
                'genres': '',
            },
            {
                'status': 200,
                'length': 1,
                'name': 'Action'
            }
        )
    ]
}
