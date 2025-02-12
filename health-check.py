import yaml
import requests
import time
from urllib.parse import urlparse
import argparse
import math

def parse_endpoint(entry):
    # Initialize the parsed entry dictionary
    parsed_entry = {}

    # Ensure 'name' and 'url' are present (required fields)
    if 'name' not in entry or 'url' not in entry:
        raise ValueError("Each entry must contain 'name' and 'url'")

    parsed_entry['name'] = entry['name']
    parsed_entry['url'] = entry['url']

    # Handle 'method' (optional, default to 'GET' if not provided)
    parsed_entry['method'] = entry.get('method', 'GET')

    # Handle 'headers' (optional, if provided, it should be a dictionary)
    parsed_entry['headers'] = entry.get('headers', {})

    # Handle 'body' (optional, if provided, it should be a JSON string)
    parsed_entry['body'] = entry.get('body', None)

    return parsed_entry


def parse_file(file_path):
    # Read and parse the YAML file
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    # Initialize an empty list to store parsed entries
    parsed_entries = []

    # Process each entry in the data
    for entry in data:
        parsed_entry = parse_endpoint(entry)
        parsed_entries.append(parsed_entry)

    return parsed_entries


def extract_domain(url):
    """Helper function to extract the domain name from a URL."""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    domain = domain.replace('www.', '')  # Remove 'www.' if present
    return domain


def send_requests(parsed_data):
    """Function to send GET or POST requests and track status."""
    domain_status = {}  # Dictionary to track status for each domain

    while True:  # Infinite loop to keep sending requests until interrupted
        for entry in parsed_data:
            try:
                # Extract data from the entry
                url = entry['url']
                method = entry['method']
                headers = entry['headers']
                body = entry['body']

                domain = extract_domain(url)  # Extract domain from URL

                # Send the HTTP request based on the method
                if method == 'GET':
                    response = requests.get(url, headers=headers)
                elif method == 'POST':
                    # Ensure body is sent as JSON if available
                    response = requests.post(url, json=body, headers=headers)
                else:
                    print(f"Unsupported method {method} for URL {url}")
                    continue  # Skip unsupported methods

                latency = response.elapsed.total_seconds()

                # Track the status (UP or DOWN) based on the response code
                if 200 <= response.status_code < 300 and latency < .5:
                    status = 'UP'
                else:
                    status = 'DOWN'

                # Update the domain's status in the dictionary
                if domain not in domain_status:
                    domain_status[domain] = {'UP': 0, 'DOWN': 0}

                if status == 'UP':
                    domain_status[domain]['UP'] += 1
                else:
                    domain_status[domain]['DOWN'] += 1

                # Print the response status
                print(f"Sent {method} request to {url} - Status Code: {response.status_code} - Latency: {latency}")

            except requests.RequestException as e:
                print(f"Error sending {method} request to {url}: {e}")

        print("\nCurrent domain statuses (as percentages):")
        for domain, status in domain_status.items():
            total_requests = status['UP'] + status['DOWN']
            up_percentage = (status['UP'] / total_requests) * 100

            # Round up the percentage using math.ceil()
            up_percentage_rounded = math.ceil(up_percentage)

            # Print domain status with percentage
            print(f"{domain}: {status['UP']}/{total_requests} (UP: {up_percentage_rounded:.2f}%)")
        # Wait for 15 seconds before sending the next batch of requests
        print("\nWaiting for 15 seconds before sending the next batch of requests...\n")
        time.sleep(15)


if __name__ == '__main__':
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Send GET/POST requests and track domain status.")
    parser.add_argument('file', help="Path to the YAML file with request definitions.")
    args = parser.parse_args()

    parsed_data = parse_file(args.file)
    send_requests(parsed_data)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
