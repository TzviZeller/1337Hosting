# 1337Hosting 2.0

---

I intend to use this fork as an opportunity to learn K8 and various GCP services.

## Architecture

I plan on building two dockerized services, an nginx service that serves cached images and ingests new pictures. The second service is a backend built in flask to ingest new photos into memorystore backend and direct request not in nginx cache.

Currently the CI/CD pipeline is Cloud Build --> GCR --> New revision of an existing K8 deployment 

