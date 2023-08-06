from datetime import datetime as dt


# prints a user friendly error message if the dob is not formatted properly
def check_dob_format(dob):
    try:
        if dob is not None:
            dt.strptime(dob, "%Y-%m-%d")
    except ValueError as error:
        error.args = (
            "The date `{0}` does not match the format YYYY-MM-DD".format(dob),
        )
        raise


def is_valid_call(call):
    return call.get('chr') is not None and call.get('start') is not None
