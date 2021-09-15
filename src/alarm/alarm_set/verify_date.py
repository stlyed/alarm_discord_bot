def verify_date(today):
    # extract the necessary values from the time
    month = today[:2]
    day = today[3:5]
    year = today[6:10]
    alarm_confirmation = ''  # initialize this value for return statement
    verified = True

    # if date does not have 10 spaces, stop
    if len(today) != 10:
        alarm_confirmation = f'Please use mm-dd-yyyy format'
        verified = False
        return [alarm_confirmation, verified]
    else:
        # make sure that everything is verified
        while verified:
            # check if month is a number
            if month.isdigit():
                # if month is not greater than 12
                if not (0 < int(month) <= 12):
                    alarm_confirmation = f'alarm could not be created, ' \
                                         f'it\'s likely that \"{month}\" in \"{today}\" is greater than 12'
                    verified = False
            else:
                alarm_confirmation = f'alarm could not be created, ' \
                                     f'it\'s likely that \"{month}\" in \"{today}\" not a digit.\n' \
                                     f'Please use mm-dd-yyyy format'
                verified = False

            # check if day is a number
            if day.isdigit():
                # allow up 29 days if month is February
                if 0 < int(day) <= 29 and int(month) == 2:
                    pass
                # allow up 30 days if an odd month
                elif 0 < int(day) <= 30 and int(month) % 2 == 1:
                    pass
                # allow up to 31 days if an even month and it's not February
                elif 0 < int(day) <= 31 and int(month) % 2 == 0 and int(month) != 2:
                    pass

                else:
                    alarm_confirmation = f'alarm could not be created, ' \
                                         f'it\'s likely that month \"{month}\" does not have \"{day}\" day(s)'
                    verified = False
            # if day is not a number
            else:
                alarm_confirmation = f'alarm could not be created, ' \
                                     f'it\'s likely that \"{day}\" in \"{day}\" not a digit.\n'
                verified = False

            # if year is not a number
            if not year.isdigit():
                verified = False

            # if everything checks out, give back the date
            if verified:
                # if the whole while loop runs, return
                return [f'on {today}. \n', verified]

        # if the while loop breaks in the middle, it will return an error
        return [alarm_confirmation, verified]
