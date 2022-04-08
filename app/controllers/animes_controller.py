from flask import jsonify, request
from app.models.animes_model import Anime
from psycopg2.errors import UniqueViolation



def create():
    data = request.get_json()
    keys = Anime.check_post_keys(data)

    if keys:
        return keys, 422

    anime = Anime(**data)

    try:
        inserted_anime = anime.create_anime()
    except UniqueViolation:
        return {"error": "anime is already exists"}, 422
    
    serialized_anime = Anime.serialize(inserted_anime)
    serialized_anime['released_date'] = serialized_anime['released_date'].strftime('%d/%m/%Y')

    return serialized_anime, 201


def animes():
    animes = Anime.get_animes()

    if not animes:
        return {"data": []}, 200
    
    serialized_animes = [Anime.serialize(anime) for anime in animes]
    
    for anime in serialized_animes:
        anime['released_date'] = anime['released_date'].strftime('%d/%m/%Y')

    return {"data": serialized_animes}, 200


def anime_by_id(anime_id: str):
    anime = Anime.get_anime_by_id(anime_id)

    if not anime:
        return {"error": "Not found"}, 404

    serialized_anime = Anime.serialize(anime[0])
    serialized_anime['released_date'] = serialized_anime['released_date'].strftime('%d/%m/%Y')

    return {"data": serialized_anime}, 200


def update(anime_id: str):
    data = request.get_json()
    keys = Anime.check_patch_keys(data)

    if keys:
        return keys, 422

    updated_anime = Anime.update_anime(anime_id, data)

    if not updated_anime:
        return {"error": "Not Found"}, 404

    serialized_anime = Anime.serialize(updated_anime)
    serialized_anime['released_date'] = serialized_anime['released_date'].strftime('%d/%m/%Y')

    return serialized_anime, 200



def delete(anime_id: str):
    deleted_anime = Anime.delete_anime(anime_id)

    if not deleted_anime:
        return {"error": "Not Found"}, 404

    serialized_anime = Anime.serialize(deleted_anime)
    serialized_anime['released_date'] = serialized_anime['released_date'].strftime('%d/%m/%Y')

    return serialized_anime, 204

    


