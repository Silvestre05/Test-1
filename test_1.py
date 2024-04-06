import requests
from collections import defaultdict
import re

def fetch_log_file(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch log file. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while fetching the log file: {str(e)}")
        return None

def analyze_log(log_content):
    if not log_content:
        return
    
    url_count = 0
    non_200_count = 0
    total_non_200_count = 0
    put_requests = defaultdict(int)

    for line in log_content.split('\n'):
        if "/production/file_metadata/modules/ssh/sshd_config" in line:
            url_count += 1
            if " 200 " not in line:
                non_200_count += 1
        
        if "/dev/report/" in line and "PUT" in line:
            ip_address = re.search(r'\d+\.\d+\.\d+\.\d+', line).group()
            put_requests[ip_address] += 1

        if " 200 " not in line:
            total_non_200_count += 1
    
    print(f"Number of times the URL '/production/file_metadata/modules/ssh/sshd_config' was fetched: {url_count}")
    print(f"Number of times the return code from Apache was not 200 for the above URL: {non_200_count}")
    print(f"Total number of times Apache returned any code other than 200: {total_non_200_count}")
    print("Total number of times that any IP address sent a PUT request to a path under '/dev/report/':")
    for ip, count in put_requests.items():
        print(f" - IP: {ip}, Count: {count}")

if __name__ == "__main__":
    log_url = "https://pastebin.com/raw/gstGCJv4"
    log_content = fetch_log_file(log_url)
    if log_content:
        analyze_log(log_content)