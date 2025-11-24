# Counter for ingestion, Counter for queries, Histogram for latency, ASGI app for /metrics endpoint, Labels for endpoint names

from prometheus_client import Counter, Histogram, make_asgi_app

# Counters

INGEST_COUNTER = Counter(
    name="documents_injested_total",
    documentation="Total number of documents successfully injested",
)

QUERY_COUNTER = Counter(
    name="queries_total",
    documentation="Total number of semantic search queries",
)

# Histograms

REQUEST_LATENCY = Histogram(
    name="request_latency_seconds",
    documentation="Latency of request handling in seconds",
    labelnames=["endpoint"],
    # default buckets are fine now, we can tune later for prod
)

# metrics endpoint

metrics_app = make_asgi_app()


