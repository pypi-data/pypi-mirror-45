# -*- coding: utf-8 -*-
import math
from random import Random

import pytest
from _pytest.config import create_terminal_writer


def get_group_size(total_items, total_groups):
    """Return the group size."""
    return int(math.ceil(float(total_items) / total_groups))


def get_group(items, group_size, group_id):
    """Get the items from the passed in group based on group size."""
    start = group_size * (group_id - 1)
    end = start + group_size

    if start >= len(items) or start < 0:
        raise ValueError("Invalid test-group argument")

    return items[start:end]


def pytest_addoption(parser):
    group = parser.getgroup('split your tests into evenly sized groups and run them')
    group.addoption('--test-group-count', dest='test-group-count', type=int,
                    help='The number of groups to split the tests into')
    group.addoption('--test-group', dest='test-group', type=int,
                    help='The group of tests that should be executed')
    group.addoption('--test-group-random-seed', dest='random-seed', type=int,
                    help='Integer to seed pseudo-random test selection')


@pytest.hookimpl(hookwrapper=True)
def pytest_collection_modifyitems(session, config, items):
    yield
    group_count = config.getoption('test-group-count')
    group_id = config.getoption('test-group')
    seed = config.getoption('random-seed', False)

    if not group_count or not group_id:
        return

    original_order = {item: index for index, item in enumerate(items)}

    if seed is not False:
        seeded = Random(seed)
        seeded.shuffle(items)

    total_items = len(items)

    group_size = get_group_size(total_items, group_count)
    tests_in_group = get_group(items, group_size, group_id)
    items[:] = tests_in_group

    if seed is not False:
        # Revert the shuffled sample of tests back to their original order.
        items.sort(key=original_order.__getitem__)

    terminal_reporter = config.pluginmanager.get_plugin('terminalreporter')
    if terminal_reporter is not None:
        terminal_writer = create_terminal_writer(config)
        message = terminal_writer.markup(
            'Running test group #{0} ({1} tests)\n'.format(
                group_id,
                len(items)
            ),
            yellow=True
        )
        terminal_reporter.write(message)
