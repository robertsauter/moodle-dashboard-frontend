import json
from group_services.app_service import fetch_quiz_grades, fetch_assignment_grades
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
    # current_user = 49
    current_user = int(user_id) - 2

    # fetch quiz grades and assign grades from the database
    operation_result, quiz_grades_df = fetch_quiz_grades()

    operation_result, assign_grades_df = fetch_assignment_grades()

    '''
    #fetch the data locylly
    assign_grades_df = pd.read_csv('mdl_assign_grades.csv',
                                   on_bad_lines='skip', encoding='utf-8')
    quiz_grades_df = pd.read_csv('mdl_quiz_grades.csv',
                                   on_bad_lines='skip', encoding='utf-8')
    '''

    # Work with pandas.
    # convert the grade type to float
    quiz_grades_df.grade = quiz_grades_df.grade.astype(float)
    quiz_grades_df['grade'] = quiz_grades_df['grade'].fillna(.0).astype(float)

    # get a unique quizzes
    all_quizzes = quiz_grades_df['quiz'].unique()
    # get a unique assignment
    all_assignment = assign_grades_df['assignment'].unique()
    max_value_of_each_quiz = quiz_grades_df['grade'].groupby(quiz_grades_df['quiz']).max().to_frame()
    d = pd.DataFrame(max_value_of_each_quiz).astype(int)
    a = d.values.tolist()
    max_value_of_each_quiz1 = sum(a, [])

    # Work with pandas.
    # convert the grade type to float
    quiz_grades_df.grade = quiz_grades_df.grade.astype(float)
    quiz_grades_df['grade'] = quiz_grades_df['grade'].fillna(.0).astype(float)

    # display the panda file as float .0
    pd.options.display.float_format = '{:,.0f}'.format

    # eliminating invalid values
    quiz_grades_df['grade'] = quiz_grades_df['grade'].replace({-1: 0, 'Null': 0})

    # specifying the current user data for grades
    quiz_grades_df_edited = quiz_grades_df.loc[quiz_grades_df['userid'] == current_user]

    # changing names dynamically depends on number of quizzes
    quizes_nums = set()
    # the name of all attended quizzes ['quiz 4', ..]
    quiz_names = []
    for i in quiz_grades_df_edited['quiz']:
        quizes_nums.add(i)

    for i in quizes_nums:
        quiz_grades_df_edited['quiz'] = quiz_grades_df_edited['quiz'].replace({i: 'quiz ' + str(i)})
        quiz_names.append('quiz ' + str(i))

    quiznor = []
    # normalizing the values of the Graph
    for i in quiz_grades_df_edited['quiz']:
        try:
            value = (quiz_grades_df_edited.loc[quiz_grades_df_edited['quiz'] == i, 'grade'].item())
            try:
                quiznor.append(value)
            except:
                pass
        except:
            pass

    quiz_changed_values = []
    counter_index = 0
    for i in all_quizzes:
        for j in quizes_nums:
            if i == j:
                max_value = max_value_of_each_quiz1[j - 1]
                p = quiznor[counter_index]
                counter_index += 1
                mino = 0
                try:
                    value = ((p - mino) / (max_value - mino)) * 10
                    try:
                        quiz_changed_values.append(value)
                    except:
                        pass
                except:
                    pass

    # change the normalized values in the dataframe
    counter = 0
    for i in quiz_names:
        quiz_grades_df_edited.loc[quiz_grades_df_edited['quiz'] == i, 'grade'] = quiz_changed_values[counter]
        counter += 1

    assign_grades_df['grade'] = assign_grades_df['grade'].replace({-1: 0, 'Null': 0})

    # specifying current user data for assignment
    assign_edited = assign_grades_df.loc[assign_grades_df['userid'] == current_user]

    # changing the values of assignment
    assignment_nums = set()
    assignment_names = []
    for i in assign_edited['assignment']:
        assignment_nums.add(i)

    for i in assignment_nums:
        assign_edited['assignment'] = assign_edited['assignment'].replace({i: 'As - w' + str(i)})
        assignment_names.append('As - w' + str(i))

    # Work with json.
    # converting quiz grades to json data
    list_string = list(map(str, all_quizzes))
    list_string2 = list(map(str, all_assignment))

    user_quiz_grades = quiz_grades_df_edited.to_json(orient="columns")

    # converting assign grades to json data
    user_assign_grades = assign_edited.to_json(orient="columns")

    # combined both data frames in a list
    list_df = [user_quiz_grades, user_assign_grades, quiz_names, list_string, assignment_names, list_string2]

    # convert a subset of Python objects into a json string. (can be used later)
    json_data = json.dumps(list_df)

    return list_df
