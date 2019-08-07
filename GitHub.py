"""
GitHub companion module for SnippetsBackup
Author: LEE WEI HAO JONATHAN (buildevol)
"""

import requests
from urllib.parse import urlparse

GITHUB_API_BASE_URL = "https://api.github.com"
GITHUB_API_DEFAULT_NUM_OF_PAGE_ITEMS = 30

CHUNK_SIZE = 1024 * 1024    # 1 MB


def backup_single_github_gist():
    """
    Back up a single GitHub Gist from a GitHub Gist URL which the user will be prompted to input.
    :return: None
    """
    github_gist_url = input("Enter a GitHub Gist URL: ")

    parsed_url = parse_single_gist_url(github_gist_url)
    github_username, github_gist_id = parsed_url

    api_github_url_format = GITHUB_API_BASE_URL + "/gists/" + github_gist_id
    response = requests.get(api_github_url_format)
    response.raise_for_status()
    decoded_json_response = response.json()
    raw_files_url_dict = get_raw_files_url_from_single_gist_dict(decoded_json_response)

    for file_url in raw_files_url_dict:
        file_response = requests.get(file_url)
        file_response.raise_for_status()
        file_name = raw_files_url_dict[file_url]
        with open(file_name, 'wb') as gist_file:
            for buffer in file_response.iter_content(CHUNK_SIZE):
                gist_file.write(buffer)
            print(f"{file_name} backup completed.")

    print("Backup a single GitHub Gist completed.")

def backup_github_gist_from_username():
    """
    Back up all GitHub Gist from a GitHub username which the user will be prompted to input.
    :return: None
    """
    github_username = input("Enter a GitHub username: ")

    api_github_url_format = GITHUB_API_BASE_URL + "/users/" + github_username + "/gists"
    response = requests.get(api_github_url_format)
    response.raise_for_status()
    decoded_json_response = response.json()


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


def get_raw_files_url_from_single_gist_dict(decoded_json):
    """
    Parses the input deserialised json to obtain a dict of raw files urls in the GitHub Gist URL.
    :param decoded_json: A deserialised json for a single GitHub Gist from the json returned by GitHub API.
    :return: A dict containing kay value pairs where the raw file url is the key and the file name is the value.
    """
    result = {}
    for file in decoded_json["files"]:
        file_name = decoded_json["files"][file]["filename"]
        raw_file_url = decoded_json["files"][file]["raw_url"]
        result[raw_file_url] = file_name

    return result


def total_num_of_items_in_all_pages(link_header_in_response, custom_page_size=GITHUB_API_DEFAULT_NUM_OF_PAGE_ITEMS):
    """
    Calculates the total number of items in all pages based on the input link header response from GitHub API
    and the input custom page size.
    :param link_header_in_response: The link header response returned by GitHub API.
    :param custom_page_size: The custom page size whose default value is based on GITHUB_API_DEFAULT_NUM_OF_PAGE_ITEMS
    :return: The total number of items in all pages.
    """
    pass
