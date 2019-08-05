"""
GitHub companion module for SnippetsBackup
Author: LEE WEI HAO JONATHAN (buildevol)
"""

import json
import requests
from urllib.parse import urlparse

GITHUB_GIST_BASE_URL = "https://api.github.com/gists/"

CHUNK_SIZE = 1024 * 1024    # 1 MB


def backup_single_github_gist():
    """
    Back up a single GitHub Gist from a GitHub Gist URL which the user will be prompted to input.
    :return: None
    """
    github_gist_url = input("Enter a GitHub Gist URL: ")

    parsed_url = parse_single_gist_url(github_gist_url)
    github_username, github_gist_id = parsed_url

    api_github_url_format = GITHUB_GIST_BASE_URL + github_gist_id
    response = requests.get(api_github_url_format)
    decoded_json_response = json.loads(response.content)
    raw_files_url_dict = get_raw_files_url_dict(decoded_json_response)

    for file_url in raw_files_url_dict:
        file_response = requests.get(file_url)
        file_response.raise_for_status()
        file_name = raw_files_url_dict[file_url]
        with open(file_name, 'wb') as gist_file:
            for buffer in file_response.iter_content(CHUNK_SIZE):
                gist_file.write(buffer)


def parse_single_gist_url(raw_gist_url):
    """
    Parses the input GitHub Gist URL (A specific GitHub Gist url).
    :param raw_gist_url: The raw GitHub Gist URL (A specific GitHub Gist url).
    :return: A list containing the GitHub username in the first index and the GitHub Gist id in the second index.
    """
    parsed_github_gist_url = urlparse(raw_gist_url).path.strip()
    parsed_github_gist_url_list = parsed_github_gist_url.split('/')

    # Since the first element in the parsed_github_gist_url_list is an empty string, removes that element
    del parsed_github_gist_url_list[0]

    return parsed_github_gist_url_list


def get_raw_files_url_dict(decoded_json):
    """
    Parses the input deserialised json to obtain a dict of raw files urls in the GitHub Gist URL.
    :param decoded_json: A deserialised json from the json returned by GitHub API.
    :return: A dict containing kay value pairs where the raw file url is the key and the file name is the value.
    """
    result = {}
    for file in decoded_json["files"]:
        file_name = decoded_json["files"][file]["filename"]
        raw_file_url = decoded_json["files"][file]["raw_url"]
        result[raw_file_url] = file_name

    return result
