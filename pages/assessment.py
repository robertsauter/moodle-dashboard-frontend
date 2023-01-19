import dash
import requests
from dash import html, dcc
from group_services.app_service import fetch_users
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State
from functools import reduce
from operator import add
from group_services.assessment_service import operation

dash.register_page(__name__,
                   path='/assessment',
                   name='Assessment',
                   title='Assessment')
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

#r = requests.get('http://localhost:5000/api/group/assessment')

data = fetch_users()

layout = html.Div([
    html.Div(id='dataDependingOnUserId2')
])

@dash.callback(
    Output('dataDependingOnUserId2', 'children'),
    Input('userId', 'data'),
)
def fetch_data_on(user_id):

    # This is the JSON object, that you can use to display your visualizations :)
    #data = r.json()
    data = operation(user_id)

    # getting the dataframes from the json file
    quiz_grades_df_edited = pd.read_json(data[0])
    assign_edited = pd.read_json(data[1])

    # just a checker
    print(quiz_grades_df_edited)
    print(assign_edited)

    # This is a plotly graph object to create the same bar chart

    # creating bar chart for quiz
    fig1 = px.bar(quiz_grades_df_edited, x='quiz', y='grade',
                labels={'quiz': '<b> quiz name <b>', 'grade': '<b> your grade <b>'}
                , title='Quiz Grades', color='quiz', text='grade', range_y=[0, 12])

    # creating bar chart for assignment
    fig2 = px.bar(assign_edited, x='assignment', y='grade',
                labels={'assignment': '<b> assignment name <b>', 'grade': '<b> your grade <b>'}
                , title='<b> Assignment Grades <b>', color='assignment', text='grade', range_y=[0, 12])

    # changing the quiz text size and background
    fig1.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig1.update_layout(uniformtext_minsize=1, paper_bgcolor="rgb(238,155,113,0)")

    # changing the assignment text size and background
    fig2.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig2.update_layout(uniformtext_minsize=1, paper_bgcolor="rgb(238,155,113,0)")
    fig2.update_layout(
        font_family="Courier New",
        font_color="black",
        title_font_family="Times New Roman",
        title_font_color="Green",
        legend_title_font_color="green"
    )

    # changing the quiz text size and background
    fig1.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig1.update_layout(uniformtext_minsize=1, paper_bgcolor="rgb(238,155,113,0)")
    fig1.update_layout(
        font_family="Courier New",
        font_color="black",
        title_font_family="Times New Roman",
        title_font_color="Green",
        legend_title_font_color="green"
    )

    # Update xaxis properties
    fig2.update_xaxes(tickfont_size=15, title_font_family="Arial", tickwidth=10)
    fig1.update_xaxes(tickfont_size=12, title_font_family="Arial", tickwidth=10, showgrid=False)

    # Update yaxis properties
    fig1.update_yaxes(tickfont_size=11, title_font_family="Arial", tickwidth=10)
    fig2.update_yaxes(tickfont_size=11, title_font_family="Arial", tickwidth=10, showgrid=False)

    '''
    Todo: 
        1-Feedback messages depending on the actual grades
        2-Heat-Map (to not show grades directly to the user)
    '''

    # fetching all Quizzes grades of the given user if not available then 0
    quizes_all = ['quiz 1', 'quiz 2', 'quiz 3', 'quiz 4', 'quiz 5', 'quiz 6', 'quiz final']
    grades = []
    for i in range(len(quizes_all)):
        try:
            value = int(quiz_grades_df_edited.loc[quiz_grades_df_edited['quiz'] == quizes_all[i], 'grade'].item())
            try:
                grades.append(value)
            except:
                pass
        except:
            grades.append(0)

    # creating Quiz Feedback
    quiz_feedback = ""


    # counting missed attendees of the Quizzes
    missedQuizes = 0
    for i in grades:
        if i == 0:
            missedQuizes += 1
            quiz_feedback = "you have missed the Quizzes " + str(missedQuizes) + " times.  "

    # calculating the total assignment grades
    totalGrade = reduce(add, grades)
    print(totalGrade)

    # Feedback possibilities for Quizzes
    if grades[0] + grades[1] + grades[2] >= 22 and grades[3] + grades[4] + grades[5] >= 22 and grades[
        6] >= 6 or totalGrade >= 50:
        quiz_feedback += " you are doing very good keep going."
    elif 15 <= grades[0] + grades[1] + grades[2] < 22 and 15 < grades[3] + grades[4] + grades[5] and 4 <= grades[6] < 6:
        quiz_feedback += "you are still doing well but focus more on your materials and study more to achieve better " \
                        "results."
    elif 10 <= grades[0] + grades[1] + grades[2] < 15 and 10 <= grades[3] + grades[4] + grades[5] and 2 <= grades[6] < 4:
        quiz_feedback += "your grades is not looking very good. You need to focus more or get help from your Professor."
    else:
        quiz_feedback += " contact your professor."


    # fetching all Assignment grades of the given user if not available then 0
    assem_all = ['AS1 - W3', 'AS2 - W5', 'AS3 - W10', 'AS4 - W11']
    assa_grades = []
    for i in range(len(assem_all)):
        try:
            value = int(assign_edited.loc[assign_edited['assignment'] == assem_all[i], 'grade'].item())
            try:
                assa_grades.append(value)
            except:
                pass
        except:
            assa_grades.append(0)


    # creating Assignment Feedback
    assa_feedback = ""

    # counting missed attendees of the Assignment
    missed_assa = 0
    for i in assa_grades:
        if i == 0:
            missed_assa += 1
            assa_feedback = "you have missed the Assignment " + str(missed_assa) + " times.  "

    # calculating the total assignment grades
    totalasGrade = reduce(add, assa_grades)
    print(totalasGrade)

    # Feedback possibilities for assignment
    if assa_grades[0] + assa_grades[1] >= 14 and assa_grades[2]+assa_grades[3] >= 14 or totalasGrade >= 28:
        assa_feedback += " you are doing very good keep going."
    elif 10 <= assa_grades[0] + assa_grades[1] < 14 and 10 <= assa_grades[2]+assa_grades[3] < 14 or totalasGrade >= 24:
        assa_feedback += " you are still doing well but focus more on your materials and study more to achieve better " \
                        "results."
    elif 8 <= assa_grades[0] + assa_grades[1] < 10 and 8 <= assa_grades[2]+assa_grades[3] < 10 or totalasGrade >= 20:
        assa_feedback += " your grades is not looking very good. You need to focus more or get help from your Professor."
    else:
        quiz_feedback += " contact your professor."


    # This is the html layout, that is displayed on the page
    return html.Div(children=[
        html.H1('Assessment page', style={'marginBottom': '2rem'}),

        html.H2('Quiz Grades'),
        dcc.Graph(
            figure=fig1,
            style={'marginBottom': '5rem'}
        ),
        # Button for feedback
        dbc.Button(
            "Quiz Feedback",
            id="popover-target",
            className="me-1",
        ),
        dbc.Popover(
            dbc.PopoverBody(f"{quiz_feedback}"),
            target="popover-target",
            trigger="click",
        ),

        html.H2('Assignment Grades'),
        dcc.Graph(figure=fig2),
        dbc.Button(
            "Assignment Feedback",
            id="popover-target2",
            className="me-1",
        ),
        dbc.Popover(
            dbc.PopoverBody(f"{assa_feedback}"),
            target="popover-target2",
            trigger="click",
        ),

    ])