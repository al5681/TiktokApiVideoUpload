
import requests
import os

# Replace with your TikTok API credentials
ACCESS_TOKEN = 'abc'
VIDEO_FILE_PATH = r'abc'

video_size = os.path.getsize(VIDEO_FILE_PATH )  # Get the video size in bytes
chunk_size = video_size  # Set chunk size to video size for a single upload

# Function to initialize video upload
def initialize_video_upload(title, privacy_level="SELF_ONLY"):
    url = "https://open.tiktokapis.com/v2/post/publish/video/init/"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json; charset=UTF-8"
    }
    payload = {
        "post_info": {
            "title": title,
            "privacy_level": privacy_level,
            "disable_duet": False,
            "disable_comment": False,
            "disable_stitch": False,
            "video_cover_timestamp_ms": 1000
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": video_size,  # Replace with actual video size in bytes
            "chunk_size": chunk_size,
            "total_chunk_count": 1
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200 and response.json().get("error", {}).get("code") == "ok":
        return response.json()["data"]["upload_url"], response.json()["data"]["publish_id"]
    else:
        raise Exception(f"Initialization failed: {response.text}")

# Function to upload video file
def upload_video(upload_url, file_path):
    headers = {
        "Content-Range": f"bytes 0-{len(open(file_path, 'rb').read()) - 1}/{len(open(file_path, 'rb').read())}",
        "Content-Type": "video/mp4"
    }
    with open(file_path, "rb") as video_file:
        response = requests.put(upload_url, headers=headers, data=video_file)
    if response.status_code == 200 or 201:
        print("Video uploaded successfully.")
    else:
        raise Exception(f"Video upload failed: {response.text}")

# Function to check post status
def check_post_status(publish_id):
    url = "https://open.tiktokapis.com/v2/post/publish/status/fetch/"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json; charset=UTF-8"
    }
    payload = {
        "publish_id": publish_id
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch post status: {response.text}")

# Main function
def main():
    try:
        print("Initializing video upload...")
        upload_url, publish_id = initialize_video_upload("My Awesome TikTok Video")
        print(f"Upload URL: {upload_url}")
        print(f"Publish ID: {publish_id}")

        print("Uploading video...")
        upload_video(upload_url, VIDEO_FILE_PATH)

        print("Checking post status...")
        status = check_post_status(publish_id)
        print(f"Post status: {status}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
