# Splunk Detection Rules (Detection as Code)

Bu repozitoriya **Splunk SIEM** sistemi üçün nəzərdə tutulmuş peşəkar aşkarçılama qaydalarını (detection rules) ehtiva edir[cite: 5, 6]. Layihə müasir SOC mühitlərində tətbiq olunan "Detection as Code" prinsipləri əsasında qurulmuşdur[cite: 5, 6].

## Layihənin Məqsədi

Aşkarlama qaydalarının birbaşa SIEM interfeysində deyil, mərkəzləşdirilmiş GitHub mühitində idarə olunmasını, versiya nəzarətini və API vasitəsilə SIEM-ə avtomatik inteqrasiyasını təmin etməkdir[cite: 5, 6].

## Repozitoriyanın Strukturu

* `/rules/splunk`: Splunk üçün SPL (Search Processing Language) formatında hazırlanmış peşəkar qaydalar[cite: 5, 6].
* `/scripts`: Qaydaların GitHub-dan Splunk API-nə sinxronizasiyası üçün nəzərdə tutulmuş avtomatlaşdırma skriptləri[cite: 5, 6].

## İstifadə Olunan Texnologiyalar

* **SIEM:** Splunk[cite: 5, 6]
* **Version Control:** GitHub[cite: 5, 6]
* **Automation:** Python (Splunk SDK / REST API)[cite: 5, 6]
* **Log Source:** Docker JSON logs[cite: 5, 6]
