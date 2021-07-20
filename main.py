import csv
import re
import time
from typing import List, Dict
import pyperclip


RESULT_FILENAME = 'result.csv'
CONFIG_FILEPATH = 'config.txt'


def write2csv(data: List[object]) -> None:
    with open(RESULT_FILENAME, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)
        print(f"成功写入：{data[0]}, {data[1]}")


def parse_data(data: str, url_tag="下单链接：", coupon_tag="元优惠券") -> Dict[str, str]:
    return {
        'url': re.search(f'({url_tag})'+r'(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]',
                         data, flags=0).group().replace(url_tag, ''),
        'coupon': re.search(r'(\d+\.\d+)'+f'{coupon_tag}', data, flags=0).group().replace(coupon_tag, '')
    }


def read_data_from_clipboard() -> str:
    # 下边2021-07-20的数据
    test_data = """
    居家日用飞科男充电式电动全身水洗胡须刀
    券后【77.40元】包邮秒杀
    20.00元优惠券：https://uland.taobao.com/quan/detail?sellerId=2209566538149&activityId=b40c1b492cf74f23b470be80f3477902
    下单链接：https://item.taobao.com/item.htm?id=645379545878
    全身水洗，多功能剃须，弹性贴面，持久续航，智能科技，剃须无残留，型男专用，魅力重现，现代型男潮流标配！"""
    return pyperclip.paste()


def read_config(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            config = tuple(i.strip() for i in f.readlines())
            return config
    except FileNotFoundError:
        return None, None


def main(data):
    url_tag, coupon_tag = read_config(CONFIG_FILEPATH)
    try:
        if url_tag and coupon_tag:
            res = parse_data(data, url_tag, coupon_tag)
        else:
            res = parse_data(data)
        write2csv([res.get('url', ''), res.get('coupon', '')])
    except Exception as e:
        print("解析失败：", e)
        print("data内容为: ", data)


if __name__ == '__main__':
    last_data = read_data_from_clipboard()
    while True:
        try:
            data = read_data_from_clipboard()
            if last_data == data:
                continue
            else:
                last_data = data
                main(data)
            time.sleep(0.1)
        except Exception as e:
            print('解析失败')
