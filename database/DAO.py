from database.DB_connect import DBConnect
from model.product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAnni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct YEAR(s.date) FROM go_daily_sales s"

        cursor.execute(query)

        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getColors():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct    Product_color FROM  go_products  "

        cursor.execute(query)

        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getProductsFromColor(color):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "select distinct  * from go_products p where p.Product_color=%s"

        cursor.execute(query, (color,))

        for row in cursor:
            result.append(Product(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllProdotti():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "select   * from go_products p"

        cursor.execute(query, )

        for row in cursor:
            result.append(Product(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPeso(numP1, numP2, anno):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []
        query = """SELECT count(distinct s2.`Date`) as peso
                    FROM go_daily_sales s, go_daily_sales s2 
                    where s.product_number=%s 
                    and s2.Product_number = %s
                        and s.date=s2.date 
                        and s.Retailer_code=s2.Retailer_code 
                        and YEAR(s.date)=%s"""

        cursor.execute(query, (numP1, numP2, anno))

        for row in cursor:
            result.append(row["peso"])

        cursor.close()
        conn.close()


        return result