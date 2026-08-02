from PIL import Image
from PIL import ImageDraw
import boto3

# S3 client create
s3 = boto3.client("s3")

rekognition = boto3.client("rekognition")

# Bucket name
bucket_name = "sahil-image-label-generator-2026"

# File name in S3
file_name = "dog.jpg"

# Download location
download_path = "downloads/dog.jpg"

print("Downloading image from S3...")

s3.download_file(bucket_name, file_name, download_path)

print("Image downloaded successfully!")

response = rekognition.detect_labels(
    Image={
        "S3Object": {
            "Bucket": bucket_name,
            "Name": file_name
        }
    },
    MaxLabels=10,
    MinConfidence=80
)

print("\nDetected Labels:\n")

for label in response["Labels"]:
    print(f"{label['Name']} : {label['Confidence']:.2f}%")

print(response)

image = Image.open(download_path)
draw = ImageDraw.Draw(image)

img_width, img_height = image.size

for label in response["Labels"]:

    for instance in label["Instances"]:

        box = instance["BoundingBox"]

        left = box["Left"] * img_width
        top = box["Top"] * img_height
        width = box["Width"] * img_width
        height = box["Height"] * img_height

        draw.rectangle(
            [(left, top), (left + width, top + height)],
            outline="red",
            width=3
        )

        draw.text((left, top - 15), label["Name"], fill="red")

image.save("output/dog_detected.jpg")
image.show()
