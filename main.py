#!/usr/bin/python

"""Check ping to connected SingAREN networks"""

import os
import time

from lib import JSON_FileManagement
from lib import check_modules
from lib import mail
from conf import main_conf


def main():
    failed_tests = {"WARN": [], "DOWN": []}

    if not os.path.isfile(main_conf.file_path_failed_tests):
        # Creates failed test file at main_conf.file_path_failed_tests if it does not exist
        JSON_FileManagement.save_file_as_json(main_conf.file_path_failed_tests, {"WARN": [], "DOWN": []})

    previous_failures = JSON_FileManagement.json_file_to_object(main_conf.file_path_failed_tests) # Previous failed tests

    network_peers = JSON_FileManagement.json_file_to_object(main_conf.file_path_network_peers)
    network_peers["timestamp"] = str(time.time()).split(".")[0]    #adds an epoch timestamp to the status dictionary
    print(network_peers["timestamp"])

    try:
        for (index, nren) in enumerate(network_peers["nren"]):
            # Picks the ip information for each country and performs a ping test to said ip

            results = check_modules.check_ping2(nren["properties"]["hostname/ip"], main_conf.ping_count)
            # Outputs ping test results for each test found within the SingAREN Peers GeoJSON file
            print(nren["properties"]['name'] + ": " + results["status"])
            del network_peers["nren"][index]["properties"]["hostname/ip"] # removes hostname/ip address for privacy reasons

            # Saves result statistics into Singpeers GeoJSON data
            network_peers["nren"][index]["results"] = results

            if results["status"] != "OK":
                # Saves all failed tests within it's own list
                #failed_tests.append(nren["properties"]['name'])
                failed_tests[results["status"]].append(nren["properties"]['name'])

    except TypeError:
        print("Error in JSON file format")
        exit()

    historical_status = check_modules.check_historical(previous_failures, failed_tests)

    # Checks if any tests are updated from previous results
    if historical_status["recovered"] or \
            historical_status["recent_fail"] or \
            historical_status["recent_warn"]:
	print("Sending status notification", JSON_FileManagement.dump_json_to_string(historical_status))

        mail.sendMail([main_conf.mail_to_address],
                      main_conf.mail_from_address, 
                      main_conf.mail_subject,
                      JSON_FileManagement.dump_json_to_string(historical_status))

    JSON_FileManagement.save_file_as_json(main_conf.file_path_failed_tests, failed_tests)
    JSON_FileManagement.save_file_as_json(main_conf.file_path_status, network_peers)


if __name__ == '__main__':
    main()

