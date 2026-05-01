class InvalidDateRangeException(Exception):
    """Exception Raised when the check-in date is later than the check-out date"""
    pass

class BookingDateValidationException(Exception):
    """Exception raised when the check-in date is lower than today"""
    pass

class RoomNotFound(Exception):
    """Exception raised when the room wasnt found."""
    pass

class RoomNotHavefee(Exception):
    """Exception raised when the room doesnt have fee."""
    pass

class CurrencyNotAllowed(Exception):
    """Exception raised whent the currency is not allowed."""