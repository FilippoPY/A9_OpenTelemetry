import time
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Configuración del tracer
provider = TracerProvider()
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("task2.sender")

# Exportador OTLP (Collector en localhost)
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

# Crear algunos spans de prueba
for i in range(3):
    with tracer.start_as_current_span(f"work-span-{i}") as span:
        span.set_attribute("iteration", i)
        time.sleep(0.2)

print("✅ Traces sent to Collector")
