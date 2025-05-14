import requests
import re
from urllib.parse import urljoin

def print_banner():
    """Display a colored tool banner with ASCII art."""
    banner = """
\033[1;32m=====================================================
   ROBOTS.TXT SCRAPER TOOL
   Author: KwesiLarry
   Contact: kwesixwizard@proton.me
   Description: Fetch and analyze robots.txt files.
=====================================================
\033[0m
    """  # \033[1;32m makes the text green, and \033[0m resets the color

    # Add ASCII art (optional)
    ascii_art = """
\033[1;34m
        _______         
      /         \\     
     |  [o] [o]  |    
      \\    <     |    
       \\_______ /     
        \\_____/       
\033[0m
    """  # \033[1;34m makes the ASCII art blue, and \033[0m resets the color

    print(banner)
    print(ascii_art)

def fetch_robots_txt(base_url):
    """Fetch the robots.txt file of a website."""
    robots_url = urljoin(base_url, "/robots.txt")
    try:
        response = requests.get(robots_url, timeout=5)
        if response.status_code == 200:
            print(f"[INFO] Successfully retrieved robots.txt from {base_url}")
            return response.text
        else:
            print(f"[ERROR] Failed to retrieve robots.txt. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Exception occurred: {e}")
        return None

def parse_disallowed_paths(robots_txt):
    """Extract disallowed paths from robots.txt."""
    disallowed_paths = []
    lines = robots_txt.splitlines()
    for line in lines:
        # Match lines starting with Disallow: (case insensitive)
        match = re.match(r"(?i)^Disallow:\s*(.+)$", line)
        if match:
            path = match.group(1).strip()
            if path:  # Ignore empty disallowed paths
                disallowed_paths.append(path)
    return disallowed_paths

def fetch_disallowed_content(base_url, paths, output_file):
    """Fetch content for disallowed paths and save results to a file."""
    with open(output_file, "w") as file:
        for path in paths:
            full_url = urljoin(base_url, path)
            try:
                response = requests.get(full_url, timeout=5)
                print(f"[INFO] Fetching {full_url} - Status: {response.status_code}")
                file.write(f"URL: {full_url}\nStatus Code: {response.status_code}\n")
                if response.status_code == 200:
                    content_preview = response.text[:200].replace("\n", " ")  # Truncate content for saving
                    file.write(f"Content Preview: {content_preview}\n\n")
                else:
                    file.write("Content not accessible or restricted.\n\n")
            except requests.exceptions.RequestException as e:
                print(f"[ERROR] Failed to fetch {full_url}. Exception: {e}")
                file.write(f"Error fetching {full_url}: {e}\n\n")
    print(f"[INFO] Results saved to {output_file}")

if __name__ == "__main__":
    print_banner()
    
    # Prompt the user to enter the target website
    target_website = input("Enter the target website (e.g., https://example.com): ").strip()
    if not target_website.startswith("http://") and not target_website.startswith("https://"):
        print("[ERROR] Please provide a valid URL starting with http:// or https://")
    else:
        robots_txt = fetch_robots_txt(target_website)
        if robots_txt:
            disallowed_paths = parse_disallowed_paths(robots_txt)
            if disallowed_paths:
                print(f"[INFO] Disallowed paths found: {disallowed_paths}")
                # Prompt the user to enter the output file name
                output_file = input("Enter the output file name (e.g., results.txt): ").strip()
                fetch_disallowed_content(target_website, disallowed_paths, output_file)
            else:
                print("[INFO] No disallowed paths found in robots.txt.")
