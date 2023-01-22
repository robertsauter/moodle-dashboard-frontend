from lib.sql_handler import SQLHandlerFacade


def fetch_users():
    query = SQLHandlerFacade('SELECT u.* FROM mdl_user u JOIN mdl_user_enrolments ue ON ue.userid = u.id JOIN mdl_enrol e ON e.id = ue.enrolid JOIN mdl_course c ON c.id = e.courseid WHERE c.id = 3;')
    result = query.operation()[0]
    return result.get('result')


def fetch_quiz_grades():
    query = SQLHandlerFacade('SELECT qg.id, qg.quiz, qg.userid, qg.grade, qg.timemodified FROM mdl_user_enrolments ue JOIN mdl_enrol e ON e.id = ue.enrolid JOIN mdl_course c ON c.id = e.courseid JOIN mdl_user u ON u.id = ue.userid JOIN mdl_quiz_grades qg ON qg.userid = u.id WHERE c.id = 3')
    result = query.operation()
    return result


def do_something_with_user_id(user_id):
    data = {
        "id": user_id,
        "content": "This is just some string"
    }
    return data


def fetch_assignment_grades():
    query = SQLHandlerFacade('SELECT ag.id, ag.assignment, ag.userid, ag.timecreated, ag.timemodified, ag.grader, ag.grade, ag.attemptnumber FROM mdl_user_enrolments ue JOIN mdl_enrol e ON e.id = ue.enrolid JOIN mdl_course c ON c.id = e.courseid JOIN mdl_user u ON u.id = ue.userid JOIN mdl_assign_grades ag ON ag.userid = u.id WHERE c.id = 3;')
    result = query.operation()
    return result


