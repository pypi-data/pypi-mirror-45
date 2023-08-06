#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pretty_table_printer` package."""

import pytest
from pretty_table_printer import pretty_table_printer


from datetime import datetime
from decimal import Decimal

from pretty_table_printer import (
    ColumnSpec,
    RowCollection,
    pretty_date,
    pretty_money,
    guess_row_collection,
    clean_headers,
    should_be_formatted_with_commas,
)


class TestColumnSpec:
    def test_it_has_name_and_width(self):
        column = ColumnSpec('id', width=4)
        assert 'id' == column.name
        assert 4 == column.width

    def test_it_has_an_optional_func(self):
        column = ColumnSpec('id', width=4)
        assert 'hello' == column.func('hello')
        assert '' == column.func('')
        assert 7 == column.func(7)

        func = lambda x: x.upper()
        column = ColumnSpec('id', width=4, func=func)
        assert 'HELLO' == column.func('hello')


class TestRowCollection:
    @property
    def id_column(self):
        return ColumnSpec('id', width=4)

    @property
    def name_column(self):
        return ColumnSpec('name', width=8)

    @property
    def it(self):
        headers = ('id', 'name')
        column_specs = (self.id_column, self.name_column)
        return RowCollection('units', column_specs=column_specs, headers=headers)

    def test_it_takes_a_column_specs_list_and_headers_list(self):
        headers = ('id', 'name')
        column_specs = (self.id_column, self.name_column)
        rows = RowCollection('units', column_specs=column_specs, headers=headers)
        assert column_specs == rows.column_specs
        assert headers == rows.headers

    def test_it_creates_a_row_class_from_headers(self):
        rows = self.it
        assert 'hello' == rows.Row(id=1, name='hello').name
        assert 1 == rows.Row(id=1, name='hello').id

    def test_you_can_append_rows_to_it(self):
        rows = self.it
        rows.append({'name': 'Sam', 'id': 1})
        assert 1 == rows[0].id
        assert 'Sam' == rows[0].name

    def test_it_has_a_length(self):
        rows = self.it
        assert len(rows) == 0
        rows.append({'name': 'Sam', 'id': 1})
        assert len(rows) == 1

    def test_it_knows_how_to_format_the_header_row(self):
        rows = self.it
        assert '| id   | name     |' == rows.header_row

    def test_it_knows_how_to_format_break_lines(self):
        rows = self.it
        assert '| ---- | -------- |' == rows.break_line

    def test_it_knows_how_to_print_itself(self):
        rows = self.it
        rows.append({'name': 'Sam', 'id': 1})
        rows.append({'name': 'Layla', 'id': 2})
        rows.append({'name': 'Jack Gabriel', 'id': 3})
        expected = """\
| id   | name     |
| ---- | -------- |
| 1    | Sam      |
| 2    | Layla    |
| 3    | Jack Ga… |
| ---- | -------- |"""
        assert expected == str(rows)


class TestPrettyDate:
    def test_it_returns_readable_string_for_datetime_object(self):
        some_sunday = datetime(2019, 3, 10, 15, 27, 34, 18)
        assert '2019-03-10 15:27:34' == pretty_date(some_sunday)

    def test_it_returns_null_char_if_none(self):
        assert '         ∅         ' == pretty_date(None)


class TestPrettyMoney:
    def test_it_returns_a_nicely_formatted_string_for_a_float(self):
        amount = 21.50
        assert '$21.50' == pretty_money(amount)

    def test_it_returns_a_nicely_formatted_string_for_an_int(self):
        amount = 21
        assert '$21.00' == pretty_money(amount)

    def test_it_returns_a_nicely_formatted_string_for_a_decimal(self):
        amount = Decimal('21.50')
        assert '$21.50' == pretty_money(amount)

    def test_it_returns_a_nicely_formatted_string_with_commas_for_big_numbers(self):
        amount = Decimal('1980.50')
        assert '$1,980.50' == pretty_money(amount)


class TestCleanHeaders:
    def test_it_handles_count_with_star(self):
        headers = ['count(*)']
        assert ['count'] == list(clean_headers(headers))

    def test_it_handles_count_distinct(self):
        headers = ['count(distinct wombats)']
        assert ['count_distinct_wombats'] == list(clean_headers(headers))

    def test_it_handles_sum(self):
        headers = ['sum(wombats)']
        assert ['sum_wombats'] == list(clean_headers(headers))


class TestShouldBeFormattedWithCommas:
    def test_it_formats_count_columns_with_commas(self):
        assert should_be_formatted_with_commas('count(*)') is True
        assert should_be_formatted_with_commas('count_this_thing') is True
        assert should_be_formatted_with_commas('this_thing_count') is True

    def test_it_formats_sum_columns_with_commas(self):
        assert should_be_formatted_with_commas('sum(*)') is True
        assert should_be_formatted_with_commas('sum_this_thing') is True
        assert should_be_formatted_with_commas('this_thing_sum') is True

    def test_it_formats_total_columns_with_commas(self):
        assert should_be_formatted_with_commas('total') is True
        assert should_be_formatted_with_commas('total_this_thing') is True
        assert should_be_formatted_with_commas('total_groups') is True
        assert should_be_formatted_with_commas('this_thing_total') is True

    def test_it_formats_columns_that_end_with_s_with_commas(self):
        assert should_be_formatted_with_commas('groups') is True

    def test_it_formats_knows_when_not_to_format_with_commas(self):
        assert should_be_formatted_with_commas('zcountz(*)') is False


class TestGuessRowCollection:
    def test_it_handles_count(self):
        rows = [{'id': 1, 'count(distinct barcode)': 27596962761}]
        row_collection = guess_row_collection(rows)
        row_collection.append(rows[0])
        expected = """\
| id | count_distinct_barcode |
| -- | ---------------------- |
| 1  | 27,596,962,761         |
| -- | ---------------------- |\
"""
        assert expected == str(row_collection)

    def test_it_handles_plural_integers(self):
        rows = [{'id': 1, 'groups': 27596962761}]
        row_collection = guess_row_collection(rows)
        row_collection.append(rows[0])
        expected = """\
| id | groups         |
| -- | -------------- |
| 1  | 27,596,962,761 |
| -- | -------------- |\
"""
        actual = str(row_collection)
        assert expected == actual

    def test_it_handles_column_names_with_question_marks(self):
        rows = [{'one?': 1}]
        row_collection = guess_row_collection(rows)
        row_collection.append(rows[0])
        expected = """\
| one |
| --- |
| 1   |
| --- |\
"""
        assert expected == str(row_collection)
