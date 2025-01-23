import time
import pandas as pd
import numpy as np

# 도시 이름과 데이터 파일 경로 매핑
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    사용자로부터 분석할 도시, 월, 요일 입력 받기
    """
    print('미국 자전거 공유 데이터를 분석합니다!')

    city = input(f"도시를 선택하세요 ({', '.join(CITY_DATA.keys())}): ").strip().lower()
    while city not in CITY_DATA:
        city = input(f"잘못된 입력입니다. 도시를 다시 입력하세요 ({', '.join(CITY_DATA.keys())}): ").strip().lower()

    month = input("필터링할 월을 입력하세요 (all, january, february, ... , december): ").strip().lower()
    valid_months = ['all'] + [m.lower() for m in pd.date_range('2023-01-01', '2023-12-01', freq='MS').strftime('%B')]
    while month not in valid_months:
        month = input("잘못된 입력입니다. 월을 다시 입력하세요: ").strip().lower()

    day = input("필터링할 요일을 입력하세요 (all, monday, tuesday, ... , sunday): ").strip().lower()
    valid_days = ['all'] + [d.lower() for d in pd.date_range('2023-01-01', '2023-01-07').strftime('%A')]
    while day not in valid_days:
        day = input("잘못된 입력입니다. 요일을 다시 입력하세요: ").strip().lower()

    print(f"\n선택된 필터 - 도시: {city}, 월: {month}, 요일: {day}\n")
    return city, month, day

def load_and_filter_data(city, month, day):
    """
    데이터 로드 및 필터링
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month_name().str.lower()
    df['Day'] = df['Start Time'].dt.day_name().str.lower()

    if month != 'all':
        df = df[df['Month'] == month]
    if day != 'all':
        df = df[df['Day'] == day]

    return df

def calculate_stats(df):
    """
    주요 통계를 계산하고 출력
    """
    print("\n[시간 통계]")
    most_common_month = df['Month'].mode()[0]
    most_common_day = df['Day'].mode()[0]
    most_common_hour = df['Start Time'].dt.hour.mode()[0]
    print(f"가장 흔한 월: {most_common_month}")
    print(f"가장 흔한 요일: {most_common_day}")
    print(f"가장 흔한 시간: {most_common_hour}시")

    print("\n[역 통계]")
    most_common_start_station = df['Start Station'].mode()[0]
    most_common_end_station = df['End Station'].mode()[0]
    common_route = (df['Start Station'] + ' -> ' + df['End Station']).mode()[0]
    print(f"빈도 가장 높은 출발지: {most_common_start_station}")
    print(f"빈도 가장 높은 도착지: {most_common_end_station}")
    print(f"빈도 가장 높은 경로: {common_route}")

    print("\n[여행 시간 통계]")
    total_travel_time = df['Trip Duration'].sum()
    mean_travel_time = df['Trip Duration'].mean()
    print(f"총 여행 시간: {total_travel_time}초")
    print(f"평균 여행 시간: {mean_travel_time:.2f}초")

    print("\n[사용자 통계]")
    print(df['User Type'].value_counts())
    if 'Gender' in df:
        print(df['Gender'].value_counts())
    if 'Birth Year' in df:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print(f"가장 오래된 출생 연도: {earliest_year}")
        print(f"가장 최근 출생 연도: {most_recent_year}")
        print(f"가장 많은 출생 연도: {most_common_year}")

def display_raw_data(df):
    """
    원시 데이터를 5행씩 출력
    
    """
    start = 0
    while True:
        show_data = input("원시 데이터를 5행씩 더 보시겠습니까? (yes/no): ").lower()
        if show_data == 'yes':
            print(df.iloc[start:start + 5])
            start += 5
            if start >= len(df):
                print("\n더 이상 데이터가 없습니다.")
                break
        elif show_data == 'no':
            break
        else:
            print("잘못된 입력입니다. 'yes' 또는 'no'를 입력해주세요.")

def main():
    """
    프로그램 실행 루프
    """
    while True:
        city, month, day = get_filters()
        df = load_and_filter_data(city, month, day)

        if df.empty:
            print("선택한 필터에 해당하는 데이터가 없습니다.")
        else:
            display_raw_data(df)
            calculate_stats(df)

        restart = input("\n프로그램을 다시 실행하시겠습니까? (yes/no): ").lower()
        if restart != 'yes':
            print("프로그램을 종료합니다. 감사합니다!")
            break

if __name__ == "__main__":
    main()
