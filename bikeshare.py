import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city_complete = False
    city_list = sorted(CITY_DATA.keys())
    while not city_complete:
        city = input("Choose city from {}: ".format(city_list))
        if CITY_DATA.get(city):
            city_complete = True
        else:
            print("Not a vaild city choice.  Please re-enter. \n")

    # get user input for month (all, january, february, ... , june)
    month_complete = False
    #month_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month_list = ['all']
    for mon in MONTHS:
        month_list.append(mon)
    while not month_complete:
        month = input("Choose month to analyze \nfrom {}: ".format(month_list))
        if month in month_list:
            month_complete = True
        else:
            print("Not a valid month choice.  Please re-enter \n")


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_complete = False
    #day_list = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day_list = ['all']
    for da in DAYS:
        day_list.append(da)
    while not day_complete:
        day = input("Choose day of week to analyze \nfrom {}: ".format(day_list))
        if day in day_list:
            day_complete = True
        else:
            print("Not a valid day choice.  Please re-enter \n")

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
    df = pd.read_csv(CITY_DATA[city])

    # pre-process 'Start Time' column to extract month and DOW data
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

   # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        #months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = MONTHS.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        #days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        dayweek = DAYS.index(day)
        df = df[df['day_of_week']==dayweek]

    rawdisp = True
    while rawdisp:
        user_req = input("Display first 5 lines of filtered data before continuing? (yes/no)")
        if user_req in ['no', 'n', 'No', 'N', 'NO']:
            rawdisp = False
        else:
            print("\n Filtered data frame \n")
            print(df.head())


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    #df['month'] = df['Start Time'].dt.month done in load_data
    popular_month = df['month'].mode()[0]
    print('Most Frequent Start Month:', MONTHS[popular_month-1].title())


    # display the most common day of week
    #df['month'] = df['Start Time'].dt.month  done in load_data
    popular_day = df['day_of_week'].mode()[0]
    print('Most Frequent Start Day of Week:', DAYS[popular_day].title())

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour: {}:00 - {}:00'.format(popular_hour,popular_hour+1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    rawdisp = True
    while rawdisp:
        user_req = input("Display first 5 lines of filtered data before continuing? (yes/no)")
        if user_req in ['no', 'n', 'No', 'N', 'NO']:
            rawdisp = False
        else:
            print("\n Filtered data frame \n")
            print(df.head())


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print("Most common starting station: {}".format(popular_start))

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print("Most common endpoint: {}".format(popular_end))

    # display most frequent combination of start station and end station trip
    combos = df.groupby(['Start Station', 'End Station']).size()
    max_combo = combos[combos==combos.max()]
    print("Most common combination starts at {} and ends at {}.".format(max_combo.index[0][0],max_combo.index[0][1]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    rawdisp = True
    while rawdisp:
        user_req = input("Display first 5 lines of aggregated rides for  station pairs? (yes/no)")
        if user_req in ['no', 'n', 'No', 'N', 'NO']:
            rawdisp = False
        else:
            print("\n Filtered data frame \n")
            print(combos.head())



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = (df['End Time'] - df['Start Time']).dt.total_seconds()

    # display mean travel time

    print("Mean travel time in seconds: {}".format(df['Travel Time'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    rawdisp = True
    while rawdisp:
        user_req = input("Display first 5 lines of calculated travel times? (yes/no)")
        if user_req in ['no', 'n', 'No', 'N', 'NO']:
            rawdisp = False
        else:
            print("\n Filtered data frame \n")
            print(df[['Travel Time', 'Start Time', 'End Time']].head())



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    df['User Type'] = df['User Type'].fillna("Not Specified")
    print("\nUser Type Distribution\n")
    print(df['User Type'].value_counts())

    # Display counts of gender
    try:
        df['Gender'] = df['Gender'].fillna("Not Specified")
        print("\n\nGender Distribution\n")
        print(df['Gender'].value_counts())
    except:
        print("\nGender distribution not available for these data")

    # Display earliest, most recent, and most common year of birth
    try:
        print("\n\nAge Data\n")
        print("Earliest birth year: {}".format(int(df['Birth Year'].min())))
        print("Most recent birth year: {}".format(int(df['Birth Year'].max())))
        print("Most common birth year: {}".format(int(df['Birth Year'].mode()[0])))
    except:
        print("Birth year not available for these data")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    rawdisp = True
    while rawdisp:
        user_req = input("Display first 5 lines of calculated travel times? (yes/no)")
        if user_req in ['no', 'n', 'No', 'N', 'NO']:
            rawdisp = False
        else:
            print("\n Filtered user data \n")
            try:
                print(df[['User Type', 'Gender', 'Birth Year']].head())
            except:
                print(df['User Type'].head())


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print("Analyzing data for {} in {} on {}.\n".format(city, month, day))
        #print(df.head())

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
