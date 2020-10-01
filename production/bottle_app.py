from bottle import get, post, template, request, redirect
import sqlite3
import os

# Are we executing at pythonanywhere?
ON_PYTHONANYWHERE = "PYTHONANYWHERE_DOMAIN" in os.environ
 
# Local vs Pythonanywhere
if ON_PYTHONANYWHERE:
    from bottle import default_app
else:
    from bottle import run, debug

@get('/')
def get_show_list():
    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("select * from todo")
    result = cursor.fetchall()
    cursor.close()
    #return str(result)
    return template("show_list", rows = result)    # creates file, templates are like html

@get("/set_status/<id:int>/<value:int>")
def set_status(id, value):
    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("update todo set status=? where id=?", (value,id))
    connection.commit()
    cursor.close()
    redirect("/")


@get("/new_item")
def get_new_item(): #returns template for a form to fill out
    return template("new_item")

@post("/new_item")
def post_new_item():    
    new_item = request.forms.get("new_item").strip()
    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("insert into todo (task, status) values(?,?)", (new_item, 1))
    #cursor.lastrowid
    connection.commit()
    cursor.close()
    #return "The new item is  [" + new_item + "] ..."
    redirect("/")


@get('/delete_item/<id:int>')   # Guarantees it grabs an int
def get_delete_item(id):
    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("DELETE from todo WHERE id=?", (id,) )    #A touple, ie 10 would be 1 and 0 without it
    connection.commit()
    cursor.close()
    redirect("/")


@get("/update_item/<id:int>")
def get_update_item(id):
    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("select * from todo where id=?", (id,))
    result = cursor.fetchall()
    cursor.close()
    return template("update_item", row=result[0])

@post("/update_item")
def post_update_item():    
    id = int(request.forms.get("id").strip())
    updated_item = request.forms.get("updated_item").strip()
    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("update todo set task=? where id=?", (updated_item, id))
    connection.commit()
    cursor.close()
    redirect("/")

if ON_PYTHONANYWHERE:
     application = default_app()
else:
    debug(True)
    run(host='localhost', port=8080)