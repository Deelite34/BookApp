from datetime import datetime


def check_date_format(input_date):
    """
    Attempts to detect date format and create datetime object, in one of few
    expected formats.
    If no format is correct, it returns None
    :param input_date: date in string format
    :return date: list, where first element is converted date,
    a datetime.datetime object
                  , second element is date format to be used for date filter
                  in the template.
    """
    possible_formats = {
        '%Y-%m-%d': 'd.m.Y',
        '%Y-%m': 'm.Y',
        '%Y': 'Y'
    }

    for possible_format in possible_formats.keys():
        try:
            date = datetime.strptime(input_date, possible_format)
        except ValueError:
            pass
        else:
            return [date, possible_formats[possible_format]]
    return None


def append_to_url_query(form, key, query_string, q=False, test=False):
    """
    Appends key correctly to the query_string.
    :param form: Form (dict-like) object containing input data from user.
    :param key: String, name of the field to be added to query string.
    :param query_string: String, query string contains already created query
    string. Data will be appended to it.
    :param q: Boolean informing whetever this is a first, mandatory
    parameter, or not.
    :param test: set to True only when running unit tests, to allow use of
    dict instead of form for form argument.
    :return query_string_helper: string result containing created query string.
    """
    if not test:
        keywords = str(form.cleaned_data[
                           key]).strip().split()  # All keywords from single
        # field in form of a list
    else:
        keywords = str(form[key]).strip().split()
    query_string_helper = query_string
    for index, keyword in enumerate(keywords):
        if not keyword or keyword == "None":
            continue
        if index == 0:
            if q:
                query_string_helper = f'{query_string_helper}{keyword}'
            else:
                query_string_helper = f'{query_string_helper}+{key}:' \
                                      f'{keyword}'
        else:
            query_string_helper = f'{query_string_helper}+{keyword}'
    return query_string_helper
