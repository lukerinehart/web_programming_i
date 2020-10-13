from bottle import get, post, template, request, redirect, response
import sqlite3
import os
import random, time, datetime


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

@get("/sandbox")
def get_sandbox():
    return template("sandbox")


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


visits = 0
visit_times = {
    }
first_visit = {
    }


@get("/visit")
def get_visit():
    visit_counter = int(request.cookies.get("visit_counter", '0'))
    user_id = request.cookies.get("user_id",str(random.randint(10000,20000)))
    visit_counter = visit_counter + 1
    response.set_cookie("visit_counter", str(visit_counter))
    response.set_cookie("user_id", user_id, max_age=300, secure=True, httponly=True,)
    last_visit = visit_times.get(user_id, "never")
    visit_times[user_id] = str(datetime.datetime.now())
    if last_visit == "never":
        first_visit[user_id] = visit_times[user_id]
    return ("User # " + user_id + ", You have visited " + str(visit_counter) + " times, your last visit was at " + last_visit + " with your first visit at " + first_visit[user_id])


if ON_PYTHONANYWHERE:
     application = default_app()
else:
    debug(True)
    run(host='localhost', port=8080)