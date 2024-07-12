# !/usr/bin/env python
# coding: utf-8
# vi: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import argparse
import json
import base64
import requests
import time
import logging

api_endpoint = "https://demolabs.42crunch.cloud"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def configure_logging(verbose):
    formatter = logging.Formatter('%(levelname)s %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    info_formatter = logging.Formatter('%(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # Check if a StreamHandler is already present
    handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]

    if not handlers:
        console_handler = logging.StreamHandler()
        if verbose:
            console_handler.setFormatter(formatter)
        else:
            console_handler.setFormatter(info_formatter)
        logger.addHandler(console_handler)

    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger("urllib3").setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)
        logging.getLogger("urllib3").setLevel(logging.INFO)

    # Set a custom formatter for INFO level
    logging.getLogger().handlers[0].addFilter(lambda record: record.levelno != logging.INFO or verbose)


def retrieve_scan_token(credentials, api_uuid, verbose):
    configure_logging(verbose)
    if verbose: logger.info("retrieve_scan_token")
    headers = {
        "accept": "application/json",
        "X-API-KEY": credentials
    }

    max_attempts = 40
    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(
                f"{api_endpoint}/api/v1/apis/{api_uuid}/scanConfigurations",
                headers=headers,
            )
            if response.status_code == 404:
                logger.warning(f"Received a 404 response. Attempt {attempt}/{max_attempts}")
                time.sleep(1)
                continue # Return a None for a 404 response, which basically means no config exists
            response.raise_for_status()
            token_id = response.json()["tokenId"]
            return token_id
        except requests.RequestException as e:
            logger.error(f"Attempt {attempt}/{max_attempts} failed. Error: {e}")
            if attempt < max_attempts:
                time.sleep(1)
            else:
                raise

def delete_scan_conf(credentials, api_uuid, verbose, scan_token):
    configure_logging(verbose)
    if verbose: logger.info("delete_scan_config")
    headers = {
        "accept": "application/json",
        "X-API-KEY": credentials
    }
    response = requests.get(
        f"{api_endpoint}/api/v1/apis/{api_uuid}/scanConfigurations",
        headers=headers,
    )
    response.raise_for_status()
    response_scan_config = response.json()
    if response_scan_config["tokenId"] and response_scan_config["tokenId"] == scan_token:
        scan_config_id = response_scan_config["id"]
    response = requests.delete(
        f"{api_endpoint}/api/v1/scanConfigurations/{scan_config_id}",
        headers=headers,
    )
    response.raise_for_status()
    # Make sure scan config is deleted
    max_attempts = 20
    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(
                f"{api_endpoint}/api/v1/apis/{api_uuid}/scanConfigurations",
                headers=headers,
            )
            if response.status_code == 404:
                return
        except requests.RequestException as e:
            logger.error(f"Delete Scan Conf: Attempt {attempt}/{max_attempts} failed. Error: {e}")
            if attempt < max_attempts:
                time.sleep(1)
            else:
                raise
    return


def create_scan_conf(credentials, api_uuid, app_endpoint, verbose):
    configure_logging(verbose)
    if verbose: logger.info("create_scan_conf - retrieve spec")
    headers_spec = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-KEY": credentials
    }

    response_spec = requests.post(
        f"{api_endpoint}/api/v1/apis/{api_uuid}/specs",
        headers=headers_spec,
        json={"filter": 256},
    )

    response_spec.raise_for_status()

    if verbose: logger.info("create_scan_conf - send config")
    scan_config = {
        "host": app_endpoint,
        "followRedirect": False,
        "flowrate": 100,
        "maxScanTime": 3600,
        "settings": {
            "memoryLimit": 2147483648,
            "memoryTimeSpan": 30,
            "maxIssue": 1000,
            "logger": "error",
            "securityDisabled": True,
        },
    }

    headers_scanconf = {
        "accept": "application/json",
        "X-API-KEY": credentials
    }

    response_scanconf = requests.post(
        f"{api_endpoint}/api/v1/apis/{api_uuid}/branches/main/scanConfigurations",
        headers=headers_scanconf,
        json={"scanConfiguration": base64.b64encode(json.dumps(scan_config).encode()).decode()},
    )
    response_scanconf.raise_for_status()

    return retrieve_scan_token(credentials, api_uuid, verbose)

def get_conformance_report(credentials, api_uuid, verbose):
    configure_logging(verbose)
    headers = {
        "accept": "application/json",
        "X-API-KEY": credentials
    }

    response_report = requests.get(
        f"{api_endpoint}/api/v1/apis/{api_uuid}/scanreport?medium=2",
        headers=headers,
    )

    response_report.raise_for_status()

    report = response_report.json()
    task_id = report["tid"]
    summary = json.loads(base64.b64decode(report["data"]).decode())["summary"]

    response_compliance = requests.get(
        f"{api_endpoint}/api/v2/sqgs/reportComplianceStatus?taskId={task_id}&reportType=scan",
        headers=headers,
    )

    response_compliance.raise_for_status()

    report_compliance = response_compliance.json()
    acceptance = report_compliance["acceptance"]
    summary["acceptance"] = acceptance

    api_tag_id = report_compliance["apiTags"][0]
    if api_tag_id is not None:
        response_thresholds = requests.get(
            f"{api_endpoint}/api/v2/sqgs/scan",
            headers=headers,
        )

        response_thresholds.raise_for_status()

        conf_scan_thresholds = response_thresholds.json()["list"]
        summary["conf_scan_thresholds"] = conf_scan_thresholds

    return summary

def main():
    global result
    global data

    parser = argparse.ArgumentParser(description="42Crunch toolkit.")
    parser.add_argument("--credentials", required=True, help="API key")
    parser.add_argument("--api_uuid", required=True, help="API UUID")
    parser.add_argument("--action", required=True, help="Action to perform: create_scan_conf or get_conformance_report")
    parser.add_argument("--app_endpoint", help="Application endpoint")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    args = parser.parse_args()

    configure_logging(args.verbose)

    if not any(vars(args).values()):
        logger.info("No options specified. Printing usage information:")
        parser.print_help()
        exit(0)

    if args.action == "create_scan_conf" and not args.app_endpoint:
        parser.error("--app_endpoint is required for action create_scan_conf")

    if args.action == "create_scan_conf":
        logger.debug("Checking to see if there is an existing scan config")
        scan_token = retrieve_scan_token(args.credentials, args.api_uuid, args.verbose)
        logger.debug(f"Found scan token: {scan_token}")
        if scan_token is not None:
            delete_scan_conf(args.credentials, args.api_uuid, args.verbose, scan_token)
        result = create_scan_conf(
            args.credentials, args.api_uuid, args.app_endpoint, args.verbose
        )

        logger.info("action: " +result)
        data ={'scan_id': result}
        with open('securityScan.json', 'w') as f:
            logger.info(data)
            json.dump(data, f)
    elif args.action == "get_conformance_report":
        result = get_conformance_report(args.credentials, args.api_uuid, args.verbose)
    else:
        parser.error("Unknown action")

    logger.info(result)

if __name__ == "__main__":
    main()
