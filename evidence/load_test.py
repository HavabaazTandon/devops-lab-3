import time
import urllib.request
import concurrent.futures

URL = "http://localhost:5000"
TOTAL = 100

def request(i):
    start = time.time()
    try:
        with urllib.request.urlopen(URL, timeout=10) as r:
            return r.status, time.time() - start
    except Exception as e:
        return str(e), time.time() - start

start = time.time()

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
    results = list(pool.map(request, range(TOTAL)))

elapsed = time.time() - start
success = sum(1 for status, _ in results if status == 200)

print("TOTAL REQUESTS:", TOTAL)
print("SUCCESSFUL:", success)
print("FAILED:", TOTAL - success)
print("TOTAL TIME:", round(elapsed, 2), "seconds")
print("REQUESTS/SECOND:", round(TOTAL / elapsed, 2))

with open("evidence/load_test_results.txt", "w") as f:
    f.write(f"Total requests: {TOTAL}\n")
    f.write(f"Successful: {success}\n")
    f.write(f"Failed: {TOTAL-success}\n")
    f.write(f"Duration: {elapsed:.2f}s\n")
    f.write(f"Requests/sec: {TOTAL/elapsed:.2f}\n")
