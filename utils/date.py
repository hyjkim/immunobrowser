from datetime import date

class FakeDate(date):
  "A manipulable date replacement copied from http://stackoverflow.com/questions/4481954/python-trying-to-mock-datetime-date-today-but-not-working "
  def __new__(cls, *args, **kwargs):
    return date.__new__(date, *args, **kwargs)
