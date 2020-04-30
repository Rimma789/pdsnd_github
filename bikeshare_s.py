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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs  
           
    i = 1
    while i < 100:        
        city = input('Would you like to see data for Chicago, New York City or Washington? ')
        city = city.lower()
        if city == 'chicago' or city == 'new york city' or city == 'washington':
            break               
        i += 1
        print('Try again')    

    # TO DO: get user input for month (all, january, february, ... , june)
   
    y = input('Would you like to filter the data by month, day, or not at all? Type "none" for no time filter?\n')
    if y == 'none':
        month = 'all'
        day = 'all'
    elif y == 'month':
        month = (input('Which month? January, February, March, April, May, June? Please type out the full month name.\n')).lower()
        day = 'all'
    elif y == 'day':
        """
        Asks user for an integer to specify day of week to reduce typos.
        
        Returns:
            (str) day_name - name of the day of week.
        """    
        def day_of_week(number):
            list = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
            number = number - 1
            day_name = list[number] 
            return day_name
        
        while True:
            try: 
                day_num = int(input('Which day? Please type your response (e.g. 1=Sunday).\n'))
                break
            except ValueError:
                print('That is not a valid number')
        day = day_of_week(day_num)
        
        
        month = 'all'
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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)
    # TO DO: display the most common day of week
    df['day'] = df['Start Time'].dt.weekday_name
    popular_day = df['day'].mode()[0]
    print('Most Popular Day:', popular_day) 

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_st = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_st)

    # TO DO: display most commonly used end station
    popular_end_st = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_st)

    # TO DO: display most frequent combination of start station and end station trip
    df.insert(5, 'Most Popular Station Combination', df['Start Station'] + ' / ' + df['End Station']) 
    popular_st_comb = (df['Most Popular Station Combination']).mode()[0]
    print('Most Popular Station Combination:', popular_st_comb)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = (sum(df['Trip Duration'])/3600)
    print('Total Travel Time:', total_travel_time,'h')

    # TO DO: display mean travel time
    mean_travel_time = ((df['Trip Duration'].mean())/3600)
    print('Mean Travel Time:', mean_travel_time,'h')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    
    if city == 'washington':
        print('There no data for gender and year of birth available.')
    else: 
        user_gender = df['Gender'].value_counts()
        print(user_gender)
        print('Earliest Year of Birth:', int(df['Birth Year'].min()))
        print('Most Recent Year of Birth:', int(df['Birth Year'].max()))
        print('Most Common Year of Birth:', int(df['Birth Year'].mode()))
    # TO DO: Display counts of gender
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
                
        raw_data_yes = True
        while raw_data_yes:
            raw_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
            if raw_data.lower() == 'yes':
                print(df.head())
                raw_data_yes = True
            if raw_data.lower() == 'no':
                break
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
