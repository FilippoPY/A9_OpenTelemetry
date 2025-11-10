from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

provider = TracerProvider()
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("task1.demo")

exporter = ConsoleSpanExporter()
provider.add_span_processor(SimpleSpanProcessor(exporter))

with tracer.start_as_current_span("root-span"):
    with tracer.start_as_current_span("child-span"):
        print("Hello OTel: inside child span")
