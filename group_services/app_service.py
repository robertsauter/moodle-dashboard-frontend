from lib.sql_handler import SQLHandlerFacade


def fetch_users():
    query = SQLHandlerFacade('SELECT u.* FROM mdl_user u JOIN mdl_user_enrolments ue ON ue.userid = u.id JOIN mdl_enrol e ON e.id = ue.enrolid JOIN mdl_course c ON c.id = e.courseid WHERE c.id = 3;')
    result = query.operation()[0]
    return result.get('result')


def fetch_quiz_grades():
    query = SQLHandlerFacade('SELECT * FROM mdl_quiz_grades')
    result = query.operation()[0]
    return result


def do_something_with_user_id(user_id):
    data = {
        "id": user_id,
        "content": "This is just some string"
    }
    return data
