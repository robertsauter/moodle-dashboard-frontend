from lib.sql_handler import SQLHandlerFacade

def operation() -> dict:
    # handler = SQLHandlerFacade(app=self.app, query="SELECT id, name FROM mdl_assign")
    handler_assign = SQLHandlerFacade(query="SELECT id, name, intro, duedate FROM mdl_assign")
    handler_assign_submission = SQLHandlerFacade(query="SELECT assignment, status, userid FROM mdl_assign_submission")

    result_assign, assign_df = handler_assign.operation()
    result_assign_submission, assign_df = handler_assign_submission.operation()

    # operation_result = {"result_assign": result_assign, "result_assign_submission": result_assign_submission}
    operation_result = {"result_assign": result_assign.get("result"),
                        "result_assign_submission": result_assign_submission.get("result")}

    """
    handler_one_user = SQLHandlerFacade(app=self.app, query="SELECT assignment, status FROM mdl_assign_submission WHERE userid = 15")
    operation_result, assign_df = handler_one_user.operation()
    """

    # operation_result, pd_dataframe = handler.operation()
    """# Work with pandas.
    print(pd_dataframe.head())
    print(pd_dataframe["id"])
    print(pd_dataframe.loc[:5, ["id", "grade"]])
    print(pd_dataframe.iloc[0])
    print(pd_dataframe[pd_dataframe["grade"] == '8.50000'])
    print(pd_dataframe[pd_dataframe["timemodified"].isin([1577442881, 1577442882])])
    """
    # Work with json data.
    data = operation_result.get("result")
    return operation_result