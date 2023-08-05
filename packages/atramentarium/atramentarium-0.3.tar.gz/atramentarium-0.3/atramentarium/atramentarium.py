#!/usr/bin/env python3

from os.path import exists

import readline

from typing import Any, List, Optional


class CommandCompleter:
    """ CommandCompleter class for readline. """
    def __init__(self, command_list: List[str] = []):
        self.__command_list = command_list
        self.matches: List[str] = []

    def get_history_items(self):
        """ Return a list of historic values. """
        return [
            readline.get_history_item(i) for i in range(
                1,
                readline.get_current_history_length() + 1
                )
            ]

    def complete(self, text: str, state: int) -> Optional[str]:
        """
        Completer function for readline.
        :param text: str: Text that the user is writing at a certain moment,
            it is a variable required by readline.set_completer.
        :param state: int: Variable required by readline.set_completer.

        """
        response = None
        if state == 0:
            values = self.get_history_items()
            values += self.__command_list + [""]
            # h = Historic value.
            self.matches = sorted(
                h for h in values if h != "" and h.startswith(text)
                )
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response


def prompt(
    command_processing_function: Any,
    prompt_string: str = "> ",
    command_list: List[str] = [],
    history_filepath: str = "/tmp/completer.hist",
    parse_and_bind_init_line: str = "tab: complete"
        ) -> None:
    """
    It starts the prompt using command_completer.Completer.
    :param command_processing_function: Any: Function to execute
        over the recognized command.
    :param prompt_string: str:
        String to be used as prompt. (Default value = "> ")
    :param command_list: List[str]:
        List of commands to be added to the completer at first.
        (Default value = [])
    :param history_filepath: str: History file path.
        (Default value = "/tmp/completer.hist")
    :param parse_and_bind_init_line: str: Init line to trigger completion.
        (Default value = "tab: complete")

    """
    readline.set_completer(
        CommandCompleter(
            command_list
            ).complete
        )
    readline.parse_and_bind(parse_and_bind_init_line)
    if exists(history_filepath):
        readline.read_history_file(history_filepath)
    while True:
        command_processing_function(input(prompt_string))
        readline.write_history_file(history_filepath)
    return None


def parse_command_list(command_list: List[List[str]]) -> List[str]:
    """
    Parse command list.
    :param command_list: List[List[str]]: List of commands.

    """
    parsed_command_list = []
    for cmd_list in command_list:
        for command in cmd_list:
            parsed_command_list.append(command)
    return parsed_command_list
