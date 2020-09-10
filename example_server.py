from bottle import route, run, template

@route('/')  #for default
@route('/hello/<my_name>')
def get_hello(my_name="Unknown Person"):
    return(template("<html>Hello, {{name}}!! <hr></html>", name=my_name))

@route('/goodbye')
def get_goodbye():
    return ("goodbye there!")


run(host="localhost", port=8080)