from __future__ import annotations

import collections
from enum import Enum
from typing import List


class NodeStates(Enum):
    CLEAN_UNKNOWN = "clean_unknown"
    CLEAN_LINUX = "clean_linux"
    CLEAN_WINDOWS = "clean_windows"
    PROPAGATED_LINUX = "propagated_linux"
    PROPAGATED_WINDOWS = "propagated_windows"
    ISLAND = "island"
    ISLAND_MONKEY_LINUX = "island_monkey_linux"
    ISLAND_MONKEY_LINUX_RUNNING = "island_monkey_linux_running"
    ISLAND_MONKEY_WINDOWS = "island_monkey_windows"
    ISLAND_MONKEY_WINDOWS_RUNNING = "island_monkey_windows_running"
    MANUAL_LINUX = "manual_linux"
    MANUAL_LINUX_RUNNING = "manual_linux_running"
    MANUAL_WINDOWS = "manual_windows"
    MANUAL_WINDOWS_RUNNING = "manual_windows_running"
    MONKEY_LINUX = "monkey_linux"
    MONKEY_LINUX_RUNNING = "monkey_linux_running"
    MONKEY_WINDOWS = "monkey_windows"
    MONKEY_WINDOWS_RUNNING = "monkey_windows_running"

    @staticmethod
    def get_by_keywords(keywords: List) -> NodeStates:
        potential_groups = [
            i for i in NodeStates if NodeStates._is_state_from_keywords(i, keywords)
        ]
        if len(potential_groups) > 1:
            raise MultipleGroupsFoundException(
                "Multiple groups contain provided keywords. "
                "Manually build group string to ensure keyword order."
            )
        elif len(potential_groups) == 0:
            raise NoGroupsFoundException(
                "No groups found with provided keywords. "
                "Check for typos and make sure group codes want to find exists."
            )
        return potential_groups[0]

    @staticmethod
    def _is_state_from_keywords(group, keywords) -> bool:
        group_keywords = group.value.split("_")
        return collections.Counter(group_keywords) == collections.Counter(
            [word.lower() for word in keywords]
        )


class MultipleGroupsFoundException(Exception):
    pass


class NoGroupsFoundException(Exception):
    pass
