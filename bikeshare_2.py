import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # set lists for comparison
    cities = ['Chicago', 'New York City', 'Washington']
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city=input('\nPlease enter which city you would like data for: Chicago, New York City or Washington: \n').title()
        print('\nYou have chosen',city,'as your city')
        user_confirm=input('\nIs this correct? Y/N\n').title()
        if user_confirm not in ('Y', 'N') or user_confirm == 'N':
            print('Please select city again')
            continue
        elif city not in cities:
            print('Invalid city chosen, please try again')
            continue
        else:
             #clear user_confirm for use later and break choosing city loop
            user_confirm=''
            print('-'*40)
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month=input('\nPlease enter which month you would like data from: January, February, March, April, May, June, All: \n').title()
        print('\nYou have chosen',month,'as your chosen month')
        user_confirm=input('\nIs this correct? Y/N\n').title()
        if user_confirm not in ('Y', 'N') or user_confirm == 'N':
            print('Please select month again')
            continue
        elif month not in months:
            print('Invalid month chosen, please try again and follow the naming convention in the examples given')
            continue
        else:
            #clear user_confirm for use later and break choosing month loop
            user_confirm=''
            print('-'*40)
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day=input('\nPlease enter which day would like data from: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, All: \n').title()
        print('\nYou have chosen',day,'as your chosen day')
        user_confirm=input('\nIs this correct? Y/N\n').title()
        if user_confirm not in ('Y', 'N') or user_confirm == 'N':
            print('Please select day again')
            continue
        elif day not in days:
            print('Invalid day chosen, please try again and follow the naming convention in the examples given')
            continue
        else:
            break
            print('-'*40)

    print('-'*40)
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

    #Load data into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    #Need to convert start time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Create month and day columns in data frame
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    #Filter on month
    if month != 'All':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month_index = (months.index(month)) + 1
        df = df[df['month'] == month_index]

    #Filter on day of week
    if day != 'All':
            df=df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Get the most common month
    pop_month = df['month'].mode()[0]

    # Make popular month output more readable by turning month numbers to strings
    if pop_month == 1:
        pop_month = 'January'
    elif pop_month == 2:
        pop_month = 'February'
    elif pop_month == 3:
        pop_month = 'March'
    elif pop_month == 4:
        pop_month = 'April'
    elif pop_month == 5:
        pop_month = 'May'
    elif pop_month == 6:
        pop_month = 'June'
    #Display the most common month
    print('The most popular month is... ', pop_month)


    # display the most common day of week, no readability change needed as already getting day_name
    pop_day = df['day_of_week'].mode()[0]
    print('The most popular day of the week is...', pop_day)


    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    pop_hour = df['hour'].mode()[0]

    #convert 24 hour to 12 hour time. strptime not needed as only using ints so simple if statement works
    if pop_hour < 12:
        print('The most popular starting hour is... ',pop_hour,'AM')
    elif pop_hour >= 12:
        if pop_hour > 12:
            pop_hour -=12
        print('The most popular starting hour is...',pop_hour,'PM')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    # just get mode of start station data frame and print
    pop_start_station = df['Start Station'].mode()[0]
    print('The most popular starting station is...',pop_start_station)

    # display most commonly used end station
    # same technique but for end station
    pop_end_station = df['End Station'].mode()[0]
    print('The most popular ending station is...',pop_end_station)

    # display most frequent combination of start station and end station trip
    # create combined_station series and get the most common result
    combined_station = df["Start Station"] + " to " + df["End Station"]
    pop_combined_station=combined_station.mode()[0]
    print('The most popular combination of start and end stations are...{}'.format(pop_combined_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_dur = df['Trip Duration'].sum()
    minute, second = divmod(total_dur, 60)
    hour, minute = divmod(minute, 60)
    print('The total travel time is... {} hours, {} minutes, and {} seconds'.format(hour,minute,second))

    # display mean travel time
    mean_dur = round(df['Trip Duration'].mean())
    minute, second = divmod(mean_dur, 60)
    #if minute is greater than 60 convert to hours to make it more readable
    if minute > 60:
        hour, minute = divmod(minute, 60)
        print('The average travel time is... {} hours, {} minutes, and {} seconds'.format(hour,minute,second))
    else:
        print('The average travel time is... {} minutes, {} seconds'.format(minute,second))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    subs = len(df[df['User Type'] == 'Subscriber'])
    cust = len(df[df['User Type'] == 'Customer'])
    print('\nCustomer type data below:')
    print('Number of subcribers:', subs)
    print('Number of customers:', cust)

    # Display counts of gender need to use try/except as some data files do not have gender data
    try:
        male_count = len(df[df['Gender'] == 'Male'])
        female_count = len(df[df['Gender'] == 'Female'])
    except:
        print('No user gender data available for you city selection:',city)
    else:
        print('\nUser gender information below')
        print('Number of male users:',male_count)
        print('Number of female users:',female_count)

    # Display earliest, most recent, and most common year of birth
    # Using int to remove .0 from year values, otherwise would print 1999.0
    # Using try/except as some data files do not have birth data
    try:
        oldest = int(df['Birth Year'].min()) #oldest
        youngest = int(df['Birth Year'].max()) #youngest
        common = int(df['Birth Year'].mode()) #common

        print('\nBirth year data below:')
        print('The oldest users birth year is...',oldest)
        print('The youngest users birth year is...',youngest)
        print('The most common birthday is...',common)
    except:
        print('No user birth year data available for your city selection:',city)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Asks user if they would like to see raw data and if so displays it until user instructs to stop"""

    start_row = 0
    max_row = 5
    length_df = len(df.index)

    # While checks to see if there are more rows to display
    while start_row < length_df:
        raw_confirm = input('\nWould you like to see raw data? Y/N').title()
        if raw_confirm == 'Y':
            print('\nDisplaying 5 rows of raw data')
            if max_row > length_df:
                max_row = length_df
            print(df.iloc[start_row:max_row])
            start_row += 5
            max_row += 5
        else:
            print('\nUser did not select Y')
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Y/N.\n').title()
        if restart != 'Y':
            print('Thank you, exiting...')
            break


if __name__ == "__main__":
	main()
