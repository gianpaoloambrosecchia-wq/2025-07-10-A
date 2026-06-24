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

        # Considero prima e ultima data del database
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

        query = """select p.product_id, sum(oi.quantity) as num_vendite
                    from products p
                    join order_items oi on p.product_id = oi.product_id 
                    join orders o on oi.order_id = o.order_id 
                    where p.category_id = %s and o.order_date between %s and %s
                    group by p.product_id"""

        cursor.execute(query, (category_id, date1, date2))

        for row in cursor:
            if row["product_id"] in idMapP:
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

    # Oppure volendo fare tutto direttamente su sql
    """select t1.product_id, t2.product_id, t1.num_ven as numt1, t2.num_ven as numt2, t1.num_ven+t2.num_ven as peso
       from (select p.product_id, count(*) as num_ven
       from products p, order_items oi, orders o
       where o.order_id = oi.order_id and oi.product_id = p.product_id and
             o.order_date between %s and %s and p.category_id = %s
       group by p.product_id) t1, 
       (select p.product_id, count(*) as num_ven
       from products p, order_items oi, orders o
       where o.order_id = oi.order_id and oi.product_id = p.product_id and
             o.order_date between %s and %s and p.category_id = %s
       group by p.product_id) t2
       where t1.product_id <> t2.product_id and t1.num_ven = t2.num_ven
       """

    # L'ultima riga della query mi permette di considerare due prodotti diversi
    # con l'arco che va da quello con num vendite maggiore a quello con num vendite
    # minore (il segno uguale sarà valido in entrambi i versi, poichè l0uguaglianza
    # sarà verificata sia da A verso B sia da B verso A


