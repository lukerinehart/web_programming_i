from bottle import get, post, template, request, redirect
import sqlite3
import os

# Are we executing at pythonanywhere?
ON_PYTHONANYWHERE = "PYTHONANYWHERE_DOMAIN" in os.environ
 
# Local vs Pythonanywhere
if ON_PYTHONANYWHERE:
    from bottle import default_application
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


if ON_PYTHONANYWHERE:
     application = dafault_application()
else:
    debug(True)
    run(host='localhost', port=8080)