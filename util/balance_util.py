import os
import pandas as pd
import datetime
import numpy as np


def getEveryDay(begin_date, end_date):
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    periods = (end_date-begin_date).days
    dates = pd.date_range(begin_date, periods=periods+1, freq='D')
    date_list = dates.to_native_types().tolist()
    return date_list


def fill(number):
    if pd.isna(number) == True:
        return 0
    else:
        return number


def modify_amount(num_string):
    num_string = num_string.replace(',', '')
    num = float(num_string)
    return num


def tx_to_change(txdata):
    txdata['amount'] = txdata['amount'].apply(modify_amount)
    subdata_from = txdata.loc[:, ['from_address', 'amount', 'date']]
    subdata_from['amount'] = -subdata_from['amount']
    subdata_from = subdata_from.rename(
        index=str, columns={'from_address': 'account'})
    subdata_to = txdata.loc[:, ['to_address', 'amount', 'date']]
    subdata_to = subdata_to.rename(
        index=str, columns={'to_address': 'account'})
    data_total = subdata_from.append(subdata_to)
    data_total = data_total.groupby(['account', 'date'])['amount'].agg(sum)
    data_total = pd.DataFrame(data_total)
    data_total = data_total.reset_index()
    return data_total


def get_tag(data):
    data_grouped = data.groupby(['account'])['date', 'amount'].apply(
        lambda x: x.sort_values(by='date', ascending=True))
    data_grouped['balance'] = data_grouped.groupby(
        ['account'])['amount'].apply(lambda x: x.cumsum())
    data_tag = data_grouped.groupby(
        ['account'])['balance'].apply(lambda x: x.max())
    data_tag = pd.DataFrame(data_tag).reset_index()
    balance_list = data_tag['balance'].tolist()
    retail_amount = np.percentile(balance_list, 75)
    retailor_list = data_tag[data_tag['balance']
                             <= retail_amount]['account'].tolist()
    return retailor_list


def get_retailor(retailor_list, data):
    data['account'] = data['account'].map(
        lambda x: 'retailor' if x in retailor_list else x)
    data = pd.DataFrame(data.groupby(['account', 'date'])[
                        'amount'].agg(sum)).reset_index()
    return data


def full_day(data):
    dict_this = {'account': [], 'date': []}
    date_list = getEveryDay(data.date.min(), data.date.max())
    accounts = set(data.account.tolist())
    for account in accounts:
        for date in date_list:
            dict_this['date'].append(date)
            dict_this['account'].append(account)
    full_day = pd.DataFrame(dict_this)
    return full_day


def main(txdata):
    data = tx_to_change(txdata)
    retailor_list = get_tag(data)
    data = get_retailor(retailor_list, data)
    full_list = full_day(data)
    full_list = pd.merge(full_list, data, how='left', on=[
                         'account', 'date']).fillna(0)
    full_list = full_list.groupby(['account'])['date', 'amount'].apply(
        lambda x: x.sort_values(by='date', ascending=True))
    full_list['balance'] = full_list.groupby(
        ['account'])['amount'].apply(lambda x: x.cumsum())
    full_list = full_list.reset_index()
    full_list = full_list.reindex(columns=['account', 'date', 'balance'])
    full_list = full_list.drop(full_list[full_list['balance'] == 0].index)
    return full_list
