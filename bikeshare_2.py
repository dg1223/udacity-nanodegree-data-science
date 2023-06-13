import time
import pandas as pd
import numpy as np
import os
import calendar

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("\n")
    print("Hello! Let's explore some US bikeshare data!")
    print("\n")

    valid_cities = ["chicago", "new york", "washington"]

    city_dict = {
        "chicago": "chicago",
        "new york": "new york city",
        "washington": "washington",
    }

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input(
        "Enter the name of the city you want to analyze. Choose any of these 3 cities: chicago, new york, washington. Please enter the name exactly as shown.: "
    )

    while city.lower() not in valid_cities:
        print("\n")
        print("Invalid city. Please enter a valid city as instructed.")
        print("\n")
        city = input(
            "Enter the name of the city you want to analyze. Choose any of these 3 cities: chicago, new york, washington. Please enter the name exactly as shown.: "
        )

    print("\n")
    chosen_city = city_dict.get(city, "Invalid city")
    print("You have chosen:", chosen_city)
    print("\n")

    # get user input for month (all, january, february, ... , june)
    valid_months = [
        "jan",
        "feb",
        "mar",
        "apr",
        "may",
        "jun",
        "jul",
        "aug",
        "sep",
        "oct",
        "nov",
        "dec",
        "all",
    ]

    month_dict = {
        "jan": "January",
        "feb": "February",
        "mar": "March",
        "apr": "April",
        "may": "May",
        "jun": "June",
        "jul": "July",
        "aug": "August",
        "sep": "September",
        "oct": "October",
        "nov": "November",
        "dec": "December",
        "all": "All",
    }

    month = input(
        "Enter the first 3 letters of the month you want to analyze the data for. For example, if you want January data, enter 'jan' (without the quotes). If you want June, enter 'jun' and so on. Enter 'all' to disable this filter.: "
    )

    while month.lower() not in valid_months:
        print("\n")
        print("Invalid month. Please enter a valid month as instructed.")
        print("\n")
        month = input(
            "Enter the first 3 letters of the month you want to analyze the data for. For example, if you want January data, enter 'jan' (without the quotes). If you want August, enter 'aug' and so on. Enter 'all' to disable this filter.: "
        )

    print("\n")
    chosen_month = month_dict.get(month, "Invalid month")
    print("You have chosen:", chosen_month)
    print("\n")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = [
        "sun",
        "mon",
        "tue",
        "wed",
        "thu",
        "fri",
        "sat",
        "all",
    ]

    day_dict = {
        "sun": "Sunday",
        "mon": "Monday",
        "tue": "Tuesday",
        "wed": "Wednesday",
        "thu": "Thursday",
        "fri": "Friday",
        "sat": "Saturday",
        "all": "All",
    }

    day = input(
        "Enter the name of the day of the week. For example, if you want Friday, enter 'fri' (without the quotes). Enter 'all' to disable this filter.: "
    )

    while day.lower() not in valid_days:
        print("\n")
        print("Invalid day. Please enter a valid day of the week as instructed.")
        print("\n")
        day = input(
            "Enter the name of the day of the week. For example, if you want Monday, enter 'mon' (without the quotes). Enter 'all' to disable this filter.: "
        )
    print("\n")
    chosen_day = day_dict.get(day, "Invalid day")
    print("You have chosen:", chosen_day)
    print("\n")

    print("-" * 40)
    print("You chose: {}, {}, {}".format(chosen_city, chosen_month, chosen_day))
    print("\n")
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    if city == "new york":
        city = "new york city"

    """ current_path = os.getcwd()
    print("Current path:", current_path)
    print(CITY_DATA.get(city)) """

    df = pd.read_csv(CITY_DATA.get(city))

    # Convert Start Time column to datetime format
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # Filter by month if applicable
    if month != "all":
        # Extract month from Start Time column
        df["Month"] = df["Start Time"].dt.month
        # Filter by month
        month_dict = {
            "jan": 1,
            "feb": 2,
            "mar": 3,
            "apr": 4,
            "may": 5,
            "jun": 6,
            "jul": 7,
            "aug": 8,
            "sep": 9,
            "oct": 10,
            "nov": 11,
            "dec": 12,
        }
        month_num = month_dict.get(month)
        df = df[df["Month"] == month_num]

        # Check if the resulting dataframe is empty after filtering for month
        if df.empty:
            print("There is no data available for the chosen month.")
            return pd.DataFrame()  # Return an empty dataframe and jump to restart

    # Filter by day if applicable
    if day != "all":
        # Extract day of week from Start Time column
        df["Day"] = df["Start Time"].dt.dayofweek
        # Filter by day (Monday=0, Sunday=6)
        day_dict = {
            "mon": 0,
            "tue": 1,
            "wed": 2,
            "thu": 3,
            "fri": 4,
            "sat": 5,
            "sun": 6,
        }
        day_num = day_dict.get(day)
        df = df[df["Day"] == day_num]

        # Check if the resulting dataframe is empty after filtering for day
        if df.empty:
            print("There is no data available for the chosen day.")
            return pd.DataFrame()  # Return an empty dataframe and jump to restart

    # Check if the resulting dataframe is empty
    if df.empty:
        print("There is no data available for the chosen month or day or both.")
        return pd.DataFrame()  # Return an empty dataframe

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # display the most common month

    # Extract month from Start Time column
    df["Month"] = df["Start Time"].dt.month
    # Find the most common month
    common_month = df["Month"].mode()[0]
    # Convert month number to month name
    common_month_name = calendar.month_name[common_month]
    print("The most common month: ", common_month_name)

    # display the most common day of week
    df["Day of Week"] = df["Start Time"].dt.dayofweek
    # Find the most common day of week
    common_day = df["Day of Week"].mode()[0]
    # Convert day number to day name
    common_day_name = calendar.day_name[common_day]
    print("The most common day of week: ", common_day_name)

    # display the most common start hour
    # Extract hour from Start Time column
    df["Hour"] = df["Start Time"].dt.hour
    # Find the most common start hour
    common_hour = df["Hour"].mode()[0]
    print("The most common start hour: ", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df["Start Station"].mode()[0]
    print("The most commonly used start station: ", common_start_station)

    # Display most commonly used end station
    common_end_station = df["End Station"].mode()[0]
    print("The most commonly used end station: ", common_end_station)

    # Display most frequent combination of start station and end station trip
    df["Trip"] = df["Start Station"] + " to " + df["End Station"]
    common_trip = df["Trip"].mode()[0]
    print(
        "The most frequent combination of start station and end station trip: ",
        common_trip,
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # Display total travel time
    total_travel_time = df["Trip Duration"].sum()
    total_travel_time_formatted = pd.to_timedelta(total_travel_time, unit="s")
    total_days = total_travel_time_formatted.days
    total_hours, remainder = divmod(total_travel_time_formatted.seconds, 3600)
    total_minutes, total_seconds = divmod(remainder, 60)
    print(
        "Total travel time: {} days, {} hours, {} minutes, {} seconds".format(
            total_days, total_hours, total_minutes, total_seconds
        )
    )

    # Display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    mean_travel_time_formatted = pd.to_timedelta(mean_travel_time, unit="s")
    mean_days = mean_travel_time_formatted.days
    mean_hours, remainder = divmod(mean_travel_time_formatted.seconds, 3600)
    mean_minutes, mean_seconds = divmod(remainder, 60)
    print(
        "Mean travel time: {} days, {} hours, {} minutes, {} seconds".format(
            mean_days, mean_hours, mean_minutes, mean_seconds
        )
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts()
    print("Counts of User Types:")
    for user_type, count in user_types.items():
        print("{}: {}".format(user_type, count))
    print()

    # Display counts of gender (excluding Washington)
    if "Gender" in df.columns:
        gender_counts = df["Gender"].value_counts()
        print("Counts of Gender:")
        for gender, count in gender_counts.items():
            print("{}: {}".format(gender, count))
        print()
    else:
        print("Gender data is not available for the selected city.")

    # Display earliest, most recent, and most common year of birth (excluding Washington)
    if "Birth Year" in df.columns:
        earliest_birth_year = int(df["Birth Year"].min())
        most_recent_birth_year = int(df["Birth Year"].max())
        most_common_birth_year = int(df["Birth Year"].mode()[0])
        print("Birth Year Statistics:")
        print("Earliest Birth Year:", earliest_birth_year)
        print("Most Recent Birth Year:", most_recent_birth_year)
        print("Most Common Birth Year:", most_common_birth_year)
    else:
        print("Birth Year data is not available for the selected city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # handle exception when no data is available
        if df.size > 0:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
        else:
            pass

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()
