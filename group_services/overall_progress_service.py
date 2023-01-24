import json
import pandas as pd
import math
from group_services.app_service import fetch_users_names


def operation():
    operation_result, quiz_grades_df = fetch_users_names()
    eu = quiz_grades_df.apply(lambda x: x.str.cat(sep=' '), axis=1).tolist()
    return eu

def fetch_data(user_id, eu):
    # reading the file from the repository
    url = 'logs_LA_20__21_20221202-1706.csv'
    df = pd.read_csv(url)

    #default_user = str(63)
    user = str(user_id)

    # user quisez
    Quiz_module_id = ['610', '616', '664', '669', '679', '697']

    df_user_quiz = df[(df['UserID'] == user)
                      & (df["Event context"] != "Quiz: E-exam") &
                      (df['Event name'] == 'Quiz attempt submitted')]
    link = generateLink(df_user_quiz)
    df_user_quiz['Event context'] = "[" + df_user_quiz['Event context'] + "](" + link + ")"

    # user assignments
    Asg_module_id = ['623', '640', '698', '708']
    df_user_assignment = df[(df['UserID'] == user) & (df["Component"] == "Assignment") &
                            (df['Event name'] == "A submission has been submitted.")]
    link = generateLink(df_user_assignment)
    df_user_assignment['Event context'] = "[" + df_user_assignment['Event context'] + "](" + link + ")"
    #print(df_user_assignment)


    # user url
    df_user_url = df[(df["Component"] == "URL") & (df["Event name"] == "Course module viewed") &
                     (df['UserID'] == user)]
    df_user_url = df_user_url.drop_duplicates(subset='Event context', keep='first')
    link = generateLink(df_user_url)
    df_user_url['Event context'] = "[" + df_user_url['Event context'] + "](" + link + ")"
    #print(df_user_url)

    # user files
    df_user_file = df[(df["Component"] == "File") & (df["Event name"] == "Course module viewed") &
                      (df['UserID'] == user)]
    df_user_file = df_user_file.drop_duplicates(subset=["Event context"], keep='first')
    link = generateLink(df_user_file)
    df_user_file['Event context'] = "[" + df_user_file['Event context'] + "](" + link + ")"
    #print(df_user_file)

    # concatenating all the user activities in one dataframe
    user_all_activities = pd.concat([df_user_quiz, df_user_assignment, df_user_url, df_user_file],
                                    ignore_index=True)

    # all quizes
    df_quizes = df[(df['Component'] == "Quiz") & (df['User full name'].isin(eu)) &
                   (df['Event context'] != 'Quiz: E-exam')]
    link = generateLink(df_quizes)
    df_quizes['Event context'] = "[" + df_quizes['Event context'] + "](" + link + ")"
    df_quizes[~df_quizes['Event context'].str.contains('|'.join(["None"]))]
    dq = df_quizes.drop_duplicates(subset='Event context', keep='first')
    #print(dq)
    Quiz_amount = dq["Component"].count()

    # all assignments
    df_asg = df[(df['Component'] == "Assignment") &
                (df["Event name"] == 'A submission has been submitted.')]
    link = generateLink(df_asg)
    df_asg['Event context'] = "[" + df_asg['Event context'] + "](" + link + ")"
    df_asg[~df_asg['Event context'].str.contains('|'.join(["None"]))]
    #print(df_asg)
    da = df_asg.drop_duplicates(subset='Event context', keep='first')
    #print(da)
    Assignment_amount = da["Component"].count()

    # all Urls
    df_url = df[(df['Component'] == "URL") & (df['User full name'].isin(eu)) &
                (df["Event name"] == "Course module viewed")]
    link = generateLink(df_url)
    df_url['Event context'] = "[" + df_url['Event context'] + "](" + link + ")"
    df_url[~df_url['Event context'].str.contains('|'.join(["None"]))]
    du = df_url.drop_duplicates(subset='Event context', keep='first')
    #print(du)
    Url_amount = du["Component"].count()

    # all files
    df_file = df[(df["Component"] == "File") & df['User full name'].isin(eu)]
    link = generateLink(df_file)
    df_file['Event context'] = "[" + df_file['Event context'] + "](" + link + ")"
    df_file[~df_file['Event context'].str.contains('|'.join(["None"]))]
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

def generateLink(data):
    moodleURL = 'http://83.212.126.199/moodle/mod/'
    if data.empty:
        link = 'http://83.212.126.199/moodle/'
        return link
    else:
        new = data['Description'].str.split("course module id '", n=1, expand=True)[1]
        data['Module_id'] = new.str.split("'", n=1, expand=True)[0]
        link = []
        for i in range(len(data)):
            print(data.iloc[i, 5])
            component = data.iloc[i, 5]
            print(data.iloc[i, 8])
            id = data.iloc[i, 8]
            if id == None:
                link.append('None')
                #drop data
            else:
                if component == 'URL':
                    link.append(moodleURL + 'url/view.php?id=' + id)
                elif component == 'File':
                    link.append(moodleURL + 'resource/view.php?id=' + id)
                elif component == 'Quiz':
                    link.append(moodleURL + 'quiz/view.php?id=' + id)
                elif component == 'Assignment':
                    link.append(moodleURL + 'assign/view.php?id=' + id)
                print(link[i])

        return link