import cv2
import multiprocessing
from math import ceil
from PyQt5.QtWidgets import QApplication, QFileDialog

def process_frames(start, end, input_file):
    print(f"시작 :{start} 끝 : {end} 구간 프레임의 존재 여부를 세보겠습니다.")
    cap = cv2.VideoCapture(input_file)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start)

    count = 0
    error_detected = False
    for frame_num in range(start, end, 7):  # 7프레임 간격으로 증가
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()
        # 프레임의 유효성 검사
        if not ret or frame is None or frame.size == 0:
            error_detected = True
            break
        count += 1

    cap.release()
    
    if error_detected:
        print(f"시작 :{start} 끝 : {end} 구간 프레임에 빠진 프레임이 존재합니다.")
    else:
        print(f"시작 :{start} 끝 : {end} 구간 프레임의 검출 끝 이상없습니다.")
        
    return count, error_detected, (start, end)

def multi_read_opencv(input_file):
    cap = cv2.VideoCapture(input_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    frames_per_process = ceil(total_frames / 5)
    frame_ranges = [(i * frames_per_process, min((i + 1) * frames_per_process, total_frames)) for i in range(5)]

    with multiprocessing.Pool(5) as pool:
        results = pool.starmap(process_frames, [(start, end, input_file) for start, end in frame_ranges])

    total_read_frames = sum(result[0] for result in results)
    for count, error_detected, frame_range in results:
        if error_detected:
            print(f"Error detected in frames range: {frame_range}")

    return fps, total_frames, total_read_frames



if __name__ == "__main__":
    app = QApplication([])
    input_file, _ = QFileDialog.getOpenFileName(
        None, 
        "Select a video file", 
        "", 
        "Video files (*.mp4 *.avi *.mov *.mxf)"
    )

    if input_file:
        fps, total_frames, total_read_frames = multi_read_opencv(input_file)
        print(f"FPS: {fps}, Total Frames: {total_frames}, Total Read Frames: {total_read_frames}")
    else:
        print("No file selected.")