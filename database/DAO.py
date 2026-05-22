from database.DB_connect import DBConnect
from model.prodotto import Prodotto


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last


    @staticmethod
    def getAllCategories():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select c.category_id, c.category_name 
                    from categories c"""

        cursor.execute(query)

        for row in cursor:
            results.append((row["category_id"], row["category_name"]))

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getAllNodes(category_id):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select p.* 
                    from products p 
                    where p.category_id = %s"""

        cursor.execute(query, (category_id,))

        for row in cursor:
            results.append(Prodotto(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNumVendite(category_id, idMapP, date1, date2):

        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)

        query = """select p.product_id, count(distinct oi.order_id) as num_vendite
                    from products p
                    join order_items oi on p.product_id = oi.product_id 
                    join orders o on oi.order_id = o.order_id 
                    where p.category_id = %s and o.order_date between %s and %s
                    group by p.product_id"""

        cursor.execute(query, (category_id, date1, date2))

        for row in cursor:
            p = idMapP[row["product_id"]]
            p.num_vendite = row["num_vendite"]

        cursor.close()
        conn.close()
        return

    @staticmethod
    def getArchi(category_id, idMapP, date1, date2):

        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)

        res = []

        query = """select distinct p1.product_id as p1, p2.product_id as p2
                    from products p1, products p2, order_items oi1, order_items oi2, orders o1, orders o2
                    where p1.product_id < p2.product_id and oi1.product_id = p1.product_id and oi2.product_id = p2.product_id
                         and oi1.order_id = o1.order_id and oi2.order_id = o2.order_id and p1.category_id = %s
                         and p2.category_id = %s and o1.order_date between %s and %s
                         and o2.order_date between %s and %s"""

        cursor.execute(query, (category_id, category_id, date1, date2, date1, date2))

        for row in cursor:
            res.append((idMapP[row["p1"]], idMapP[row["p2"]]))

        cursor.close()
        conn.close()
        return res


