import os
import glob
import yaml
import requests
import urllib3

# SSL xəbərdarlıqlarını söndürürük
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SPLUNK_URL_BASE = os.getenv("SPLUNK_URL", "").strip()
SPLUNK_TOKEN = os.getenv("SPLUNK_TOKEN", "").strip()

if not SPLUNK_URL_BASE or not SPLUNK_TOKEN:
    print("Xəta: SPLUNK_URL və ya SPLUNK_TOKEN mühit dəyişənləri tapılmadı!")
    exit(1)

BASE_URL = f"{SPLUNK_URL_BASE}/servicesNS/nobody/search/saved/searches"

# Token əsaslı başlıqlar (Headers)
HEADERS = {
    "Authorization": f"Bearer {SPLUNK_TOKEN}"
}

def deploy_rule(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        rule = yaml.safe_load(f)

    rule_name = rule.get("name")
    search_query = rule.get("search")
    cron_schedule = rule.get("cron", "*/15 * * * *")
    
    if not rule_name or not search_query:
        print(f"Səhv format: {file_path}")
        return

    payload = {
        "name": rule_name,
        "search": search_query,
        "cron_schedule": cron_schedule,
        "is_scheduled": "1",
        "output_mode": "json"
    }

    # Qaydanın mövcud olub-olmadığını token ilə yoxlayırıq
    check_url = f"{BASE_URL}/{rule_name}"
    response = requests.get(check_url, headers=HEADERS, verify=False)

    if response.status_code == 200:
        # Yeniləyirik
        update_url = f"{BASE_URL}/{rule_name}"
        res = requests.post(update_url, headers=HEADERS, data={"search": search_query, "cron_schedule": cron_schedule}, verify=False)
        if res.status_code in [200, 201]:
            print(f"[OK] Qayda yeniləndi: {rule_name}")
        else:
            print(f"[XƏTA] Qayda yenilənmədi: {rule_name} -> {res.text}")
    else:
        # Yeni yaradırıq
        res = requests.post(BASE_URL, headers=HEADERS, data=payload, verify=False)
        if res.status_code in [200, 201]:
            print(f"[OK] Yeni qayda əlavə edildi: {rule_name}")
        else:
            print(f"[XƏTA] Qayda yaradıla bilmədi: {rule_name} -> {res.text}")

def main():
    rule_files = glob.glob("rules/*.yml") + glob.glob("rules/*.yaml")
    if not rule_files:
        print("Heç bir qayda faylı tapılmadı.")
        return

    for file_path in rule_files:
        deploy_rule(file_path)

if __name__ == "__main__":
    main()
