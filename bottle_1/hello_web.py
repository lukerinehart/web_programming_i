from bottle import route, run, template


@route('/hello')
@route('/hello/<my_name>')  # Route Specifier
def get_hello(my_name="Unknown Person"):    # Route Handler
    return template("Hello, {{name}}!", name=my_name)

## my_name is a variable

@route('/goodbye')
def get_goodbye():
    return "Goodbye there!"

run(host='localhost', port=8080)