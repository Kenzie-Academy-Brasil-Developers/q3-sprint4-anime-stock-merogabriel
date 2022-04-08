import psycopg2
from app.models import DatabaseConnector
from psycopg2 import sql


class Anime(DatabaseConnector):
    anime_columns = [
        "id",
        "anime",
        "released_date",
        "seasons"
    ]


    def __init__(self, **kwargs):
        self.anime = kwargs["anime"]
        self.released_date = kwargs["released_date"]
        self.seasons = kwargs["seasons"]


    @classmethod
    def serialize(cls, data: tuple):
        return dict(zip(cls.anime_columns, data))

    
    def create_anime(self):
        self.create_table()
        self.get_conn_cur()

        query = """
            INSERT INTO animes
                (anime, released_date, seasons)
            VALUES
                (%s, %s, %s)
            RETURNING *;
        """

        query_values = tuple(self.__dict__.values())

        
        self.cur.execute(query, query_values)

        self.conn.commit()

        inserted_anime = self.cur.fetchone()

        self.cur.close() 
        self.conn.close()

        return inserted_anime
        
        
    
    @classmethod
    def get_animes(cls):
            cls.create_table()
            cls.get_conn_cur()

            query = "SELECT * FROM animes;"

            cls.cur.execute(query)

            animes = cls.cur.fetchall()

            cls.cur.close()
            cls.conn.close()

            return animes


    @classmethod
    def get_anime_by_id(cls, anime_id: str):
        cls.create_table()
        cls.get_conn_cur()

        sql_anime_id = sql.Literal(anime_id)

        query = sql.SQL("""
            select * from animes where id = {id}
        """).format(id=sql_anime_id)

        cls.cur.execute(query)

        anime = cls.cur.fetchall()

        cls.cur.close()
        cls.conn.close()

        return anime        


    @classmethod
    def update_anime(cls, anime_id: str, payload: dict):
        cls.get_conn_cur()
        
        columns = [sql.Identifier(key) for key in payload.keys()]
        values = [sql.Literal(value) for value in payload.values()]
        sql_anime_id = sql.Literal(anime_id)

        query = sql.SQL(
            """
            UPDATE
                animes
            SET
                ({columns}) = ROW({values})
            WHERE
                id = {id}
            RETURNING *;
            """
        ).format(
            id=sql_anime_id,
            columns=sql.SQL(",").join(columns),
            values=sql.SQL(",").join(values),
        )

        cls.cur.execute(query)

        updated_anime = cls.cur.fetchone()

        cls.commit_and_close()

        return updated_anime


    @classmethod
    def delete_anime(cls, anime_id: str):
        cls.get_conn_cur()

        sql_anime_id = sql.Literal(anime_id)

        
        query = sql.SQL("""DELETE FROM animes WHERE id = {id}
        RETURNING *;
        """).format(id=sql_anime_id)

        cls.cur.execute(query)

        cls.conn.commit()

        deleted_anime = cls.cur.fetchone()  

        cls.cur.close()
        cls.conn.close()

        return deleted_anime


    @classmethod
    def check_post_keys(cls, payload: dict):
        anime_columns = [
        "anime",
        "released_date",
        "seasons"
        ]
        
        keys = [key for key in payload.keys()]

        if keys == anime_columns:
            return False    

        wrong_keys = [key for key in payload.keys() if key not in anime_columns]

        return {
            "available_keys": anime_columns,
            "wrong_keys_sended": wrong_keys
        }

    
    @classmethod
    def check_patch_keys(cls, payload: dict):
        anime_columns = [
        "anime",
        "released_date",
        "seasons"
        ]

        wrong_keys = [key for key in payload.keys() if key not in anime_columns]

        if not wrong_keys:
            return False

        return {
            "available_keys": anime_columns,
            "wrong_keys_sended": wrong_keys
        }

