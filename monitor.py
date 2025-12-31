#Project Structure

#   uptime-monitor/
#   ├── monitor.py # Main monitoring script
#   ├── config.json # Configuration file (URLs, thresholds, webhook)
#   ├── requirements.txt # Python dependencies
#   ├── logs/
#   │ ├── uptime.log # All check results
#   │ └── alerts.log # Failure and alert-related events
#   └── README.md

''' 
Questions I have while building
   - Brought up by my friend: how do I get around constant pinging ip ban?
'''

# monitor.py
import json # to parse json files
import time
import requests

def load_config():
# Function to load config so I can reuse it without being a global var
    with open("config.json") as file:
        config = json.load(file) # parses JSON from file
                                 # could also do:
                                 #  text = file.read()
                                 #  config = json.loads(text) # which parses JSON from a string
    return config # is a dict

def check_url(url, timeout_seconds, retries):
    result = {
        "up": False,
        "final_status": None, # int or None
        "redirected": False,
        "redirect_count": 0,
        "final_url": None, # String
        "redirect_chain": [], # list of intermediate URLs or statuses
        "latency_ms_total": None, # float
        "latency_ms_last_attempt": None, #float
        "error": None # String or None
    }
    start_total = time.perf_counter()

    for attempt in range(retries + 1):
        start_attempt = time.perf_counter()

        try:
            headers = {"User-Agent": "uptime-monitor/1.0 (ProjectV)"} # User-Agent to avoid false downs
            response = requests.get(
                url,
                headers=headers,
                timeout=timeout_seconds, # example=example_test is parameter binding i.e. keyword binding 
                allow_redirects=True
            )
            end_attempt = time.perf_counter()

            result["latency_ms_last_attempt"] = (end_attempt - start_attempt) * 1000

            result["final_status"] = response.status_code
            result["final_url"] = response.url

            result["redirect_count"] = len(response.history)
            result["redirected"] = result["redirect_count"] > 0

            # Stores list of urls redirected to up until success
            result["redirect_chain"] = [r.url for r in response.history] # list of r.url for each r in response.history

            # Website is Up logic: treating 200-399 as up
            result["up"] = 200 <= response.status_code <= 399

            # Success indicates no error
            result["error"] = None

            break

        except requests.RequestException as e: # handles RequestException and gives me the exception object saved in var "e" to inspect
            end_attempt = time.perf_counter()
            result["latency_ms_last_attempt"] = (end_attempt - start_attempt) * 1000

            # Specific exception message
            result["error"] = f"{type(e).__name__}: {e}" # type(e),__name__ // what class was this object created from? and whats it's name?
                                                         #f"{e}" calls str(e) giving me the error's message" i.e., why did it fail?

            # Try again if not last attempt, otherwise loop ends and "Up" stays false
            continue

    end_total = time.perf_counter()
    result["latency_ms_total"] = (end_total - start_total) * 1000 #convert to milliseconds

    return result
    
def main():
    website_down = False
    config = load_config()
 
    for url in config["urls"]:
        result = check_url(url, config["timeout_seconds"], config["retries"])
        print("Checked url:" + url)
        if result["up"]:
            print("Website is up and running")
            print(f"Total Latency in milliseconds: {result["latency_ms_total"]}")
            print(f"Final Status Code: {result["final_status"]}")
            if result["redirected"]:
                print(f"Website was redirected {result['redirect_count']} times:")
                for each in result["redirect_chain"]:
                    print("\t" + each + "\n")
                print("Final landing page: " + result["final_url"])
        else:
            print("Website is down")
            print(f"final status: {result['final_status']}")
            print(result["error"])
            website_down = True
        print("\n")

    if website_down:
        return 1
        
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
    