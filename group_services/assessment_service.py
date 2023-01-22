import json
from lib.sql_handler import SQLHandlerFacade
import pandas as pd


# #########################################
# Fetching data and pass them to frontend #
# #########################################

def operation(user_id) -> dict:
        """
          Returns a list of quiz and assumption grades and pass them to the frontend.
                  Parameters:
                          ! current_user (int): the logged-in user can be added as a parameter.
                  Returns:
                          list_df (dict): Values of grades as new dictionary
                          initialized from a mapping object's (key, value) pairs.
        """
        # logged in user
        #current_user = 49
        current_user = int(user_id)-2
        #print(current_user)
        
        quiz_grades_handler = SQLHandlerFacade(query="SELECT qg.id, qg.quiz, qg.userid, qg.grade, qg.timemodified FROM mdl_user_enrolments ue JOIN mdl_enrol e ON e.id = ue.enrolid JOIN mdl_course c ON c.id = e.courseid JOIN mdl_user u ON u.id = ue.userid JOIN mdl_quiz_grades qg ON qg.userid = u.id WHERE c.id = 3")
        operation_result, quiz_grades_df = quiz_grades_handler.operation()

        assign_grade_handler = SQLHandlerFacade(query="SELECT ag.id, ag.assignment, ag.userid, ag.timecreated, ag.timemodified, ag.grader, ag.grade, ag.attemptnumber FROM mdl_user_enrolments ue JOIN mdl_enrol e ON e.id = ue.enrolid JOIN mdl_course c ON c.id = e.courseid JOIN mdl_user u ON u.id = ue.userid JOIN mdl_assign_grades ag ON ag.userid = u.id WHERE c.id = 3; ")
        operation_result, assign_grades_df = assign_grade_handler.operation()

        #assign_grades_df = pd.read_csv('mdl_assign_grades.csv',
        #                               on_bad_lines='skip', encoding='utf-8')
        # quiz_grades_df = pd.read_csv('mdl_quiz_grades.csv',
        #                              on_bad_lines='skip', encoding='utf-8')

        # Work with pandas.

        # convert the grade type to float
        quiz_grades_df.grade = quiz_grades_df.grade.astype(float)
        quiz_grades_df['grade'] = quiz_grades_df['grade'].fillna(.0).astype(float)

        # display the panda file as float .0
        pd.options.display.float_format = '{:,.0f}'.format

        # changing the values of quiz names
        # quiz_grades_df['quiz'] = quiz_grades_df['quiz'].replace(
        #     {37: 'quiz 1', 38: 'quiz 2', 39: 'quiz 3', 40: 'quiz 4', 41: 'quiz 5', 42: 'quiz 6', 43: 'quiz final',
        #      -1: 0, 'Null': 0})
        quiz_grades_df['quiz'] = quiz_grades_df['quiz'].replace(
            {1: 'quiz 1', 2: 'quiz 2', 3: 'quiz 3', 4: 'quiz 4', 5: 'quiz 5', 6: 'quiz 6', 7: 'quiz 7', 8: 'quiz 8', 9: 'quiz 9',
             -1: 0, 'Null': 0})

        # eliminating invalid values
        quiz_grades_df['grade'] = quiz_grades_df['grade'].replace({-1: 0, 'Null': 0})

        # specifying the current user data for grades
        quiz_grades_df_edited = quiz_grades_df.loc[quiz_grades_df['userid'] == current_user]

        # normalizing the values of the Graph(lazy way)
        quiz1nor = quiz_grades_df_edited.loc[quiz_grades_df_edited['quiz'] == 'quiz 1', 'grade']
        quiz2nor = quiz_grades_df_edited.loc[quiz_grades_df_edited['quiz'] == 'quiz 2', 'grade']
        quiz4nor = quiz_grades_df_edited.loc[quiz_grades_df_edited['quiz'] == 'quiz 4', 'grade']
        quiz6nor = quiz_grades_df_edited.loc[quiz_grades_df_edited['quiz'] == 'quiz 6', 'grade']

        quiz1_changed_value = ((quiz1nor - 0) / (3 - 0)) * 10
        quiz2_changed_value = ((quiz2nor - 0) / (4 - 0)) * 10
        quiz4_changed_value = ((quiz4nor - 0) / (3 - 0)) * 10
        quiz6_changed_value = ((quiz6nor - 0) / (3 - 0)) * 10

        quiz_grades_df_edited.loc[quiz_grades_df_edited['quiz'] == 'quiz 1', 'grade'] = quiz1_changed_value
        quiz_grades_df_edited.loc[quiz_grades_df_edited['quiz'] == 'quiz 2', 'grade'] = quiz2_changed_value
        quiz_grades_df_edited.loc[quiz_grades_df_edited['quiz'] == 'quiz 4', 'grade'] = quiz4_changed_value
        quiz_grades_df_edited.loc[quiz_grades_df_edited['quiz'] == 'quiz 6', 'grade'] = quiz6_changed_value

        # changing the values of assignment
        # assign_grades_df['assignment'] = assign_grades_df['assignment'].replace(
        #     {27: 'AS1 - W3', 28: 'AS2 - W5', 30: 'AS3 - W10', 31: 'AS4 - W11', -1: 0, 'Null': 0})
        assign_grades_df['assignment'] = assign_grades_df['assignment'].replace(
            {1: 'AS1', 2: 'AS2', 3: 'AS3', 4: 'AS4',
            5: 'AS5',
            6: 'AS6',
            7: 'AS7',
            8: 'AS8',
            9: 'AS9',
            10: 'AS10',
            11: 'AS11',
            12: 'AS12',
            13: 'AS13',
            14: 'AS14',
            -1: 0, 'Null': 0})

        assign_grades_df['grade'] = assign_grades_df['grade'].replace({-1: 0, 'Null': 0})

        # specifying current user data for assignment
        assign_edited = assign_grades_df.loc[assign_grades_df['userid'] == current_user]

        # Work with json data.
        # converting quiz grades to json data
        user_quiz_grades = quiz_grades_df_edited.to_json(orient="columns")

        # converting assign grades to json data
        user_assign_grades = assign_edited.to_json(orient="columns")

        # combined both data frames in a list
        list_df = [user_quiz_grades, user_assign_grades]

        # convert a subset of Python objects into a json string. (can be used later)
        json_data = json.dumps(list_df)

        return list_df