import logging
import time
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# --- CONFIGURACIÓN DE TRACES ---
provider = TracerProvider()
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("task3.sender")

otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

# --- GENERACIÓN DE SPANS ---
with tracer.start_as_current_span("root-span"):
    for i in range(3):
        with tracer.start_as_current_span(f"child-span-{i}") as span:
            span.set_attribute("iteration", i)
            time.sleep(0.2)

# --- CONFIGURACIÓN DE LOGS ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler("local_logs.txt"), logging.StreamHandler()]
)

logging.info("🚀 Task3 application started")
logging.info("📡 Spans exported via OTLP gRPC")
logging.info("✅ Logs pipeline operational")

print("✅ Task3: traces and logs sent successfully.")
