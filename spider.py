# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import json
from colorama import Fore, Style, init
import urllib3 as url
import platform
import csv
import time

url.disable_warnings(url.exceptions.InsecureRequestWarning)
module_name = "Spider: Find Usernames Across Social Networks"

__version__ = "1.2"
__doc__ = ("\"\n"
           "            bot create by Yann-arthur Tcheumani create:13/01/2019  Last modification: 20/01/2019\n"
           "            last version: 1.2\n"
           "            caution bot should not be used for malicious purposes ")


def write_description_valid(url_domain, urls):
    print(Style.BRIGHT + Fore.WHITE + "[" +
          Fore.GREEN + "+" +
          Fore.WHITE + "]" + Fore.YELLOW + url_domain +
          Fore.GREEN + ": " + str(urls))


def write_description_error(url_domain):
    print(Style.BRIGHT + Fore.WHITE + "[" +
          Fore.RED + "-" +
          Fore.WHITE + "]" + Fore.YELLOW + url_domain +
          Fore.WHITE +
          Fore.GREEN + ": " + Fore.RED + "Not found")


def write_json(url_domain, urls, data):
    """
    :param url_domain: url of the site
    :param urls: url_domain with username
    :param data: data of request
    """
    datas = {url_domain: {'url': urls, 'status': data.status}}
    with open('Result.json', 'w') as result:
        json.dump(datas, result, sort_keys=True, indent=5)


def write_csv(url_domain, urls, data, times):
    """
    :param url_domain: url of the site
    :param urls: url_domain with username
    :param data: data of request
    :param times: time of request
    """
    with open('Result.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['url_domain'] + ['urls'] + ['status'] + ['time'])
        spamwriter.writerow([url_domain, urls, data.status, '{}ms'.format(times)])


def verification(url_domain, urls, data_json=False, data_csv=False):
    """
    :param url_domain: url of the site
    :param urls: url_domain with username
    :param data_json: create or not json file
    :param data_csv: create or not csv file
    """
    http = url.PoolManager()
    times = int(round(time.time() * 1000))
    data = http.request('GET', urls)
    times1 = int(round(time.time() * 1000))
    milli_sec = times1 - times

    if data.status == 404:
        write_description_error(url_domain)
        if data_json:
            write_json(url_domain, urls, data)
        elif data_csv:
            write_csv(url_domain, urls, data, milli_sec)
    elif data.status == 200:
        write_description_valid(url_domain, urls)
        if data_json:
            write_json(url_domain, urls, data)
        elif data_csv:
            write_csv(url_domain, urls, data, milli_sec)


def spider(pseudo, site=None, file_json=False, file_csv=False):
    """
    :param pseudo: username researching
    :param site: site specific or not
    :param file_json: create or not json file
    :param file_csv: create or not csv file
    """
    init(autoreset=True)

    print((Style.BRIGHT + Fore.RED + "[" +
           Fore.GREEN + "*" +
           Fore.RED + "]" + Fore.YELLOW + "Checking username" +
           Fore.WHITE + " {}" +
           Fore.GREEN + " on:").format(pseudo))

    if not site:
        with open('data.json') as f:
            data = json.load(f)
            for i in data:
                chaineTriee = re.sub(r'{}', str(pseudo), data[i]['url'])
                verification(i, chaineTriee, file_json, file_csv)
    else:
        chaineTriee = re.sub(r"{}", str(pseudo), site['url'])
        verification(site['url_domain'], chaineTriee, file_json, file_csv)


def main():
    version_string = f"%(prog)s {__version__}\n" + \
                     f"Python:  {platform.python_version()}"

    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            description=f"{module_name} (Version {__version__})"
                            )
    parser.add_argument("--version",
                        action="version", version=version_string,
                        help="Display version information and dependencies."
                        )
    parser.add_argument("--verbose", "-v", "-d", "--debug",
                        action="store_true", dest="verbose", default=False,
                        help="Display extra debugging information and metrics."
                        )
    parser.add_argument("--csv",
                        action="store_true", dest="csv", default=False,
                        help="Create Comma-Separated Values (CSV) File."
                        )
    parser.add_argument("--site",
                        action="append", metavar='SITE_NAME',
                        dest="site_list", default=None,
                        help="Limit analysis to just the listed sites.  Add multiple options to specify more than one site."
                        )
    parser.add_argument("--json",
                        action="store_true", dest="json", default=False,
                        help="create json of result"
                        )
    parser.add_argument("pseudo",
                        nargs='+', metavar='Pseudo',
                        action="store",
                        help="One or more usernames to check with social networks."
                        )
    args = parser.parse_args()
    print("""
                     _            
              (_)   | |          
     ___ _ __  _  __| | ___ _ __ 
    / __| '_ \| |/ _` |/ _ \ '__|            
    \__ \ |_) | | (_| |  __/ |   
    |___/ .__/|_|\__,_|\___|_|   
        | |                      
        |_|     """)
    with open("data.json", "r", encoding="utf-8") as raw:
        site_data_all = json.load(raw)

    if args.site_list is None:

        site_data = None
    else:
        site_data = {}
        site_missing = []
        for site in args.site_list:
            for url_domain in site_data_all:
                if site == url_domain:
                    site_data['url'] = site_data_all[site]['url']
                    site_data['url_domain'] = site
            if not site_data:
                site_missing.append(f"'{site}'")
        if site_missing:
            print(f"Site not found {', '.join(site_missing)}.")
            sys.exit(1)

    for pseudo in args.pseudo:
        if not args.json:
            if not args.csv:
                spider(pseudo, site_data)
            else:
                spider(pseudo, site_data, file_csv=True)
        else:
            if not args.csv:
                spider(pseudo, site_data, file_json=True)
            else:
                spider(pseudo, site_data, file_csv=True, file_json=True)
        print("------------------------")


if __name__ == "__main__":
    main()
