# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    bot create by Yann-arthur Tcheumani create:13/01/2019  Last modification: 13/01/2019
    last version: 1.0.0
    caution bot should not be used for malicious purposes
"""

import sys
import re
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import json
from colorama import Fore, Style, init
import urllib3 as url
import platform

url.disable_warnings(url.exceptions.InsecureRequestWarning)
module_name = "Spider: Find Usernames Across Social Networks"

__version__ = "1.0"


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


def verification(url_domain, urls):
    http = url.PoolManager()
    data = http.request('GET', urls)
    if data.status == 404:
        write_description_error(url_domain)
    elif data.status == 200:
        write_description_valid(url_domain, urls)


def spider(pseudo, site=None):
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
                verification(i, chaineTriee)
    else:
        chaineTriee = re.sub(r"{}", str(pseudo), site['url'])
        verification(site['url_domain'], chaineTriee)


def main():

    global site_data
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
    """parser.add_argument("--quiet", "-q",
                        action="store_false", dest="verbose",
                        help="Disable debugging information (Default Option)."
                        )"""

    """parser.add_argument("--csv",
                        action="store_true", dest="csv", default=False,
                        help="Create Comma-Separated Values (CSV) File."
                        )"""
    parser.add_argument("--site",
                        action="append", metavar='SITE_NAME',
                        dest="site_list", default=None,
                        help="Limit analysis to just the listed sites.  Add multiple options to specify more than one site."
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
        # Not desired to look at a sub-set of sites
        site_data = None
    else:
        # User desires to selectively run queries on a sub-set of the site list.

        # Make sure that the sites are supported & build up pruned site database.
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
        spider(pseudo, site_data)
        print("------------------------")


if __name__ == "__main__":
    main()
