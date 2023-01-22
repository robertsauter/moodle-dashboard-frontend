import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from functools import reduce
from operator import add
from group_services.assessment_service import operation

dash.register_page(__name__,
                   path='/assessment',
                   name='Assessment',
                   title='Assessment')
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

layout = html.Div([
    html.Div(id='assessmentDataDependingOnUserId')
])


@dash.callback(
    Output('assessmentDataDependingOnUserId', 'children'),
    Input('userId', 'data'),
)
def fetch_selected_assessment(user_id):
    # This is the JSON object, that you can use to display your visualizations :)
    data = operation(user_id)

    # getting the dataframes from the json file
    quiz_grades_df_edited = pd.read_json(data[0])
    assign_edited = pd.read_json(data[1])

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

    # Update x-axis properties
    fig2.update_xaxes(tickfont_size=15, title_font_family="Arial", tickwidth=10)
    fig1.update_xaxes(tickfont_size=12, title_font_family="Arial", tickwidth=10, showgrid=False)

    # Update y-axis properties
    fig1.update_yaxes(tickfont_size=11, title_font_family="Arial", tickwidth=10)
    fig2.update_yaxes(tickfont_size=11, title_font_family="Arial", tickwidth=10, showgrid=False)

    # name of quizzes
    attended_quizzes = data[2]

    grades = []
    for i in attended_quizzes:
        try:
            value = int(quiz_grades_df_edited.loc[quiz_grades_df_edited['quiz'] == i, 'grade'].item())
            try:
                grades.append(value)
            except:
                pass
        except:
            grades.append(0)

    # the number of all quizzes
    total_quizzes_nums0 = data[3]

    # convert the quiz's from string to int
    total_quizzes_nums = [int(i) for i in total_quizzes_nums0]

    # number of attended quizzes 6
    num_attended_quizzes = len(attended_quizzes)

    # total number of the quizzes  9
    all_quizzes_nums = len(total_quizzes_nums)

    # counting missed attendees of the Quizzes
    missed_quizzes = all_quizzes_nums - num_attended_quizzes

    # creating Quiz Feedback
    quiz_feedback = "you have missed the Quizzes " + str(missed_quizzes) + " times.  "

    # calculating the total assignment grades
    try:
        # reduce type error by empty values
        total_grade = reduce(add, grades)
    except TypeError:
        print("empty user value")
    except:
        pass

    # summing by 2. elements in list // by using, will lower feedback failure
    grades_2_in_row = [sum(grades[i:i + 2]) for i in range(0, len(grades), 2)]
    # summing by 3. elements in list // can be used with help of the temp List
    grades_3_in_row = [sum(grades[i:i + 3]) for i in range(0, len(grades), 3)]

    grade_of_each_quiz = 10
    all_quizzes_grades = all_quizzes_nums * grade_of_each_quiz  # 30

    total_per_grade = all_quizzes_grades / 100
    missed_per_quiz = all_quizzes_nums / 100

    # Feedback possibilities for Quizzes
    if missed_quizzes <= 40 * missed_per_quiz and total_grade >= 60 * total_per_grade:
        quiz_feedback += " you are doing very good keep going."
    elif missed_quizzes <= 50 * missed_per_quiz and total_grade >= 45 * total_per_grade:
        quiz_feedback += "you are still doing well but focus more on your materials and study more to achieve better " \
                         "results."
    elif missed_quizzes <= 65 * missed_per_quiz and total_grade >= 35 * total_per_grade:
        quiz_feedback += "your grades is not looking very good. You need to focus more or get help from your Professor."
    else:
        quiz_feedback += "contact your professor."

    # fetching all Assignment grades of the given user if not available then 0
    attended_assignment = data[4]

    # the number of all Assignments [9,12,14]
    total_assignment_nums0 = data[5]

    # convert the Assignments from string to int
    total_assignment_nums = [int(i) for i in total_assignment_nums0]

    assa_grades = []
    for i in attended_assignment:
        try:
            value = int(assign_edited.loc[assign_edited['assignment'] == i, 'grade'].item())
            try:
                assa_grades.append(value)
            except:
                pass
        except:
            assa_grades.append(0)

    # number of attended quizzes
    num_attended_assignment = len(attended_assignment)

    # total number of the quizzes
    number_all_assignment = len(total_assignment_nums)

    # counting missed attendees of the Quizzes
    missed_assignment = number_all_assignment - num_attended_assignment

    # calculating the total assignment grades
    try:
        total_ass_grades = reduce(add, assa_grades)
    except TypeError:
        print("empty user value")
    except:
        pass

    grade_of_each_assignment = 10
    all_assignment_grades = number_all_assignment * grade_of_each_assignment

    total_per_grade_assignment = all_assignment_grades / 100
    missed_per_assignment = number_all_assignment / 100

    # creating Assignment Feedback
    assa_feedback = "you have missed the Quizzes " + str(missed_assignment) + " times.  "

    # Feedback possibilities for assignment
    if missed_assignment <= 40 * missed_per_assignment and total_ass_grades >= 60 * total_per_grade_assignment:
        assa_feedback += " you are doing very good keep going."
    elif missed_assignment <= 50 * missed_per_assignment and total_ass_grades >= 45 * total_per_grade_assignment:
        assa_feedback += "you are still doing well but focus more on your materials and study more to achieve better " \
                         "results."
    elif missed_assignment <= 65 * missed_per_assignment and total_ass_grades >= 35 * total_per_grade_assignment:
        assa_feedback += "your grades is not looking very good. You need to focus more or get help from your Professor."
    else:
        assa_feedback += "contact your professor."

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
