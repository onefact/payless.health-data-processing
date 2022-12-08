# Federal Rules
https://www.federalregister.gov/documents/2019/11/27/2019-24931/medicare-and-medicaid-programs-cy-2020-hospital-outpatient-pps-policy-changes-and-payment-rates-and

2022 update: https://www.federalregister.gov/documents/2021/11/16/2021-24011/medicare-program-hospital-outpatient-prospective-payment-and-ambulatory-surgical-center-payment#h-628

# Database

https://www.dolthub.com/repositories/onefact/paylesshealth/data/main


# Development environment

Install dolt:

`brew install dolt`

Clone the dolthub repo (dolthub is analogous to github, as `dolt` is like `git` and provides a version control systems for databases):
```
dolt clone onefact/paylesshealth
cd paylesshealth && dolt table export hospitals ../hospital-price-transparency/data/hospitals.csv
```