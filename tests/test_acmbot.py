#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright © 2014 Cameron Brandon White

import unittest
import datetime
import yaml
from modules.acmbot import *

class TestAcmBot(unittest.TestCase):
    

    def setUp(self):
        with open('./tests/events0.yaml') as f:
            self.events = yaml.load(f.read())

    def test_load_yaml(self):
        """ Makes sure that load_yaml will at least run """
        load_yaml(
            'http://acm.pdx.edu/files/events.yaml'
        )
    
    def test_events0_entrys(self):
        self.assertEqual(len(self.events), 4)
        event = self.events[0]
        self.assertEqual(event['title'], "Title 0")
        self.assertEqual(event['date'], datetime.date(2014, 3, 14))
        self.assertEqual(event['time'], '16:30')
        self.assertEqual(event['speaker'], 'Cameron White')
        self.assertEqual(event['description'], '"Description 0"\n')
        event = self.events[1]
        self.assertEqual(event['title'], "Title 1")
        self.assertEqual(event['date'], datetime.date(2014, 3, 13))
        self.assertEqual(event['time'], '17:31')
        self.assertEqual(event['speaker'], 'Adam Curry')
        self.assertEqual(event['description'], '"Description 1"\n')
        event = self.events[2]
        self.assertEqual(event['title'], "Title 2")
        self.assertEqual(event['date'], datetime.date(2014, 2, 21))
        self.assertEqual(event['time'], '15:12')
        self.assertEqual(event['speaker'], 'John C. Dvorak')
        self.assertEqual(event['description'], '"Description 2"\n')
        event = self.events[3]
        self.assertEqual(event['title'], "Title 3")
        self.assertEqual(event['date'], datetime.date(2014, 1, 14))
        self.assertEqual(event['time'], '02:44')
        self.assertEqual(event['speaker'], 'Bart Massey')
        self.assertEqual(event['description'], '"Description 3"\n')

    def test_events0_filter_take_date_0(self):
        # 2014-3-14
        date = datetime.date(2014, 3, 14)
        events = select_events(
                self.events, 
                lambda x: filter_take_date(x, date)
        )
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(event[1]['title'], "Title 0")
        self.assertEqual(event[1]['date'], datetime.date(2014, 3, 14))
        self.assertEqual(event[1]['time'], '16:30')
        self.assertEqual(event[1]['speaker'], 'Cameron White')
        self.assertEqual(event[1]['description'], '"Description 0"\n')

    def test_events0_filter_take_date_1(self):
        # 2014-3-14
        date = datetime.date(2014, 3, 13)
        events = select_events(
                self.events, 
                lambda x: filter_take_date(x, date)
        )
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(event[1]['title'], "Title 1")
        self.assertEqual(event[1]['date'], datetime.date(2014, 3, 13))
        self.assertEqual(event[1]['time'], '17:31')
        self.assertEqual(event[1]['speaker'], 'Adam Curry')
        self.assertEqual(event[1]['description'], '"Description 1"\n')

    def test_events0_filter_take_date_2(self):
        # 2014-3-14
        date = datetime.date(2014, 2, 21)
        events = select_events(
                self.events, 
                lambda x: filter_take_date(x, date)
        )
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(event[1]['title'], "Title 2")
        self.assertEqual(event[1]['date'], datetime.date(2014, 2, 21))
        self.assertEqual(event[1]['time'], '15:12')
        self.assertEqual(event[1]['speaker'], 'John C. Dvorak')
        self.assertEqual(event[1]['description'], '"Description 2"\n')

    def test_events0_filter_take_date_3(self):
        # 2014-3-14
        date = datetime.date(2014, 1, 14)
        events = select_events(
                self.events, 
                lambda x: filter_take_date(x, date)
        )
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(event[1]['title'], "Title 3")
        self.assertEqual(event[1]['date'], datetime.date(2014, 1, 14))
        self.assertEqual(event[1]['time'], '02:44')
        self.assertEqual(event[1]['speaker'], 'Bart Massey')
        self.assertEqual(event[1]['description'], '"Description 3"\n')

    def test_events0_command_date_0(self):
        # 2014-3-14
        events = command_date(self.events, datetime.date(2014, 3, 14))
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(event[1]['title'], "Title 0")
        self.assertEqual(event[1]['date'], datetime.date(2014, 3, 14))
        self.assertEqual(event[1]['time'], '16:30')
        self.assertEqual(event[1]['speaker'], 'Cameron White')
        self.assertEqual(event[1]['description'], '"Description 0"\n')

    def test_events0_command_date_1(self):
        # 2014-3-13
        events = command_date(self.events, datetime.date(2014, 3, 13))
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(event[1]['title'], "Title 1")
        self.assertEqual(event[1]['date'], datetime.date(2014, 3, 13))
        self.assertEqual(event[1]['time'], '17:31')
        self.assertEqual(event[1]['speaker'], 'Adam Curry')
        self.assertEqual(event[1]['description'], '"Description 1"\n')

    def test_events0_command_date_2(self):
        # 2014-2-21
        events = command_date(self.events, datetime.date(2014, 2, 21))
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(event[1]['title'], "Title 2")
        self.assertEqual(event[1]['date'], datetime.date(2014, 2, 21))
        self.assertEqual(event[1]['time'], '15:12')
        self.assertEqual(event[1]['speaker'], 'John C. Dvorak')
        self.assertEqual(event[1]['description'], '"Description 2"\n')

    def test_events0_command_date_3(self):
        # 2014-1-14
        events = command_date(self.events, datetime.date(2014, 1, 14))
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(event[1]['title'], "Title 3")
        self.assertEqual(event[1]['date'], datetime.date(2014, 1, 14))
        self.assertEqual(event[1]['time'], '02:44')
        self.assertEqual(event[1]['speaker'], 'Bart Massey')
        self.assertEqual(event[1]['description'], '"Description 3"\n')

    def test_events0_filter_take_date_range_0(self):
        """ Everything after 2014-1-1 """
        date = datetime.date(2014,1,1)
        events = select_events(
                self.events, 
                lambda x: filter_take_date_range(x, None, date)
        )
        self.assertEqual(len(events), 4)
        event = events[0]
        self.assertEqual(event[1]['title'], "Title 0")
        self.assertEqual(event[1]['date'], datetime.date(2014, 3, 14))
        self.assertEqual(event[1]['time'], '16:30')
        self.assertEqual(event[1]['speaker'], 'Cameron White')
        self.assertEqual(event[1]['description'], '"Description 0"\n')
        event = events[1]
        self.assertEqual(event[1]['title'], "Title 1")
        self.assertEqual(event[1]['date'], datetime.date(2014, 3, 13))
        self.assertEqual(event[1]['time'], '17:31')
        self.assertEqual(event[1]['speaker'], 'Adam Curry')
        self.assertEqual(event[1]['description'], '"Description 1"\n')
        event = events[2]
        self.assertEqual(event[1]['title'], "Title 2")
        self.assertEqual(event[1]['date'], datetime.date(2014, 2, 21))
        self.assertEqual(event[1]['time'], '15:12')
        self.assertEqual(event[1]['speaker'], 'John C. Dvorak')
        self.assertEqual(event[1]['description'], '"Description 2"\n')
        event = events[3]
        self.assertEqual(event[1]['title'], "Title 3")
        self.assertEqual(event[1]['date'], datetime.date(2014, 1, 14))
        self.assertEqual(event[1]['time'], '02:44')
        self.assertEqual(event[1]['speaker'], 'Bart Massey')
        self.assertEqual(event[1]['description'], '"Description 3"\n')

    def test_events0_filter_take_date_range_1(self):
        """ Everything after 2014-1-14 """
        date = datetime.date(2014,1,14)
        events = select_events(
                self.events, 
                lambda x: filter_take_date_range(x, None, date)
        )
        self.assertEqual(len(events), 4)
        event = events[0]
        self.assertEqual(event[1]['title'], "Title 0")
        self.assertEqual(event[1]['date'], datetime.date(2014, 3, 14))
        self.assertEqual(event[1]['time'], '16:30')
        self.assertEqual(event[1]['speaker'], 'Cameron White')
        self.assertEqual(event[1]['description'], '"Description 0"\n')
        event = events[1]
        self.assertEqual(event[1]['title'], "Title 1")
        self.assertEqual(event[1]['date'], datetime.date(2014, 3, 13))
        self.assertEqual(event[1]['time'], '17:31')
        self.assertEqual(event[1]['speaker'], 'Adam Curry')
        self.assertEqual(event[1]['description'], '"Description 1"\n')
        event = events[2]
        self.assertEqual(event[1]['title'], "Title 2")
        self.assertEqual(event[1]['date'], datetime.date(2014, 2, 21))
        self.assertEqual(event[1]['time'], '15:12')
        self.assertEqual(event[1]['speaker'], 'John C. Dvorak')
        self.assertEqual(event[1]['description'], '"Description 2"\n')
        event = events[3]
        self.assertEqual(event[1]['title'], "Title 3")
        self.assertEqual(event[1]['date'], datetime.date(2014, 1, 14))
        self.assertEqual(event[1]['time'], '02:44')
        self.assertEqual(event[1]['speaker'], 'Bart Massey')
        self.assertEqual(event[1]['description'], '"Description 3"\n')

    def test_events0_filter_take_date_range_2(self):
        """ Everything after 2014-1-14 """
        date = datetime.date(2014,1,15)
        events = select_events(
                self.events, 
                lambda x: filter_take_date_range(x, None, date)
        )
        self.assertEqual(len(events), 3)
        event = events[0]
        self.assertEqual(event[1]['title'], "Title 0")
        self.assertEqual(event[1]['date'], datetime.date(2014, 3, 14))
        self.assertEqual(event[1]['time'], '16:30')
        self.assertEqual(event[1]['speaker'], 'Cameron White')
        self.assertEqual(event[1]['description'], '"Description 0"\n')
        event = events[1]
        self.assertEqual(event[1]['title'], "Title 1")
        self.assertEqual(event[1]['date'], datetime.date(2014, 3, 13))
        self.assertEqual(event[1]['time'], '17:31')
        self.assertEqual(event[1]['speaker'], 'Adam Curry')
        self.assertEqual(event[1]['description'], '"Description 1"\n')
        event = events[2]
        self.assertEqual(event[1]['title'], "Title 2")
        self.assertEqual(event[1]['date'], datetime.date(2014, 2, 21))
        self.assertEqual(event[1]['time'], '15:12')
        self.assertEqual(event[1]['speaker'], 'John C. Dvorak')
        self.assertEqual(event[1]['description'], '"Description 2"\n')

    def test_events0_filter_take_date_range_3(self):
        """ Everything before 2014-1-1 """
        date = datetime.date(2014,1,1)
        events = select_events(
                self.events, 
                lambda x: filter_take_date_range(x, date, None)
        )
        self.assertEqual(len(events), 0)

    def test_events0_filter_take_date_range_4(self):
        """ Everything before 2014-1-14 """
        date = datetime.date(2014,1,14)
        events = select_events(
                self.events, 
                lambda x: filter_take_date_range(x, date, None)
        )
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(event[1]['title'], "Title 3")
        self.assertEqual(event[1]['date'], datetime.date(2014, 1, 14))
        self.assertEqual(event[1]['time'], '02:44')
        self.assertEqual(event[1]['speaker'], 'Bart Massey')
        self.assertEqual(event[1]['description'], '"Description 3"\n')

    def test_events0_filter_take_date_range_5(self):
        """ Everything before 2014-1-14 """
        date = datetime.date(2014,2,25)
        events = select_events(
                self.events, 
                lambda x: filter_take_date_range(x, date, None)
        )
        self.assertEqual(len(events), 2)
        event = events[0]
        self.assertEqual(event[1]['title'], "Title 2")
        self.assertEqual(event[1]['date'], datetime.date(2014, 2, 21))
        self.assertEqual(event[1]['time'], '15:12')
        self.assertEqual(event[1]['speaker'], 'John C. Dvorak')
        self.assertEqual(event[1]['description'], '"Description 2"\n')
        event = events[1]
        self.assertEqual(event[1]['title'], "Title 3")
        self.assertEqual(event[1]['date'], datetime.date(2014, 1, 14))
        self.assertEqual(event[1]['time'], '02:44')
        self.assertEqual(event[1]['speaker'], 'Bart Massey')
        self.assertEqual(event[1]['description'], '"Description 3"\n')

    def test_weekday_difference(self):
        self.assertEqual(weekday_difference(0,0), 0)
        self.assertEqual(weekday_difference(0,1), 1)
        self.assertEqual(weekday_difference(0,2), 2)
        self.assertEqual(weekday_difference(0,3), 3)
        self.assertEqual(weekday_difference(0,4), 4)
        self.assertEqual(weekday_difference(0,5), 5)
        self.assertEqual(weekday_difference(0,6), 6)
        self.assertEqual(weekday_difference(1,0), 6)
        self.assertEqual(weekday_difference(1,1), 0)
        self.assertEqual(weekday_difference(1,2), 1)
        self.assertEqual(weekday_difference(1,3), 2)
        self.assertEqual(weekday_difference(1,4), 3)
        self.assertEqual(weekday_difference(1,5), 4)
        self.assertEqual(weekday_difference(1,6), 5)
        self.assertEqual(weekday_difference(2,0), 5)
        self.assertEqual(weekday_difference(2,1), 6)
        self.assertEqual(weekday_difference(2,2), 0)
        self.assertEqual(weekday_difference(2,3), 1)
        self.assertEqual(weekday_difference(2,4), 2)
        self.assertEqual(weekday_difference(2,5), 3)
        self.assertEqual(weekday_difference(2,6), 4)
        self.assertEqual(weekday_difference(3,0), 4)
        self.assertEqual(weekday_difference(3,1), 5)
        self.assertEqual(weekday_difference(3,2), 6)
        self.assertEqual(weekday_difference(3,3), 0)
        self.assertEqual(weekday_difference(3,4), 1)
        self.assertEqual(weekday_difference(3,5), 2)
        self.assertEqual(weekday_difference(3,6), 3)
        self.assertEqual(weekday_difference(4,0), 3)
        self.assertEqual(weekday_difference(4,1), 4)
        self.assertEqual(weekday_difference(4,2), 5)
        self.assertEqual(weekday_difference(4,3), 6)
        self.assertEqual(weekday_difference(4,4), 0)
        self.assertEqual(weekday_difference(4,5), 1)
        self.assertEqual(weekday_difference(4,6), 2)
        self.assertEqual(weekday_difference(5,0), 2)
        self.assertEqual(weekday_difference(5,1), 3)
        self.assertEqual(weekday_difference(5,2), 4)
        self.assertEqual(weekday_difference(5,3), 5)
        self.assertEqual(weekday_difference(5,4), 6)
        self.assertEqual(weekday_difference(5,5), 0)
        self.assertEqual(weekday_difference(5,6), 1)
        self.assertEqual(weekday_difference(6,0), 1)
        self.assertEqual(weekday_difference(6,1), 2)
        self.assertEqual(weekday_difference(6,2), 3)
        self.assertEqual(weekday_difference(6,3), 4)
        self.assertEqual(weekday_difference(6,4), 5)
        self.assertEqual(weekday_difference(6,5), 6)
        self.assertEqual(weekday_difference(6,6), 0)

if __name__ == '__main__':
    unittest.main()
