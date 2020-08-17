"""
A simple script to run multiple locust tests and write results.

Results are written using standard CSV files and also an HTML
page is created that contains graphs to compare results.
"""

import argparse
import json
import subprocess
import shlex
import os
import csv


def parse_args():
    """Parse arguments for the script."""
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', "--file", action="store", default="tests.json",
                        help="JSON file for tests to run")
    parser.add_argument("-o", "--output", action="store",
                        default="results", help="Store output in this folder")
    parser.add_argument("-n", "--name", action="store",
                        default="default", help="Name of test run")
    args = parser.parse_args()

    return args


def read_tests(file):
    """Read tests from the file."""
    try:
        data = json.load(open(file))
        return data["tests"]
    except FileNotFoundError:
        raise FileNotFoundError(f"Cannot find file with name {file}")
    except json.decoder.JSONDecodeError:
        raise Exception("Cannot parse tests file")
    except KeyError:
        raise Exception("You need to have a 'tests' key in your tests file")


def run_single_test(test, output):
    """
    Run a single locust test.

    This function takes a single test dictionary and runs it using locust
    command

    Args:
        test (dict): A dictionary that holds test information such as 'users'
        count, 'rps' the number of users added per second and 'time' the
        time the test will run for it.
    """
    duration = test.get("time", "1m")
    users = test.get("users", 10)
    rps = test.get("rps", 5)
    output = os.path.join(output, f"{users}-{rps}-{duration}")
    locust_command = shlex.split(
        f"locust --headless -u {users} -r {rps} -t{duration} --only-summary \
        --csv={output}")
    subprocess.run(locust_command)
    return output


def run_tests(tests, output, name):
    """
    Run all tests.

    Here we pass a list of tests and loop over them to run them all.

    Args:
        tests (list): A list of test dictionaries to run.
        output (str): The name of output folder.
    """
    os.makedirs(os.path.join(output, name), exist_ok=True)
    csv_files = []
    for test in tests:
        csv_files.append(run_single_test(test, os.path.join(output, name)))
    return csv_files


def write_results(results, name):
    """Write results to a CSV file."""
    file = f"results/{name}/data.csv"
    writer = csv.writer(open(file, "w"))
    writer.writerow(["rps", "avg", "failures"])
    rps = []
    avg = []
    failures = []
    for result in results:
        result = f"{result}_stats.csv"
        with open(result) as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] == "Aggregated":
                    rps.append(float(row[9]))
                    avg.append(float(row[5]))
                    failures.append(int(row[3]))
                    break
    rps, avg, failures = zip(*sorted(zip(rps, avg, failures)))
    rps = list(rps)
    avg = list(avg)
    failures = list(failures)
    for e in range(len(rps)):
        writer.writerow([rps[e], avg[e], failures[e]])


def main():
    """Run main script function."""
    args = parse_args()
    tests = read_tests(args.file)
    results = run_tests(tests, args.output, args.name)
    write_results(results, args.name)


if __name__ == '__main__':
    main()
