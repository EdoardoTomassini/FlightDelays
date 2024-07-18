from database.DB_connect import DBConnect
from model.airport import Airport
from model.connessione import Connessione


class DAO():

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * 
                    from airports a
                     order by a.AIRPORT desc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(Nmin, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT tmp.ID, tmp.IATA_CODE, count(*) as N
                    from(
                    SELECT a.ID, a.IATA_CODE , f.AIRLINE_ID, count(*) as n
                    FROM flights f, airports a 
                    where a.ID = f.ORIGIN_AIRPORT_ID or a.ID = f.DESTINATION_AIRPORT_ID
                    group by a.ID, f.AIRLINE_ID 
                    ) 
                    as tmp
                    group by tmp.ID
                    HAVING N >= %s"""

        cursor.execute(query, (Nmin ,))

        for row in cursor:
            result.append(idMap[row["ID"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV2(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t1.ORIGIN_AIRPORT_ID, t1.DESTINATION_AIRPORT_ID, COALESCE(t1.n, 0) + COALESCE(t2.n, 0) as peso
                    from (
                    SELECT f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID, count(*) as n
                    FROM flights f 
                    group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID
                    order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID 
                    ) t1
                    left join
                    (SELECT f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID, count(*) as n
                    FROM flights f 
                    group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID
                    order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID
                    ) t2
                    ON t1.ORIGIN_AIRPORT_ID = t2.DESTINATION_AIRPORT_ID
                    and t2.ORIGIN_AIRPORT_ID = t1.DESTINATION_AIRPORT_ID 
                    where t1.ORIGIN_AIRPORT_ID < t1.DESTINATION_AIRPORT_ID or t2.ORIGIN_AIRPORT_ID is null
                    """

        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(idMap[row["ORIGIN_AIRPORT_ID"]],
                          idMap[row["DESTINATION_AIRPORT_ID"]],
                          row["peso"]))

        cursor.close()
        conn.close()
        return result