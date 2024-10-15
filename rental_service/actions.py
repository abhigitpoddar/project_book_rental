import datetime
import os

from .models import Status, Rental

from dateutil import relativedelta
from datetime import datetime


# ALl rental service related actions will be taken care by this class
class RentalServiceAction:
    def refresh_amounts(self, rent: Rental, current_time: datetime) -> None:
        change = False
        if os.environ.get('TIMEUNIT') == "Month":
            updated_date = rent.updated_at.date()
            current_date = current_time.date()
            delta = relativedelta.relativedelta(current_date, updated_date)
            diff = delta.months + delta.years*12
            if diff >= 1:
                change = True

        if os.environ.get('TIMEUNIT') == "Minute":
            print("here....")
            diff = (current_time - rent.updated_at).total_seconds() // 60.0
            if diff >= 1:
                print(diff)
                change = True

        if change:
            rent.status = Status.PURCHASED.value
            rent.amount += (rent.book.page / 100) * (diff)
            rent.updated_at = current_time
            print(rent.amount)
            rent.save()
