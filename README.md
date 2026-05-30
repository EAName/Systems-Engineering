# Systems-Engineering

Graduate coursework on cloud-scale data systems: object storage APIs, batch ingestion pipelines, relational and document indexing, distributed Spark analytics, and operational patterns for large-volume public datasets on AWS.

---

## 1. Title and Summary

**Systems Engineering (Big Data / Cloud Data Systems)**  
Northwestern University M.S. in Data Science (Data Engineering specialization): design and implement ingestion, storage, query, and analytics workflows across S3, PostgreSQL, Elasticsearch, and Spark on EMR, with CLI, REST, and GraphQL interfaces to the same storage operations.

---

## 2. Concepts and Methods

- **Object storage operations (AWS S3):** boto3 client for bucket/object CRUD, folder prefixes, upload/download, existence checks (`awsapi.py`); argparse CLI with documented flags (`Commands2RunScripts.txt`)
- **API protocol comparison:** expose identical S3 operations via Flask REST routes (`aws_restapi.py`) and GraphQL mutations/queries with Graphene (`aws_graphapi.py`); Postman collection for REST testing (`AWS S3 Operations.postman_collection.json`)
- **Public dataset ingestion pipelines:** scrape source index pages, download compressed dumps, extract, upload to S3 (`imdbapi.py` for IMDb TSV.gz; `panamaapi.py` for ICIJ Panama/Offshore Leaks zip archives)
- **Fixed-width survey ETL:** download CDC BRFSS fixed-width files; map column positions via `mapping_variable_list.csv`; decode state/activity codes; transform to typed features; bulk index into Amazon Elasticsearch Service with AWS4Auth (`process_brfss_data.py`); Kibana dashboard artifact (`brfss_kibana_dashboard.json`)
- **Document store validation:** connect to managed Elasticsearch cluster and run index counts (`ElasticSearchImportDataValidation.py`)
- **Relational modeling and SQL analytics:** Northwind PostgreSQL schema DDL/DML (`01-PostgreSQLNorthwindScriptDDLDML.sql`); analytical SQL over normalized schema (`02-PostgreSQL_NorthwindInsights.sql`)
- **Interactive analytics (pandas / Spark):** pandas tutorial notebook; Spark SQL and PySpark getting-started notebooks (`01-PandasTutorial.ipynb`, `02-SparkSQLTutorial.ipynb`, `03-GettingStartedWithPySpark.ipynb`)
- **Distributed text analytics on EMR:** author attribution pipeline over literary corpora (Austen/Dickens/Twain text files); Spark ML feature extraction (Tokenizer, StopWordsRemover, NGram, CountVectorizer); MLLib classifiers (Naive Bayes, LogisticRegressionWithLBFGS); S3-backed `wholeTextFiles` reads on EMR (`txt_analytics_EMR.ipynb`)
- **Web scraping:** BeautifulSoup/Requests introductory scrape (`WebScraper-Example1.ipynb`)
- **Cluster bootstrap:** EMR node dependency install script (`emr_install.sh`; boto3, NLTK corpora)
- **Testing:** moto-mocked S3 unit tests for `awsapi` bucket operations (`tests/test_awsapi.py`)

**Course syllabus topic not represented in committed artifacts:** graph database implementation or relational-vs-graph performance benchmarks

**Out of scope for this repo:** Azure-centric batch ETL course implementation (see **Data-Miners**); production analytics web app deployment (see **Analytics-Applications-Engineering**); standalone database prep notebooks (see **Database-Systems-and-Data-Preparation**); algorithm fundamentals (see **Data-Engineering-Algorithms**).

---

## 3. Stack

| Layer | Tools |
|-------|-------|
| Language | Python 3, SQL, Bash |
| Cloud | AWS S3, Amazon Elasticsearch Service, EMR/YARN, Spark |
| AWS SDK / auth | boto3, requests_aws4auth, AWS4Auth |
| Web APIs | Flask, Flask-RESTful, Graphene, flask-graphql |
| Data processing | pandas, NumPy, xport, PySpark, Spark ML / MLLib |
| Search / viz | elasticsearch-py, Kibana dashboard JSON |
| Relational | PostgreSQL (Northwind DDL/DML + insights SQL) |
| Scraping / HTTP | requests, BeautifulSoup |
| Testing | pytest/unittest, moto (`mock_aws`) |
| Ops artifacts | Postman collection, `graphql_queries.txt`, sample CSVs (iris, titanic, wine quality) |

---

## 4. Structure

```
Systems-Engineering/
├── awsapi.py                          # S3 CLI utility
├── aws_restapi.py                     # S3 REST API
├── aws_graphapi.py                    # S3 GraphQL API
├── imdbapi.py                         # IMDb download → S3 pipeline
├── panamaapi.py                       # Panama Papers download → S3 pipeline
├── process_brfss_data.py              # BRFSS fixed-width ETL → Elasticsearch
├── ElasticSearchImportDataValidation.py
├── 01-PandasTutorial.ipynb
├── 02-SparkSQLTutorial.ipynb
├── 03-GettingStartedWithPySpark.ipynb
├── txt_analytics_EMR.ipynb            # Spark author attribution on EMR
├── WebScraper-Example1.ipynb
├── S3 upload notebook.ipynb
├── 01-PostgreSQLNorthwindScriptDDLDML.sql
├── 02-PostgreSQL_NorthwindInsights.sql
├── mapping_*.csv                      # BRFSS codebook mappings
├── brfss_kibana_dashboard.json
├── tests/test_awsapi.py
├── emr_install.sh
├── Austen*.txt, Dickens*.txt, Twain*.txt
└── README.md
```

- **Organization:** reusable S3 module (`awsapi`) consumed by ingestion scripts and mirrored in REST/GraphQL layers; notebooks for exploratory and distributed compute; SQL scripts for relational baseline
- **Reusable modules:** `awsapi` (S3 primitives); ingestion scripts share download/extract/upload pattern
- **Engineering practice:** CLI + API surface parity, large-file ingestion with idempotent upload helpers, schema-driven fixed-width parsing, bulk ES indexing, EMR-side ML feature pipelines, mocked cloud tests without live AWS

---

**Course context:** Northwestern University, M.S. in Data Science, Data Engineering specialization  
**Repository:** https://github.com/EAName/Systems-Engineering
