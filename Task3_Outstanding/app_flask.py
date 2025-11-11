import time
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from opentelemetry import _logs
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
import logging

# --- Tracing setup ---
trace_provider = TracerProvider()
trace.set_tracer_provider(trace_provider)
tracer = trace.get_tracer("task3.outstanding.tracer")

trace_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
trace_provider.add_span_processor(BatchSpanProcessor(trace_exporter))

# --- Logging setup ---
log_provider = LoggerProvider()
_logs.set_logger_provider(log_provider)
log_exporter = OTLPLogExporter(endpoint="http://localhost:4317", insecure=True)
log_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))

handler = LoggingHandler(level=logging.INFO)
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)

# --- Demo activity ---
for i in range(3):
    with tracer.start_as_current_span(f"outstanding-span-{i}") as span:
        span.set_attribute("iteration", i)
        logging.info(f"Processing iteration {i}")
        time.sleep(0.2)

print("✅ Sent traces and logs to Collector.")

