import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from group_services.app_service import fetch_assignment_grades, fetch_quiz_grades
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from functools import reduce
from operator import add
from group_services.assessment_service import get_results, operation

assessment_data = operation()

dash.register_page(__name__,
                   path='/assessment',
                   name='Assessment',
                   title='Assessment')
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])


# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "55px",
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#F0F8FF",
}

sidebar = html.Div(
    [
        html.H2("Assessment", className="display-4",style={"font-size": "2.5rem"}),
        html.Hr(),
        html.P(
            "Grades of students for Quizzes and Assignments", className="lead"
        ),
        dcc.Tabs(id="tabs", value='first',className="tabs-header", children=[
            dcc.Tab(label='Quizzes', value='first',className='custom-tab', style= {"background-color":"orange"}),
            dcc.Tab(label='Assignment', value='second',className='custom-tab',style= {"background-color":"orange"}),
        ]
        ),
    ],
    style=SIDEBAR_STYLE,
)


layout = html.Div([
    html.Div(id='assessmentDataDependingOnUserId'),
    sidebar,
])

@dash.callback(
    Output('assessmentDataDependingOnUserId', 'children'),
    Input('userId', 'data'),
    Input("tabs", "value"),
)
def fetch_selected_assessment(user_id,tabs):
    # This is the JSON object, that you can use to display your visualizations :)
    data = get_results(user_id, assessment_data)

    # getting the dataframes from the json file
    quiz_grades_df_edited = pd.read_json(data[0])
    assign_edited = pd.read_json(data[1])

    # This is a plotly graph object to create the same bar chart
    # creating bar chart for quiz
    fig1 = px.bar(quiz_grades_df_edited, x='quiz', y='grade',
                  labels={'quiz': '<b> quiz name <b>', 'grade': '<b> your grade <b>'}
                  , color='quiz', text='grade', range_y=[0, 12]
                  # , title='Quiz Grades'
                  )

    # creating bar chart for assignment
    fig2 = px.bar(assign_edited, x='assignment', y='grade',
                  labels={'assignment': '<b> assignment name <b>', 'grade': '<b> your grade <b>'}
                  , color='assignment', text='grade', range_y=[0, 12]
                  # , title='<b> Assignment Grades <b>'
                  )

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
    fig1.update_yaxes(tickfont_size=1, title_font_family="Arial", tickwidth=10)
    fig2.update_yaxes(tickfont_size=1, title_font_family="Arial", tickwidth=10, showgrid=False)

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
        quiz_feedback += " Congrats! Looks like your learning method fits you, your results are impressive."
    elif missed_quizzes <= 50 * missed_per_quiz and total_grade >= 45 * total_per_grade:
        quiz_feedback += " Great job, you improved! What has helped you getting better? Reflect and keep going!"
    elif missed_quizzes <= 65 * missed_per_quiz and total_grade >= 35 * total_per_grade:
        quiz_feedback += "Hey! The best thing to do is to look at the learning materials again. If you have any " \
                         "questions, contact someone who can help you. "
    else:
        quiz_feedback += "Don‘t worry and focus on the lectures. Helpful tip: Try out different learning methods and " \
                         "find out what works best for you. Get in touch with your professor."

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
    assa_feedback = "you have missed the Assignments " + str(missed_assignment) + " times.  "

    # Feedback possibilities for assignment
    if missed_assignment <= 40 * missed_per_assignment and total_ass_grades >= 60 * total_per_grade_assignment:
        assa_feedback += " Congrats! Looks like your learning method fits you, your results are impressive."
    elif missed_assignment <= 50 * missed_per_assignment and total_ass_grades >= 45 * total_per_grade_assignment:
        assa_feedback += " Great job, you improved! What has helped you getting better? Reflect and keep going!"
    elif missed_assignment <= 65 * missed_per_assignment and total_ass_grades >= 35 * total_per_grade_assignment:
        assa_feedback += " Hey! The best thing to do is to look at the learning materials again. If you have any " \
                         "questions, contact someone who can help you. "
    else:
        assa_feedback += " Don‘t worry and focus on the lectures. Helpful tip: Try out different learning methods and " \
                         "find out what works best for you. Get in touch with your professor. "

    if tabs == "first":
        return [
            html.Br(), html.Br(),
            #html.H1('Assessment page', style={'marginBottom': '2rem'}),
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
            )
        ]
    elif tabs == "second":
        return [
            html.Br(), html.Br(),
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

        ]
    # If the user tries to reach a different page, return a 404 message
    else:
        return [
            # html.H1("404: Not found", className="text-danger"),
            # html.Hr(),
            html.P(f"The pathname {tabs} was not recognised..."),
        ]