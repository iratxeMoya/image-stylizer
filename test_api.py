import requests
import time
import argparse

# API endpoints
BASE_URL = "http://127.0.0.1:8000"  # Replace with your actual FastAPI server URL if different
UPLOAD_ENDPOINT = f"{BASE_URL}/style-transfer/"
RESULT_ENDPOINT = f"{BASE_URL}/result/"

# Step 1: Upload Image for Style Transfer
def upload_image(file_path, style):
    with open(file_path, "rb") as image_file:
        # Prepare the payload for the POST request
        files = {"file": (file_path, image_file)}
        data = {"style": style}

        response = requests.post(UPLOAD_ENDPOINT, files=files, data=data)
        
        if response.status_code == 200:
            # Extract image ID from response
            result = response.json()
            print(f"Upload successful! Image ID: {result['image_id']}")
            return result['image_id']
        else:
            print(f"Error during upload: {response.status_code} - {response.text}")
            return None

# Step 2: Get the Processed Result
def get_processed_image(image_id):
    # Construct the result endpoint
    result_url = f"{RESULT_ENDPOINT}{image_id}"

    while True:
        # Check if the processed image is ready
        response = requests.get(result_url)
        
        if response.status_code == 200:
            # Save the processed image to a file
            output_file = f"processed_{image_id}.png"
            with open(output_file, "wb") as f:
                f.write(response.content)
            print(f"Processed image saved as {output_file}")
            break
        elif response.status_code == 404:
            # If the result is not ready yet, wait and try again
            print("Result not ready yet, retrying in 5 seconds...")
            time.sleep(60)
        else:
            print(f"Error while fetching result: {response.status_code} - {response.text}")
            break

# Main function
if __name__ == "__main__":
    # Argument parser for command-line input
    parser = argparse.ArgumentParser(description="Image Style Transfer")
    parser.add_argument("image_file_path", type=str, help="Path to the image file to upload", default='data/input_image.jpg')
    parser.add_argument(
        "style_option",
        type=str,
        choices=["anime", "pixar", "watercolor", "oleo", "pixel art"],
        help="Style option to apply (choices: anime, pixar, watercolor, oleo, pixel art)"
    )

    # Parse the arguments
    args = parser.parse_args()

    # Run the process
    image_id = upload_image(args.image_file_path, args.style_option)
    # if image_id:
    #     get_processed_image(image_id)