import os
import subprocess
from PyQt5.QtWidgets import QApplication, QFileDialog

def convert_video_to_720p(ffmpeg_path, input_file, output_file):
    command = [
        ffmpeg_path, 
        '-i', input_file,
        '-s', 'hd720',  # 720p 해상도로 설정
        '-c:v', 'libx264', 
        '-crf', '23', 
        '-c:a', 'aac', 
        '-strict', 
        '-2', 
        output_file
    ]
    subprocess.run(command, shell=False)

def main():
    app = QApplication([])
    ffmpeg_path, _ = QFileDialog.getOpenFileName(
        None, 
        "Select FFmpeg executable", 
        "", 
        "All files (*)"  # 모든 파일을 선택할 수 있도록 변경
    )
    
    if not ffmpeg_path:
        print("FFmpeg executable not selected.")
        return

    input_file, _ = QFileDialog.getOpenFileName(
        None, 
        "Select a video file", 
        "", 
        "Video files (*.mp4 *.avi *.mov *.mxf)"
    )

    if input_file:
        desktop_path = os.path.join(os.path.expanduser("~/Desktop"), "converted_video_720p.mp4")
        convert_video_to_720p(ffmpeg_path, input_file, desktop_path)
        print(f"Converted video saved to {desktop_path}")
    else:
        print("No video file selected.")

if __name__ == "__main__":
    main()
