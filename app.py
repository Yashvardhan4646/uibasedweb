import os
import yt_dlp
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

FFMPEG_PATH = "bin"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    filename = ""

    if request.method == "POST":
        query = request.form.get("query")
        file_type = request.form.get("type")
        quality = request.form.get("quality")

        if not query:
            message = "Please enter something to search"
            return render_template("index.html", message=message)

        ydl_opts = {
            "ffmpeg_location": FFMPEG_PATH,
            "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
            "quiet": True,
            "no_warnings": True,
        }

        if file_type == "mp3":
            ydl_opts.update({
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": quality,
                }],
            })
        else:
            ydl_opts.update({
                "format": f"bestvideo[height<={quality}]+bestaudio/best",
                "merge_output_format": "mp4",
            })

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch1:{query}", download=True)
                title = info["entries"][0]["title"]

                ext = "mp3" if file_type == "mp3" else "mp4"
                filename = f"{title}.{ext}"

            message = "Download ready"

        except Exception as e:
            message = "Error while downloading"

    return render_template("index.html", message=message, filename=filename)


@app.route("/download/<path:filename>")
def download_file(filename):
    return send_from_directory(
        DOWNLOAD_FOLDER,
        filename,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)
