from lib.sql_handler import SQLHandlerFacade
import datetime
import calendar

def operation() -> dict:
    handler_assign = SQLHandlerFacade(query="SELECT id, name, intro, duedate FROM mdl_assign")
    handler_assign_submission = SQLHandlerFacade(query="SELECT assignment, status, userid FROM mdl_assign_submission")

    result_assign, assign_df = handler_assign.operation()
    result_assign_submission, assign_df = handler_assign_submission.operation()

    operation_result = {"result_assign": result_assign.get("result"),
                        "result_assign_submission": result_assign_submission.get("result")}

    data = operation_result.get("result")
    return operation_result

# Calendar Arrays
dayAbbr = [y for y in calendar.day_abbr]
monthAbbr = [w for w in calendar.month_abbr]

# Convert epoch time to deadline
def deadline(duedate_epoch):
  duedate_full = str(datetime.datetime.fromtimestamp(duedate_epoch))
  duedate_year = int(duedate_full[0:4])
  duedate_month = int(duedate_full[5:7])
  duedate_day = int(duedate_full[8:10])
  duedate_time = str(duedate_full)[11:16]

  weekdayNumber = calendar.weekday(duedate_year, duedate_month, duedate_day)
  weekdayAbbr = dayAbbr[weekdayNumber]

  deadlineStr = "due " + weekdayAbbr + ", " + \
                str(duedate_day) + " " + \
                monthAbbr[duedate_month] + " " + \
                str(duedate_year) + " " + \
                str(duedate_time)
  return deadlineStr

# Fake current time
def currentDate():
  current_date = datetime.datetime.now() # current date/time
  current_date_epoch = current_date.timestamp() # converting into epoch time
  fake_current_date = float(current_date_epoch) - float(94694400) # subtracting 3 years

  return fake_current_date

# List of assignments
def assignmentsToDisplay(user, dataset):
  assignmentsList = []

  for submission in dataset["result_assign_submission"]: # going through submissions
    statusDict = {}
    if int(submission["userid"]) == int(user): # pick submissions from the user
      for assignment in dataset["result_assign"]: #going through
        if int(submission["assignment"]) == int(assignment["id"]): # pick the assignment
          statusDict["status"] = submission["status"] # status as a dictionary
          assignment.update(statusDict) # append status to assignment
          assignmentsList.append(assignment) # append dict to the list

  return(assignmentsList)

# Icons
def whichIcon(status, duedate):
    if status == "submitted":
        icon_src = "assets/check2-circle.svg"
    elif int(duedate) < currentDate():
        icon_src = "assets/x-circle.svg"
    else:
        icon_src = ""

    return icon_src