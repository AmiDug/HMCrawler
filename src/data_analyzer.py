#!/usr/bin/env python3

def return_price_average(store_list):
    """
    Takes in all store items the user searched for and outputs the average price for them.
    :param store_list:
    :return:
    """
    price_list = []
    for item in store_list:
        price_list.append(item['price'])
    if len(price_list) == 0:
        return 0
    return sum(price_list) / len(price_list)

def return_rating_average(store_list):
    """
    Takes in all store items the user searched for and outputs the average rating for them.
    :param store_list:
    :return:
    """
    rating_list = []
    for item in store_list:
        rating_list.append(item['rate'])
    if len(rating_list) == 0:
        return 0
    return sum(rating_list) / len(rating_list)

def return_count_average(store_list):
    """
    Takes in all store items the user searched for and outputs the average amount of them.
    :param store_list:
    :return:
    """
    print(store_list)
    count_list = []
    for item in store_list:
        count_list.append(item['count'])
    if len(count_list) == 0:
        return 0
    return sum(count_list) / len(count_list)