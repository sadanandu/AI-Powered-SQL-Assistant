from oml.utils import ONNXPipelineConfig, ONNXPipeline

# Choose an appropriate template & sequence length
config = ONNXPipelineConfig.from_template("text", max_seq_length=256, distance_metrics=["COSINE"])
pipeline = ONNXPipeline(model_name="sentence-transformers/all-MiniLM-L12-v2", config=config)

# Export a compatible ONNX model
pipeline.export2file("converted_model", output_dir=".")
