# Systems-Engineering
Design principles and best practices for implementing large-scale systems for data ingestion, processing, storage, and analytics.


Cloud-based computer architecture and scalable systems for data science. Evaluate performance and resource utilization in batch, interactive, and streaming environments.
Review protocols for application programming interfaces.
Compare data models, resource requirements, and performance of applications implemented with relational versus graph database systems.


Key components include:

Jupyter notebooks
Examples cover Pandas (01-PandasTutorial.ipynb), Spark (02-SparkSQLTutorial.ipynb, 03-GettingStartedWithPySpark.ipynb), and general data exploration.
Datasets
Several CSV files (e.g., iris.csv, titanic.csv, winequality-red.csv, winequality-white.csv) and text data (Austen1.txt–Twain5.txt) are included for analysis tasks.
SQL scripts
Files such as 01-PostgreSQLNorthwindScriptDDLDML.sql and 02-PostgreSQL_NorthwindInsights.sql show schema creation and query examples.
AWS S3 utilities
awsapi.py implements command-line operations for listing/creating/deleting buckets, managing folders, and uploading/downloading files. The main CLI parser starts around line 348 and supports operations via arguments like -bo, -oo, and -fo.
aws_restapi.py exposes similar S3 functionality through a Flask REST API, with routes such as /buckets/create and /files/upload.
aws_graphapi.py provides a GraphQL interface wrapping the same operations.
Commands2RunScripts.txt lists example commands for invoking these utilities.
Data ingestion scripts
imdbapi.py downloads IMDb data, decompresses it and uploads files to S3.
panamaapi.py performs similar steps for the Panama Papers dataset.
process_brfss_data.py downloads a large health survey, transforms it with Pandas and loads results into Amazon Elasticsearch Service.
Additional artifacts
Mapping files for BRFSS processing (mapping_* CSVs), a Kibana dashboard definition (brfss_kibana_dashboard.json), Postman collection for S3 API testing, and various text notes/instructions (imdb import steps.txt, graphql_queries.txt).
Important Notes for Newcomers

AWS Credentials: Many scripts assume access to AWS S3 or Elasticsearch. Configure credentials (e.g., via ~/.aws/credentials) before running them.
Dependencies: Packages such as boto3, flask, graphene, requests, pandas, elasticsearch, and requests_aws4auth are required. Some scripts list installation hints in comments (e.g., at the top of process_brfss_data.py).
Data Volume: The ingestion scripts can download and process large files. Be mindful of disk space and network usage.
Command Examples: Refer to Commands2RunScripts.txt for quick command-line examples of how to execute the S3 utilities or ingestion scripts.
Next Steps for Learning

Explore Notebooks
Open the Jupyter notebooks to see data manipulation examples in Pandas and Spark.
Run the S3 utilities
Experiment with awsapi.py locally (or on an EC2 instance) to understand bucket and object management. The README-style commands in Commands2RunScripts.txt are a good starting point.
Examine the API implementations
Compare the REST and GraphQL versions for exposing S3 operations. Consider deploying one locally to test the endpoints.
Dig into the ingestion pipelines
Study imdbapi.py, panamaapi.py, and process_brfss_data.py to see how they download, parse and upload data. These scripts illustrate typical ETL (Extract‑Transform‑Load) patterns with AWS services.
