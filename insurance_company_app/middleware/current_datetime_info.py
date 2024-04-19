from django.utils import timezone
import calendar


class CurrentDateTimeMiddleware:

    def __init__(self, get_response):
        self.__get_response = get_response

    def __call__(self, request):
        current_datetime = timezone.localtime(timezone.now())
        current_timezone = timezone.get_current_timezone()
        text_calendar = calendar.TextCalendar(firstweekday=0)\
            .formatmonth(current_datetime.year, current_datetime.month)
        formatted_calendar_rows = text_calendar.split('\n')

        request.current_datetime = current_datetime
        request.current_timezone = current_timezone
        request.text_calendar = formatted_calendar_rows

        response = self.__get_response(request)
        return response
