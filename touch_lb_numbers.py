import csv
import json
import argparse
import time
import os

import re
from http.client import HTTPException
from itertools import chain
import platform

try:
    import requests
    from bs4 import BeautifulSoup
    from telebot import TeleBot
except ImportError:
    os.system('pip install requests beautifulsoup4 pyTelegramBotAPI')
    import requests
    from bs4 import BeautifulSoup
    from telebot import TeleBot
from telebot.util import smart_split

from scraping import get_numbers, do_number_booking, logger
from premium_numbers import get_premium_numbers


source_csv_fieldnames = ['id', 'first_name', 'last_name', 'father_name', 'mother_name',
                         'ref_number', 'birth_day', 'birth_month', 'birth_year', 'confirmation_code', 'id_type']

destination_csv_fieldnames = ['booked_number'] + source_csv_fieldnames


def load_first_row_to_book(file_name):
    with open(file_name) as numbers_file:
        reader = csv.DictReader(numbers_file, fieldnames=source_csv_fieldnames)
        return next(reader)


def remove_first_line(file_name):
    with open(file_name, 'r') as numbers_file:
        lines = numbers_file.readlines()
    with open(file_name, 'w') as numbers_file:
        numbers_file.writelines(lines[1:])


def save_booked_info(file_name, id, first_name, last_name, father_name, mother_name, ref_number, birth_day,
                     birth_month, birth_year, confirmation_code, booked_number, id_type):
    with open(file_name, 'a') as numbers_file:
        writer = csv.DictWriter(numbers_file, fieldnames=destination_csv_fieldnames)
        writer.writerow({
            'booked_number': booked_number, 'id': id, 'first_name': first_name, 'last_name': last_name,
            'father_name': father_name, 'mother_name': mother_name, 'ref_number': ref_number,
            'birth_day': birth_day, 'birth_month': birth_month, 'birth_year': birth_year,
            'confirmation_code': confirmation_code, 'id_type': id_type
        })


def load_numbers(numbers_file_name):
    try:
        with open(numbers_file_name) as numbers_file:
            return json.load(numbers_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_numbers(numbers, file_name):
    with open(file_name, 'w') as numbers_file:
        json.dump(numbers, numbers_file, indent=4)


def get_new_numbers(numbers, old_numbers):
    return set(numbers) - set(old_numbers)


def send_numbers(numbers, old_numbers, notification_bot, args):
    new_numbers = get_new_numbers(numbers, old_numbers)
    save_numbers(list(set(old_numbers).union(new_numbers)), args.old_numbers_file_name)
    if new_numbers:
        premium_number_categories, other_numbers = get_premium_numbers(new_numbers)
        premium_numbers_set = set(chain(*premium_number_categories.values()))
        if len(premium_numbers_set) > 0:
            logger.info('Premium numbers:')
            for category, p_numbers in premium_number_categories.items():
                if len(p_numbers) > 0:
                    logger.info(f'{category}: {p_numbers}')
            premium_numbers_set.update(load_numbers(args.available_premium_numbers))
            premium_numbers_set.difference_update(premium_number_categories['abc_only'])
            save_numbers(list(premium_numbers_set), args.available_premium_numbers)
        logger.info('Other new numbers:')
        for number in other_numbers:
            logger.info('Number: %s', number)
        for category, p_numbers in premium_number_categories.items():
            if len(p_numbers) > 0:
                send_telegram_message(
                    notification_bot, args.telegram_channel_id,
                    f'Premium numbers: {category}\n{" ".join(map(str, p_numbers))}'
                )
        if other_numbers:
            for start_index in range(0, len(other_numbers), 30):
                send_telegram_message(
                    notification_bot, args.telegram_channel_id,
                    " ".join([str(x) for x in other_numbers[start_index:start_index + 30]])
                )
    else:
        logger.info('No new numbers')


def send_telegram_message(bot, channel_id, message):
    for part in smart_split(message):
        if platform.node() == 'Hamza-XPS-15-7590':
            print('TELEGRAM:', message)
        else:
            bot.send_message(channel_id, part)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get the new numbers from touch.com.lb')
    parser.add_argument('--interval', '-i', type=int, default=3, help='Refresh interval in seconds')
    parser.add_argument('--old_numbers_file_name', '-o', type=str, default='old_numbers.json',
                        help='Old numbers file name')
    parser.add_argument('--telegram_token', '-t', type=str, help='Telegram bot token',
                        default='7380584915:AAFLp7ZTfnyBhqMPND5_D3V6Cbi7s-Y97To')
    parser.add_argument('--telegram_channel_id', '-c', type=str, help='Telegram channel id',
                        default='-1002224397023')
    parser.add_argument('--numbers-to-book', '-b', type=str, help='Numbers to book file',
                        default='numbers_to_book.csv')
    parser.add_argument('--booked-numbers', '-k', type=str, help='Booked numbers file',
                        default='booked_numbers.csv')
    parser.add_argument('--available-premium-numbers', '-p', type=str,
                        help='Available premium numbers file', default='available_premium_numbers.json')
    parser.add_argument('--numbers-source', '-s', type=str, help='Number source file')
    args = parser.parse_args()
    logger.info('Getting numbers from %s...', args.numbers_source or 'touch.com.lb')
    while True:
        try:
            if args.numbers_source:
                with open(args.numbers_source) as f:
                    numbers = [int(x) for x in re.findall(r'\d+', f.read())]
            else:
                numbers = get_numbers()
            if numbers:
                old_numbers = load_numbers(args.old_numbers_file_name)
                notification_bot = TeleBot(args.telegram_token, threaded=False)
                send_numbers(numbers, old_numbers, notification_bot, args)
                premium_numbers_list = load_numbers(args.available_premium_numbers)
                if len(premium_numbers_list):
                    info_row = load_first_row_to_book(args.numbers_to_book)
                    booked_message = do_number_booking(premium_numbers_list[0], **info_row)
                    if booked_message:
                        send_telegram_message(notification_bot, args.telegram_channel_id, booked_message)
                        remove_first_line(args.numbers_to_book)
                        save_booked_info(args.booked_numbers, booked_number=premium_numbers_list[0], **info_row)
                        premium_numbers_list.pop(0)
                        save_numbers([int(n) for n in premium_numbers_list], args.available_premium_numbers)
                else:
                    time.sleep(args.interval)
            else:
                logger.warning('No numbers found!')
                time.sleep(args.interval)
        except KeyboardInterrupt:
            logger.info('Stopped.')
            break
        except (requests.RequestException, HTTPException) as e:
            logger.error('Request failed: %s', e)
        except Exception as e:
            logger.exception('Unknown error occurred: %s', e)
