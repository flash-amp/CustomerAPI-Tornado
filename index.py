from tornado import web
import tornado.ioloop
from sqlite_store import *
import json

PORT = 8080


conn = create_conn()
create_table(conn)
delete_customer(conn,1)
val = insert_customer(conn,(1,'as','sd','asas',1234567890,'ds','sas'))
print(val)
select_all_customers(conn)
select_customer_by_id(conn,1)
update_customer(conn,('abdul','azeez','azeez@gmail.com',1234567890,'chennai','tamilnadu',1)) 
select_all_customers(conn)  

# customerList = getCustomers()

class Customers(web.RequestHandler):
    def get(self):
        return self.finish(select_all_customers(conn))
    def post(self):
        d = json.loads(self.request.body)
        
        #print(type(self.request.body))
        return self.write(insert_customer(conn,tuple(d.values())))

class Customer(web.RequestHandler):
    def get(self,id):
        return self.finish(select_customer_by_id(conn,id))

    def put(self,id):
        d = json.loads(self.request.body)
        update_customer(conn,tuple(d.values())+(id,))
        return self.finish(select_customer_by_id(conn,id))

    def delete(self,id):
        return self.write(delete_customer(conn,id))
    # def put(self,id):


if __name__ == "__main__":
    app = web.Application([
        (r"/customers/",Customers),
        (r"/customers/([0-9]+)/",Customer)
    ])

    app.listen(PORT)
    print("im listening ",PORT)
    tornado.ioloop.IOLoop.current().start()

conn.close()