import os
import errno
from datetime import datetime, timedelta
import CONFIG

def open_file_by_date(foldername, filename):
    """
    python의 open 인스턴트를 반환.
    csv writer가 파일을 open할떄 사용한다.
    :param filename:
    :param foldername:
    :return:
    """
    total_file_path = get_file_path(foldername, filename)
    check_and_make_dir(total_file_path)  # 폴더 있는지 체크하고 없으면 만들어줌
    f = open(total_file_path, 'a', encoding='cp949', newline='')
    return f

def get_file_path(foldername, filename):
    """
    folder, file 이름을 주면 config의 기본 path를 바탕으로 full file path(csv)를 반환.
    이는 csv파일을 열때 사용되기도 하고, pandas에서 to_csv를 할떄 사용되기도 한다.
    :param foldername:
    :param filename:
    :return:
    """

    now = datetime.today()
    hour = now.hour
    minute = now.minute

    # D+0일 오전 7시 30분 - D+1일 오전 7시 30분까지는 D+0로 본다. <오전 7시 30분이 날짜가 바뀌는 기점>
    # CONFIG에서 바꿔줄 수 있음

    if hour < CONFIG.TIMEINFO['CRITERIA_HOUR']:
        date = now.date() - timedelta(days=1)
    elif hour == CONFIG.TIMEINFO['CRITERIA_HOUR'] and minute < CONFIG.TIMEINFO['CRITERIA_MINUTE']:
        date = now.date() - timedelta(days=1)
    else:
        date = now.date()

    date = str(date)

    file_path = CONFIG.IOINFO['PATH'] + date + "\\" + foldername + "\\"
    file_name = date + "_" + filename + ".csv"
    total_file_path = file_path + file_name

    return total_file_path

def check_and_make_dir(total_file_path):
    """
    filepath를 주면 하위 폴더들이 존재하지 않으면 생성해준다.
    :param total_file_path:
    :return:
    """
    if not os.path.exists(os.path.dirname(total_file_path)):
        try:
            os.makedirs(os.path.dirname(total_file_path))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

# if __name__ == "__main__":
#     check_and_make_dir("D:\\MMDATA\\2019-01-04\\a\\b\\c\\d.csv")
