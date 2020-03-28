import time
import math
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DATA = { 'january': 1,
                'february': 2,
                'march': 3,
                'april': 4,
                'may': 5,
                'june': 6}

WEEK_DATA = { 'monday': 0,
                'tuesday': 1,
                'wednesday': 2,
                'thursday': 3,
                'friday': 4,
                'saturday': 5,
                'sunday': 6}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print()

    while True:
        print('Which city would you like to explore?')
        city = input("Enter: 'Chicago', 'New York City', or 'Washington' - ").lower()
        print()
        if city not in CITY_DATA:
            print("**ERROR!** Please enter 'Chicago', 'New York City', or 'Washington'")
            continue
        city = CITY_DATA[city]
        break

    while True:
        f1 = input("Would you like to filter the data by a month and/or a week? Enter: 'yes' or 'no' - ").lower()
        print()
        if f1 =='yes':
            f1 = True
        elif f1 =='no':
            f1 = False
        else:
            print("You did not enter a valid choice! Please enter 'yes' or 'no'.")
            continue
        break

    while True:
        if f1:
            f2 = input("Would you like to filter by 'month' or 'day' or 'both'? - ").lower()
            print()
            if f2 =='month':
                print('Which month are you interested in?')
                month = input("Enter: 'January', 'February', 'March', 'April', 'May', 'June' - ").lower()
                print()
                if month not in MONTH_DATA:
                    print('**ERROR!** We do not have data for that month. Please enter one of the months listed above')
                    continue
                month = MONTH_DATA[month]
                day ='all'
            elif f2 =='day':
                print('Which day of the week would you like to analyze?')
                day = input("Enter: 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' - ").lower()
                print()
                if day not in WEEK_DATA:
                    print('**ERROR!** Please check your spelling and/or enter the full name of the day as listed above')
                    continue
                day = WEEK_DATA[day]
                month ='all'
            elif f2 =='both':
                print('Which month are you interested in?')
                month = input('January, February, March, April, May, June - ').lower()
                print()
                if month not in MONTH_DATA:
                    print('**ERROR!** We do not have data for that month. Please enter one of the months listed above')
                    continue
                month = MONTH_DATA[month]
                print('And which day of the week would you like to analyze?')
                day = input('Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday - ').lower()
                print()
                if day not in WEEK_DATA:
                    print('**ERROR!** Please check your spelling and/or enter the full name of the day as listed above')
                    continue
                day = WEEK_DATA[day]
            else:
                print('**ERROR!** We do not have data for that entry. Please try again')
                continue
            break
        else:
            day = 'all'
            month = 'all'
            break

    print('-'*100)
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
    df = pd.read_csv(city)
    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.dayofweek
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    if day != 'all':
        df = df[df['day_of_week'] == day]
    if month != 'all':
        df = df[df['month'] == month]
    df.drop('day_of_week', axis=1, inplace=True)
    df.drop('month', axis=1, inplace=True)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.dayofweek
    df['month'] = pd.to_datetime(df['Start Time']).dt.month

    most_freq_month = df['month'].mode()[0]
    for num in MONTH_DATA:
        if MONTH_DATA[num] == most_freq_month:
            most_freq_month = num.title()
    print('The most common month for travel is: {}'.format(most_freq_month))

    most_freq_day = df['day_of_week'].mode()[0]
    for num in WEEK_DATA:
        if WEEK_DATA[num] == most_freq_day:
            most_freq_day = num.title()
    print('The most common day of week for travel is: {}'.format(most_freq_day))

    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour
    most_freq_hour = df['hour'].mode()[0]
    print('The most common hour for travel is: {}'.format(most_freq_hour))
    df.drop('hour', axis=1, inplace=True)
    df.drop('day_of_week', axis=1, inplace=True)
    df.drop('month', axis=1, inplace=True)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print()
    print('The most commonly used start station was: {}'.format(df['Start Station'].mode()[0]))

    print()
    print('Most commonly used end station was: {}'.format(df['End Station'].mode()[0]))

    print()
    most_freq_station_comb = df['Start Station'] + ' to ' + df['End Station']
    print('The most frequnt combination of start station to end station trip was: {}'.format(most_freq_station_comb.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    travel_durations = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])

    print()
    td_sum = df['Trip Duration'].sum()
    print('Total travel time: ' + str(td_sum))

    print()
    td_mean = df['Trip Duration'].mean()
    print('Mean travel time: ' + str(td_mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Statistics...\n')
    start_time = time.time()

    print()
    types_of_users = df.groupby('User Type', as_index=False).count()
    print('Number of user types are: ')
    for i in range(len(types_of_users)):
        print('{}s: {}'.format(types_of_users['User Type'][i], types_of_users['Start Time'][i]))

    print()
    if 'Gender' not in df:
        print('Sorry, user gender data not avalible for this city')
    else:
        gender_of_users = df.groupby('Gender', as_index=False).count()
        print('The user gender counts are: ')
        for i in range(len(gender_of_users)):
            print('{}s: {}'.format(gender_of_users['Gender'][i], gender_of_users['Start Time'][i]))

    print()
    if 'Birth Year' not in df:
        print('Sorry, user birth data is not available for this city.')
    else:
        birth = df.groupby('Birth Year', as_index=False).count()
        print('The earliest year of birth was: {}.'.format(int(birth['Birth Year'].min())))
        print('The most recent year of birth was: {}.'.format(int(birth['Birth Year'].max())))
        print('The most common year of birth year was: {}.'.format(int(birth.iloc[birth['Start Time'].idxmax()]['Birth Year'])))

    print("\nThis query took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    d1 = input("Would you like to view some of the raw trip data? Enter 'yes' or 'no' - ").lower()
    print()
    if d1 == 'yes':
        d1 = True
    elif d1 == 'no':
        d1 = False
    else:
        print("**ERROR!** Please enter 'yes' or 'no' ")
        display_data(df)
        return

    if d1:
        while True:
            for i in range(5):
                print(df.iloc[i])
                print()
            d1 = input("Would you like to see another five trips? Enter 'yes' or 'no' - ").lower()
            if d1 == 'yes':
                continue
            elif d1 == 'no':
                break
            else:
                print("**ERROR!** Please enter 'yes' or 'no' ")
                return


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        print()
        if restart != 'yes':
            break

if __name__ == "__main__":
	main()
