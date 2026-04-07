class InvalidDateRangeException(Exception):
    """Exception Raised when the check-in date is later than the check-out date"""
    pass

class BookingDateValidationException(Exception):
    """Exception raised when the check-in date is lower than today"""
    pass