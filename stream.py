import gdown
import subprocess
import time
import os
from main import keep_alive  # 👈 Import uptime server thread

# 🔃 Start Flask keep-alive
keep_alive()

# 🎬 Google Drive video config
drive_id = "1-iC97qVqueAT0kHL0sS93DBqZJpsP_ds"
video_file = "video.mp4"
stream_key = "3gr0-q51j-d1ct-8702-bdb7"
stream_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

def download_video():
    print("📥 Checking for existing video...")
    if os.path.exists(video_file):
        print("✅ Video already exists. Validating...")
        return validate_video()

    try:
        print("🌐 Downloading from Google Drive...")
        gdown.download(
            url=f"https://drive.google.com/uc?id={drive_id}",
            output=video_file,
            quiet=False
        )
        print("✅ Download complete.")
        validate_video()
    except Exception as e:
        print(f"❌ Download failed: {e}")
        time.sleep(5)
        exit(1)

def validate_video():
    result = subprocess.run(["ffprobe", video_file], capture_output=True, text=True)
    if "Duration" not in result.stderr and "Duration" not in result.stdout:
        print("🚫 Invalid video. Removing corrupted file...")
        os.remove(video_file)
        exit(1)

def stream_loop():
    while True:
        print("🚀 Starting stream...")
        result = subprocess.run([
            "ffmpeg",
            "-re",
            "-i", video_file,
            "-c:v", "copy",
            "-c:a", "aac",
            "-f", "flv",
            stream_url
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print("⚠️ FFmpeg crashed. Error:\n", result.stderr)
            print("🔁 Retrying in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    download_video()
    stream_loop()
