from enum import Enum

crontab_every_day = {"minute": "0", "day_of_week": "*", "day_of_month": "*", "month_of_year": "*"}


# class ScheduledTime(Enum):
#     at_4_am = {"hour": "4", **EVERY_DAY}
#     at_5_am = {"hour": "5", **EVERY_DAY}
#     at_6_am = {"hour": "6", **EVERY_DAY}
#     at_7_am = {"hour": "7", **EVERY_DAY}
#     at_8_am = {"hour": "8", **EVERY_DAY}
#     at_9_am = {"hour": "9", **EVERY_DAY}
#     at_10_am = {"hour": "10", **EVERY_DAY}
#     at_11_am = {"hour": "11", **EVERY_DAY}
#     at_12_am = {"hour": "12", **EVERY_DAY}
#     at_1_pm = {"hour": "13", **EVERY_DAY}
#     at_2_pm = {"hour": "14", **EVERY_DAY}
#     at_3_pm = {"hour": "15", **EVERY_DAY}
#     at_4_pm = {"hour": "16", **EVERY_DAY}
#     at_5_pm = {"hour": "17", **EVERY_DAY}
#     at_6_pm = {"hour": "18", **EVERY_DAY}
#     at_7_pm = {"hour": "19", **EVERY_DAY}
#     at_8_pm = {"hour": "20", **EVERY_DAY}
#     at_9_pm = {"hour": "21", **EVERY_DAY}
#     at_10_pm = {"hour": "22", **EVERY_DAY}
#     at_11_pm = {"hour": "23", **EVERY_DAY}


class SetupStatus(Enum):
    active = "Active"
    disabled = "Disabled"
