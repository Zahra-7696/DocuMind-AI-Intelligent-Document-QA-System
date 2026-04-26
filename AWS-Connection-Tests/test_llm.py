import boto3

client = boto3.client("bedrock-runtime", region_name="us-east-1")

response = client.converse(
    modelId="amazon.nova-lite-v1:0",
    messages=[
        {
            "role": "user",
            "content": [
                {"text": "Explain Retrieval-Augmented Generation in two simple sentences."}
            ],
        }
    ],
    inferenceConfig={
        "maxTokens": 200,
        "temperature": 0.3,
        "topP": 0.9,
    },
)

print(response["output"]["message"]["content"][0]["text"])