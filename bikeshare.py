import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs.
    valid_cities = ['chicago', 'new york city', 'washington']

    while True:
        city = input("Please enter a city (Chicago, New York City, Washington): ").lower()
        if city in valid_cities:
            print("You entered:", city.title())
            break
        else:
            print("Invalid input. Please enter one of the specified cities.")

    # Get user input for month (all, january, february, ... , june).
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

    while True:
        month = input("Please enter a month (January, February, March, April, May, June, or 'all'): ").lower()
        if month in valid_months:
            print("You entered:", month.title())
            break
        else:
            print("Invalid input. Please enter a valid month or 'all'.")

    # Get user input for day of week (all, monday, tuesday, ... sunday).
    valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

    while True:
        day = input("Please enter a day of the week (Monday, Tuesday, ..., Sunday, or 'all'): ").lower()

        if day in valid_days:
            print("You entered:", day.title())
            break
        else:
            print("Invalid input. Please enter a valid day of the week or 'all'.")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads all data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    file_name = CITY_DATA[city.lower()]
    df = pd.read_csv(file_name)
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
     # Filter by month if applicable.
    if month.lower() != 'all':
        month_num = pd.to_datetime(month, format='%B').month
        df = df[df['Start Time'].dt.month == month_num]

    # Filter by day if applicable.
    if day.lower() != 'all':
        df = df[df['Start Time'].dt.day_name().str.lower() == day.lower()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    common_month = df['Start Time'].dt.month.mode()[0]
    print(f"The most common month for travel is: {common_month}")

    # Display the most common day of week.
    common_day_of_week = df['Start Time'].dt.day_name().mode()[0]
    print(f"The most common day of the week for travel is: {common_day_of_week}")

    # Display the most common start hour.
    common_start_hour = df['Start Time'].dt.hour.mode()[0]
    print(f"The most common start hour is: {common_start_hour}:00")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station.
    common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station is: {common_start_station}")

    # Display most commonly used end station.
    common_end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station is: {common_end_station}")

    # Display most frequent combination of start station and end station trip.
    frequent_combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"The most frequent combination of start and end stations for trips is: {frequent_combination}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time.
    total_travel_time = df['Trip Duration'].sum()
    print(f"The total travel time for all trips is: {total_travel_time} seconds")

    # Display mean travel time.
    mean_travel_time = df['Trip Duration'].mean()
    print(f"The mean travel time is: {mean_travel_time} seconds")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types.
    if 'User Type' in df:
        user_types = df['User Type'].value_counts()
        print("\nCounts of user types:")
        for user_type, count in user_types.items():
            print(f"{user_type}: {count}")
    else:
        print('\nUser Type information not availabel')

    # Display counts of gender.
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of gender:")
        for gender, count in gender_counts.items():
            print(f"{gender}: {count}")
    else:
        print('\nGender information not availabel')
    
    # Display earliest, most recent, and most common year of birth.
    if 'Birth Year' in df:
        earliest_year_birth = int(df['Birth Year'].min())
        print(f"The earliest year of birth is: {earliest_year_birth}")
    
        most_recent_year_birth = int(df['Birth Year'].max())
        print(f"The most recent year of birth is: {most_recent_year_birth}")
    
        most_common_year_birth = int(df['Birth Year'].mode()[0])
        print(f"The most common year of birth is: {most_common_year_birth}")
    else:
        print('\nBirth Year information not avaiable')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_data(df):
    """Displays data based on user input."""

    start_idx = 0
    end_idx = 5
    valid_responses = ['yes', 'no']
    
    display = input("Do you want to see 5 rows of data? Enter 'yes' or 'no': ").lower()

    while display not in valid_responses:
        print("Invalid input. Please enter 'yes' or 'no'.")
        display = input("Do you want to see 5 rows of data? Enter 'yes' or 'no': ").lower()

    while display == 'yes':
        if end_idx > len(df):
            print("No more data to display.")
            break

        print(df.iloc[start_idx:end_idx])
        display = input("Do you want to see the next 5 rows of data? Enter 'yes' or 'no': ").lower()

        while display not in valid_responses:
            print("Invalid input. Please enter 'yes' or 'no'.")
            display = input("Do you want to see the next 5 rows of data? Enter 'yes' or 'no': ").lower()
        
        start_idx += 5
        end_idx += 5



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
