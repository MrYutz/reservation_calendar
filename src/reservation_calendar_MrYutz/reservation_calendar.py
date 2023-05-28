from datetime import datetime, timedelta

import pandas as pd


class ReservationCalendar:
    """
    Reservation Calendar
       --------------------
       The Reservation Calendar is a calendar that is used to determine the week number of a given date.
       The Reservation Calendar is based on Memorial Day, which is the last Monday in May.
       The Reservation Calendar is used to determine the start date of a reservation for a future year.

       Week Zero is the week before Memorial Day and does not include Memorial Day.
       Weeks run from Sunday to Saturday, with Sunday being day zero and Friday being day 5.

       Any future date can be converted to a week number and weekday number using the Reservation Calendar.
    """

    def __init__(self):
        current_year = datetime.now().year
        self.FVRC = self.generate_week_number_calendar(current_year - 5, current_year + 10)

    def _validate_and_extend_fvrc(self, year: int) -> None:
        if year not in self.FVRC["Year"].values:
            future_year_calendar = self.generate_week_number_calendar(year, year)
            self.FVRC = pd.concat([self.FVRC, future_year_calendar], ignore_index=True)

    # Define the function to get Memorial Day
    def get_memorial_day(self, year: int) -> datetime:
        # Memorial Day is the last Monday in May
        last_day_of_may = datetime(year, 5, 31)
        offset: int = (last_day_of_may.weekday() - 0) % 7
        memorial_day: datetime = last_day_of_may - timedelta(days=offset)
        return memorial_day

    # Define the function to generate the week number calendar
    def generate_week_number_calendar(self, start_year, end_year) -> pd.DataFrame:
        dfs = []
        for year in range(start_year, end_year + 1):
            memorial_day: datetime = self.get_memorial_day(year)
            thursday_before_memorial_day: datetime = memorial_day - timedelta(
                days=(memorial_day.weekday() - 3) % 7
            )
            sunday_of_week_zero: datetime = thursday_before_memorial_day - timedelta(
                days=4
            )  # Move back 4 days to get to the Sunday of that week
            for week_number in range(14):
                start_date: datetime = sunday_of_week_zero + timedelta(days=7 * week_number)
                dfs.append(
                    pd.DataFrame({"Year": [year], "Week Number": [week_number], "Start Date": [start_date]})
                )
        df: pd.DataFrame = pd.concat(dfs, ignore_index=True)
        return df

    def get_week_number(self, date: datetime) -> int:
        self._validate_and_extend_fvrc(date.year)
        return self.FVRC[(self.FVRC["Year"] == date.year) & (self.FVRC["Start Date"] <= date)].iloc[-1][
            "Week Number"
        ]

    def get_reservation_start_date(self, current_date: datetime, future_year: int) -> datetime:
        self._validate_and_extend_fvrc(future_year)

        current_week_number = self.get_week_number(current_date)
        current_weekday = (current_date.weekday() + 1) % 7
        future_week_start_date = self.FVRC[
            (self.FVRC["Year"] == future_year) & (self.FVRC["Week Number"] == current_week_number)
        ].iloc[0]["Start Date"]
        future_reservation_start_date = future_week_start_date + timedelta(days=current_weekday)
        return future_reservation_start_date

    def get_fvrc(self, date: datetime) -> tuple[int, int]:
        fvrc_week_number = self.get_week_number(date)
        fvrc_weekday_number = (date.weekday() + 1) % 7
        return fvrc_week_number, fvrc_weekday_number

    def get_fvrc_day(self, date: datetime) -> str:
        day_name: list[str] = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        fvrc_weekday_number: int = (date.weekday() + 1) % 7
        return day_name[fvrc_weekday_number]
