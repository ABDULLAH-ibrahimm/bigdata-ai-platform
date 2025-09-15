from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

# ==============================
# Config
# ==============================
GITHUB_URL = "https://raw.githubusercontent.com/ABDULLAH-ibrahimm/bigdata-ai-platform/9d55674b154a80ebb5759367ca95750a0a71ba4f/data_sources"
DATA_LAKE = "/mnt/d/grad_bigdata_depi/bigdata-ai-platform/Data_Ingestion"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

# ==============================
# DAG Definition
# ==============================
with DAG(
    dag_id="data_ingestion_github",
    default_args=default_args,
    description="Ingest raw data from GitHub into Data Lake",
    schedule_interval="@daily",
    start_date=datetime.now() - timedelta(days=1),  # <-- دايماً قبل النهاردة بيوم
    catchup=False,
    tags=["ingestion", "github", "datalake"],
) as dag:

    # --------- Transactions (CSV) ---------
    ingest_transactions = BashOperator(
        task_id="ingest_transactions",
        bash_command=f"curl -sSL {GITHUB_URL}/Cust-churn.csv -o {DATA_LAKE}/raw/Cust-churn.csv",
    )

    # --------- Clickstream Logs (CSV) ---------
    ingest_clickstream = BashOperator(
        task_id="ingest_clickstream",
        bash_command=f"curl -sSL {GITHUB_URL}/E-commerce%20Website%20Logs.csv -o {DATA_LAKE}/raw/E-commerce_Website_Logs.csv",
    )

    # --------- Complaints (RAR) ---------
    ingest_complaints = BashOperator(
        task_id="ingest_complaints",
        bash_command=f"curl -sSL {GITHUB_URL}/consumer_complaints.rar -o {DATA_LAKE}/raw/consumer_complaints.rar",
    )

    # --------- Reviews (RAR) ---------
    ingest_reviews = BashOperator(
        task_id="ingest_reviews",
        bash_command=f"curl -sSL {GITHUB_URL}/reviews.rar -o {DATA_LAKE}/raw/reviews.rar",
    )

    # ترتيب التنفيذ
    [ingest_transactions, ingest_clickstream, ingest_complaints, ingest_reviews]
