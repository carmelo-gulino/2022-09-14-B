from database.DB_connect import DBConnect
from model.album import Album


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def get_all_albums():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select a.* , avg(t.Milliseconds) d_media
            from album a , track t 
            where t.AlbumId = a.AlbumId 
            group by a.AlbumId"""
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(Album(**row))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_nodes(durata, albums_map):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select a.AlbumId , avg(t.Milliseconds) d_media 
        from album a , track t 
        where a.AlbumId = t.AlbumId  
        group by a.AlbumId 
        having d_media > %s"""
        cursor.execute(query, (durata,))
        result = []
        for row in cursor:
            result.append(albums_map[row['AlbumId']])
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_edge(a1, a2):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct p.PlaylistId 
        from playlisttrack p , playlisttrack p2 , album a , album a2 , track t , track t2 
        where a.AlbumId = t.AlbumId and a2.AlbumId = t2.AlbumId 
        and p.PlaylistId = p2.PlaylistId and t.TrackId = p.TrackId and p2.TrackId = t2.TrackId 
        and a.AlbumId = %s and a2.AlbumId = %s"""
        cursor.execute(query, (a1, a2))
        result = None
        for row in cursor:
            result = row['PlaylistId']
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_n_brani(album):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select count(distinct t.TrackId) n_brani
        from track t , album a 
        where t.AlbumId = a.AlbumId and a.AlbumId = %s"""
        cursor.execute(query, (album,))
        result = None
        for row in cursor:
            result = row['n_brani']
        cursor.close()
        cnx.close()
        return result
