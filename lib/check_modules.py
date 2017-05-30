import subprocess
import re

def check_ping2(hostname_or_ip="127.0.0.1", ping_count="4", warn_percent_loss=0):
    statistics = {"status": "DOWN", "loss": "N/A", "minimum": "N/A", "maximum": "N/A", "average": "N/A" }
    stats = ["minimum", "maximum", "average"]

    ping_count = str(ping_count)
    
    result = subprocess.Popen(["ping", hostname_or_ip, "-c", ping_count],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)

    stdout_result = str(result.stdout.read())
    stream_data = result.communicate()[0]

    if result.returncode == 0:
        statistics["loss"] = float(re.search("(\d*)% packet loss", stdout_result).group(1))

        if statistics["loss"] > warn_percent_loss:
            statistics["status"] = "WARN"
        else:
            statistics["status"] = "OK"

        rtt_match = re.search(r'(\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)', stdout_result)
        for (index, rtt_stat) in enumerate(stats):
            statistics[rtt_stat] = float(rtt_match.group(index + 1))

    return statistics

def check_historical(previous_downs, current_downs):
    print("Previous Downs", previous_downs)
    print("Current Downs:", current_downs)

    history = {"recent_fail" : [i for i in current_downs["DOWN"] if i not in previous_downs["DOWN"]]}
    print("Recently Failed:", history["recent_fail"])

    history["recent_warn"] = [i for i in current_downs["WARN"] if i not in previous_downs["WARN"]]
    print("Recently Warn:", history["recent_warn"])

    # Looks through all WARN and DOWN Instances
    history["recovered"] = [h for i in previous_downs for h in previous_downs[i] if h not in current_downs[i]]
    print("Recently Recovered:", history["recovered"])
    
    return history
