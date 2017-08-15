# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pandas as pd

seats = pd.read_csv(r'seat_1.csv')
seat = seats.loc[:, ['group_code', 'row_num', 'column_num', 'hall_id']]

shows = pd.read_csv(r'showtime.csv')
show = shows.loc[:, ['id', 'hall_id', 'cinema_id']]

# result = pd.DataFrame(columns=['id', 'hall_id', 'cinema_id', 'group_code', 'row_num', 'column_num'])
temp = pd.merge(show, seat, on=['hall_id'])
temp.to_csv(r'test.csv', header=False, index=False)
