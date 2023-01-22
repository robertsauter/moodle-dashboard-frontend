import json
import pandas as pd
import math
import csv

from lib.sql_handler import SQLHandlerFacade

def fetch_data(user_id):
    # reading the file from the repository
    url = 'logs_LA_20__21_20221202-1706.csv'
    df = pd.read_csv(url)

    # get list of enrolled users through sql query
    quiz_grades_handler = SQLHandlerFacade(query="SELECT u.firstname, u.lastname FROM mdl_user_enrolments ue JOIN mdl_enrol e ON e.id = ue.enrolid JOIN mdl_course c ON c.id = e.courseid JOIN mdl_user u ON u.id = ue.userid WHERE c.id = 3;")
    operation_result, quiz_grades_df = quiz_grades_handler.operation()
    eu = quiz_grades_df.apply(lambda x: x.str.cat(sep=' '), axis=1).tolist()

    # get list of enrolled users through csv file
    # eu = []
    # with open('enrolled_users_course_3.csv', newline='', encoding='utf-8') as csvfile:
    #     reader = csv.reader(csvfile, delimiter=',')
    #     # Skip the first row (header)
    #     next(reader)
    #     for row in reader:
    #         eu.append(row[0] + ' ' + row[1])

    #default_user = str(63)
    default_user = str(int(user_id)-2)
    print(default_user)

    # user quisez
    Quiz_module_id = ['610', '616', '664', '669', '679', '697']

    df_user_quiz = df[(df['UserID'] == default_user)
                      & (df["Event context"] != "Quiz: E-exam") &
                      (df['Event name'] == 'Quiz attempt submitted')]
    #print(df_user_quiz)

    # user assignments
    Asg_module_id = ['623', '640', '698', '708']
    df_user_assignment = df[(df['UserID'] == default_user) & (df["Component"] == "Assignment") &
                            (df['Event name'] == "A submission has been submitted.")]
    #print(df_user_assignment)


    # user url
    df_user_url = df[(df["Component"] == "URL") & (df["Event name"] == "Course module viewed") &
                     (df['UserID'] == default_user)]
    df_user_url = df_user_url.drop_duplicates(subset='Event context', keep='first')
    #print(df_user_url)

    # user files
    df_user_file = df[(df["Component"] == "File") & (df["Event name"] == "Course module viewed") &
                      (df['UserID'] == default_user)]
    df_user_file = df_user_file.drop_duplicates(subset=["Event context"], keep='first')
    #print(df_user_file)

    # concatenating all the user activities in one dataframe
    user_all_activities = pd.concat([df_user_quiz, df_user_assignment, df_user_url, df_user_file],
                                    ignore_index=True)

    # all quizes
    df_quizes = df[(df['Component'] == "Quiz") & (df['User full name'].isin(eu)) &
                   (df['Event context'] != 'Quiz: E-exam')]
    dq = df_quizes.drop_duplicates(subset='Event context', keep='first')
    #print(dq)
    Quiz_amount = dq["Component"].count()

    # all assignments
    df_asg = df[(df['Component'] == "Assignment") &
                (df["Event name"] == 'A submission has been submitted.')]
    #print(df_asg)
    da = df_asg.drop_duplicates(subset='Event context', keep='first')
    #print(da)
    Assignment_amount = da["Component"].count()

    # all Urls
    df_url = df[(df['Component'] == "URL") & (df['User full name'].isin(eu)) &
                (df["Event name"] == "Course module viewed")]

    du = df_url.drop_duplicates(subset='Event context', keep='first')
    #print(du)
    Url_amount = du["Component"].count()

    # all files
    df_file = df[(df["Component"] == "File") & df['User full name'].isin(eu)]
    dff = df_file.drop_duplicates(subset=['Event context'], keep='first')
    #print(dff)
    File_amount = dff["Component"].count()

    # dataframe of all the activities that exist in the course
    all_activities = pd.concat([dq, da, du, dff], ignore_index=True)

    #print(all_activities)


    seen_activities = list(user_all_activities['Event context'])
    unseen = all_activities[~all_activities["Event context"].isin(seen_activities)]

    # percentage of each learning material
    quiz_perc = math.ceil(df_user_quiz["Component"].count() * 100 / Quiz_amount)
    assignment_perc = math.ceil(df_user_assignment["Component"].count() * 100 / Assignment_amount)
    url_perc = math.ceil(df_user_url["Component"].count() * 100 / Url_amount)
    file_perc = math.ceil(df_user_file["Component"].count() * 100 / File_amount)


    # converting the dataframes to json


    data_user = user_all_activities.to_json(orient="columns")
    data_unseen = unseen.to_json(orient="columns")
    perc = json.dumps([quiz_perc, assignment_perc, url_perc, file_perc])
    list_df=[data_user,data_unseen,perc]
    json_data=json.dumps(list_df)

    return list_df