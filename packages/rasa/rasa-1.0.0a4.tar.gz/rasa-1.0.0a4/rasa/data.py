import json
import logging
import os
import shutil
import tempfile
import uuid
from typing import Tuple, List, Text, Set, Union
import re

logger = logging.getLogger(__name__)


def get_core_directory(paths: Union[Text, List[Text]]) -> Text:
    """Recursively collects all Core training files from a list of paths.

    Args:
        paths: List of paths to training files or folders containing them.

    Returns:
        Path to temporary directory containing all found Core training files.
    """
    core_files, _ = _get_core_nlu_files(paths)
    return _copy_files_to_new_dir(core_files)


def get_nlu_directory(paths: Union[Text, List[Text]]) -> Text:
    """Recursively collects all NLU training files from a list of paths.

    Args:
        paths: List of paths to training files or folders containing them.

    Returns:
        Path to temporary directory containing all found NLU training files.
    """
    _, nlu_files = _get_core_nlu_files(paths)
    return _copy_files_to_new_dir(nlu_files)


def get_core_nlu_directories(paths: Union[Text, List[Text]]) -> Tuple[Text, Text]:
    """Recursively collects all training files from a list of paths.

    Args:
        paths: List of paths to training files or folders containing them.

    Returns:
        Path to directory containing the Core files and path to directory
        containing the NLU training files.
    """
    story_files, nlu_data_files = _get_core_nlu_files(paths)

    story_directory = _copy_files_to_new_dir(story_files)
    nlu_directory = _copy_files_to_new_dir(nlu_data_files)

    return story_directory, nlu_directory


def _get_core_nlu_files(paths: Union[Text, List[Text]]) -> Tuple[Set[Text], Set[Text]]:
    story_files = set()
    nlu_data_files = set()

    if isinstance(paths, str):
        paths = [paths]

    for path in set(paths):
        if not path:
            continue

        if _is_valid_filetype(path):
            if _is_nlu_file(path):
                nlu_data_files.add(os.path.abspath(path))
            else:
                story_files.add(os.path.abspath(path))
        else:
            new_story_files, new_nlu_data_files = _find_core_nlu_files_in_directory(
                path
            )

            story_files.update(new_story_files)
            nlu_data_files.update(new_nlu_data_files)

    return story_files, nlu_data_files


def _find_core_nlu_files_in_directory(directory: Text) -> Tuple[Set[Text], Set[Text]]:
    story_files = set()
    nlu_data_files = set()
    for root, _, files in os.walk(directory):
        for f in files:
            full_path = os.path.join(root, f)

            if not _is_valid_filetype(full_path):
                continue

            if _is_nlu_file(full_path):
                nlu_data_files.add(full_path)
            else:
                story_files.add(full_path)

    return story_files, nlu_data_files


def _is_valid_filetype(path: Text) -> bool:
    is_file = os.path.isfile(path)
    is_datafile = path.endswith(".json") or path.endswith(".md")

    return is_file and is_datafile


def _is_nlu_file(file_path: Text) -> bool:
    with open(file_path, encoding="utf-8") as f:
        if file_path.endswith(".json"):
            content = f.read()
            is_nlu_file = json.loads(content).get("rasa_nlu_data") is not None
        else:
            is_nlu_file = any(_contains_nlu_pattern(l) for l in f)
    return is_nlu_file


def _contains_nlu_pattern(text: Text) -> bool:
    nlu_pattern = r"\s*##\s*(intent|regex||synonym|lookup):"

    return re.match(nlu_pattern, text) is not None


def _copy_files_to_new_dir(files: Set[Text]) -> Text:
    directory = tempfile.mkdtemp()
    for f in files:
        # makes sure files do not overwrite each other, hence the prefix
        unique_prefix = uuid.uuid4().hex
        unique_file_name = unique_prefix + "_" + os.path.basename(f)
        shutil.copy2(f, os.path.join(directory, unique_file_name))

    return directory
