import requests

def test_stylize_image(image_path, style):
    url = "http://localhost:8000/stylize"
    files = {"image": open(image_path, "rb")}
    data = {"style": style}
    
    # Send POST request
    response = requests.post(url, files=files, data=data)
    
    if response.status_code == 200:
        # Save the stylized image to disk
        with open("data/stylized_output.png", "wb") as f:
            f.write(response.content)
        print("Stylized image saved as 'stylized_output.png'")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Example usage
    test_stylize_image("data/input_image.jpg", "pixar")