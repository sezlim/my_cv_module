# -*- coding: utf-8 -*-

import sys
import re
import subprocess
import socket
import os
import random
import cv2
import numpy as np
import psutil
import time
from pymediainfo import MediaInfo
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import librosa
from scipy.io import wavfile
import wave
import shutil
import datetime
from pydub import AudioSegment
from threading import Thread, Event
import json
from datetime import datetime, timedelta




def want_know_korea_word_in_path():
    def contains_korean(text):
        return any('\uAC00' <= char <= '\uD7A3' for char in text)

    # 현재 실행 중인 파이썬 인터프리터의 절대 경로
    current_dir = os.path.dirname(sys.executable)

    # 경로에 한글이 포함되어 있는지 확인
    if contains_korean(current_dir):
        print("경로에 한글이 포함되어 있습니다:", current_dir)
        return True
    else:
        print("경로에 한글이 포함되어 있지 않습니다.", current_dir)
        return False



def make_folder(parent_folder, folder_name, clear=True):
    # 폴더 경로 생성
    folder_path = os.path.join(parent_folder, folder_name)

    # 폴더가 이미 존재하는 경우
    if os.path.exists(folder_path):
        if clear == True:
            # clear가 True이면 폴더 내부의 모든 내용을 지웁니다.
            try:
                for filename in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print(f'Failed to delete {file_path}. Reason: {e}')
            except Exception as e:
                print(f'Failed to clear folder: {folder_path}. Reason: {e}')
    else:
        # 폴더가 존재하지 않으면 새로 생성합니다.
        try:
            os.makedirs(folder_path)
        except Exception as e:
            print(f'Failed to create folder: {folder_path}. Reason: {e}')

## 사용에시
## make_folder(r'/Users/imsejin/Desktop/입', "new_folder",True) << 이미 폴더가 있을 시 "new_folder" 내부 파일들 모두 삭제
## make_folder(r'/Users/imsejin/Desktop/입', "new_folder",False) << 이미 폴더가 있을 시 "new_folder" 내부 파일 유지



def get_my_ip_address():
    try:
        # Create a socket
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Connect to an external server (here, Google's DNS server) to determine the local IP
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
    except:
        try:
            # subprocess를 실행할 때 CMD 창이 뜨지 않도록 하는 설정입니다.
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            # ipconfig 명령을 실행하여 결과를 받아옵니다.
            result = subprocess.run(['ipconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True,
                                    startupinfo=startupinfo)

            # 정규 표현식을 사용하여 IPv4 주소를 찾습니다.
            ip_list = re.findall(r'IPv4 Address[. ]*: (\d+\.\d+\.\d+\.\d+)', result.stdout)
            if not ip_list:  # 첫 번째 방법으로 IP 주소를 찾지 못한 경우 두 번째 패턴 시도
                ip_list = re.findall(r'IPv4 주소[. ]*: (\d+\.\d+\.\d+\.\d+)', result.stdout)

            ip = ip_list[0] if ip_list else "Unable to determine IP"
        except Exception:
            ip = "Unable to determine IP"

    return ip



def compare_file_size_with_folder_capacity(file_path, folder_path, mutiple):
    ## 파일크기 비교 mutiple의 경우 몇배 이상이냐를 나타낸다.

    # 파일 크기를 바이트 단위로 얻음
    file_size = os.path.getsize(file_path)

    # 폴더의 가용 용량을 얻음
    _, _, free_space = shutil.disk_usage(folder_path)

    # 파일 크기와 폴더의 가용 용량 비교
    if file_size * int(mutiple) <= free_space:
        return True
    else:
        return False
######################################################################################
def find_ffmpeg_path():
    # 현재 Python 실행 파일의 경로를 가져옵니다.
    executable_path = sys.executable

    # Python 실행 파일의 기본 디렉토리를 구합니다.
    base_path = os.path.dirname(executable_path)

    # 다양한 운영 체제에 대한 대상 파일들을 정의합니다.
    target_files = ['ffmpeg', 'ffmpeg.exe']

    # 주어진 디렉토리에서 대상 파일들을 찾는 함수입니다.
    def find_files(directory, filenames):
        for root, dirs, files in os.walk(directory):
            for filename in filenames:
                if filename in files:
                    return {filename: os.path.join(root, filename)}
        return {}

    # 대상 파일들을 검색합니다.
    found = find_files(base_path, target_files)

    # 만약 찾지 못했다면 None을 반환합니다.
    ffmpeg_path = found.get('ffmpeg', found.get('ffmpeg.exe', None))

    return ffmpeg_path
def disable_to_read_by_opencv_change_the_format(input_file_path,fail_folder_path):
    _, file_extension = os.path.splitext(input_file_path)
    ffmpeg_path = find_ffmpeg_path()
    cap = cv2.VideoCapture(input_file_path)
    fps = (cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames-1)
    ret, frame = cap.read()
    cap.release()
    fps = int(fps)
    if fps == 29:
        fps = 30000/1001
    elif fps == 59:
        fps = 60000/1001
    if not ret or  file_extension.lower() == ".mkv" or  file_extension.lower() == ".avi":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        print("미지원 코덱의 변환을 시도해 봅니다.")
        # 입력 파일 경로에서 확장자를 제외한 부분을 기반으로 출력 파일 경로 생성
        outputfile_path = os.path.splitext(input_file_path)[0] + '.mov'

        # FFmpeg 명령 구성
        command = [
            ffmpeg_path,  # FFmpeg 실행 파일 경로
            '-i', input_file_path,  # 입력 파일
            '-c:v', 'prores_ks',  # 비디오 코덱 설정 (ProRes)
            '-profile:v', '3',  # ProRes 프로파일 설정 (3은 HQ에 해당)
            '-vendor', 'apl0',
            '-pix_fmt', 'yuv422p10le',  # 픽셀 포맷 설정
            '-c:a', 'pcm_s16le',  # 오디오 코덱 설정 (PCM 16비트 리틀 엔디언)
            outputfile_path  # 출력 파일
        ]

        # FFmpeg 명령 실행
        try:
            subprocess.run(command, check=True,startupinfo=startupinfo)
            print(f"변환 성공: {outputfile_path}")
            time.sleep(1)
            try:
                os.remove(input_file_path)
            except:
                pass

            raise
        except subprocess.CalledProcessError as e:
            print(f"변환 실패, 입력 파일 실패 폴더로 이동 중: {e}")
            try:
                destination_file_path = os.path.join(fail_folder_path,os.path.basename(input_file_path))
                if os.path.exists(destination_file_path):
                    # 동일한 이름의 파일이 있으면, 새로운 파일 이름 생성 (예: 이름에 "_(중복)" 추가)
                    new_file_name = os.path.splitext(file_name)[0] + "_(중복)" + os.path.splitext(file_name)[1]
                    destination_file_path = os.path.join(fail_folder_path, new_file_name)
                shutil.move(input_file_path,destination_file_path)
                raise
            except OSError as e:
                print(f" {e}")
                raise

    else:
        return
def move_ip_file_to_local(net_working_folder_path, working_folder):
    fail_folder_path = os.path.join(os.path.dirname(net_working_folder_path), "(실패)_코덱_미지원_파일")
    try:
        os.mkdir(fail_folder_path)
    except:
        pass

    # 지원하는 확장자 리스트
    supported_extensions = ['mxf', 'mov', 'mp4','mkv','avi']

    # 파일 목록을 찾고 필터링
    files = [f for f in os.listdir(net_working_folder_path)
             if os.path.isfile(os.path.join(net_working_folder_path, f))
             and f.lower().split('.')[-1] in supported_extensions]

    # 파일 목록이 비어있지 않은지 확인
    if not files:
        return

    # 파일 목록 섞기
    random.shuffle(files)

    # 첫 번째 파일 선택
    file_to_move = files[0]
    full_path_of_file =os.path.join(net_working_folder_path, file_to_move)
    disable_to_read_by_opencv_change_the_format(full_path_of_file, fail_folder_path)

    folder_capacity_able_to_use = compare_file_size_with_folder_capacity(os.path.join(net_working_folder_path, file_to_move), working_folder, 10)

    if folder_capacity_able_to_use == True:
        # 파일 복사
        shutil.copy(os.path.join(net_working_folder_path, file_to_move), working_folder)
        print(f"'{file_to_move}' 파일이 '{working_folder}'로 복사되었습니다.")

        movied_file_path = os.path.join(working_folder,file_to_move)
        return  movied_file_path
    elif folder_capacity_able_to_use == False:
        file =os.path.join(net_working_folder_path, file_to_move)
        path_of_fail_folder = os.path.join(os.path.dirname(net_working_folder_path),"작업실패파일_PC의_용량이부족합니다.")
        make_folder(os.path.dirname(net_working_folder_path),"작업실패파일_PC의_용량이부족합니다.", False)

        # 파일의 이름을 얻음
        file_name = os.path.basename(file)

        # 최종 목적지 경로
        final_dst = os.path.join(path_of_fail_folder, file_name)

        # 파일 이름이 중복되는 경우 이름 변경
        counter = 1
        while os.path.exists(final_dst):
            # 파일 이름에 카운터 추가
            name, ext = os.path.splitext(file_name)
            new_name = f"{name}_{counter}{ext}"
            final_dst = os.path.join(path_of_fail_folder, new_name)
            counter += 1

        shutil.move(file,final_dst)

###########################################

def create_video_with_still_frames(video_path, fps, output_folder_path, start_frame_num, end_frame_num, still_frame,ffmpeg_path,selected_resolution,selected_channel,selected_still_time):
    fps = int(fps)
    if fps == 29:
        fps = 30000/1001
    elif fps == 59:
        fps = 60000/1001

    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # Define the extensions
        _, file_extension = os.path.splitext(video_path)
        video_extension = ".mov" #mxf로 하니까 앞에 블랙이 있으면 안짤려 ;;;
        print(f" 추출할 프레임은 {end_frame_num}")
        # Extract directory path from output_path
        output_dir = output_folder_path

        temp_output_filename = "temp" + video_extension
        temp_output_path = os.path.join(output_dir, temp_output_filename)

##############################################
        if selected_resolution == "HD":
            resolution = f'{1920}x{1080}'
        else:
            resolution = f'{3840}x{2160}'

        print(f"{resolution} {start_frame_num}프레임부터 {end_frame_num}까지로 진행합니다.")

        ffmpeg_command = [
            str(ffmpeg_path),
            '-i', str(video_path),
            '-r', str(fps),
            '-vf', f'trim=start_frame={str(start_frame_num)}:end_frame={str(end_frame_num)},setpts=PTS-STARTPTS',
            '-an',  # remove audio
            '-map', '0:v:0',  # select only the first video stream
            '-s', str(resolution),  # set resolution to the video's resolution
            '-c:v', 'libx264',  # set video codec to H.264
            '-crf', '18',
            '-preset', 'ultrafast',  # fastest encoding, but larger file size
            str(temp_output_path)
        ]

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        # 명령 실행
        process = subprocess.Popen(ffmpeg_command, startupinfo=startupinfo)
        ffmpeg_pid = process.pid
        process.wait()
        # 작업이 끝난 후 ffmpeg가 여전히 실행 중인지 확인
        if psutil.pid_exists(ffmpeg_pid):
            print("ffmpeg가 여전히 실행 중. 강제 종료합니다.")
            psutil.Process(ffmpeg_pid).terminate()

        # still_frame = cv2.cvtColor(still_frame, cv2.COLOR_BGR2RGB)
        if str(selected_still_time) == "0":
            print("스틸이 0초라 그냥 끝내면 됨")
            return
        else:
        # JPEG로 저장하고 품질을 100로 설정

            if os.path.isfile('still_frame.png'):
                os.remove('still_frame.png')  # 파일이 이미 존재하면 삭제합니다.

            if os.path.isfile('re_still_frame.png'):
                os.remove('re_still_frame.png')  # 파일이 이미 존재하면 삭제합니다.

            cv2.imwrite('still_frame.png', still_frame, [cv2.IMWRITE_JPEG_QUALITY, 100])## 100으로 바꿔보자

            ffmpeg_resize_command = [
                str(ffmpeg_path),
                '-i', 'still_frame.png',
                '-s', str(resolution),
                're_still_frame.png'
            ]

            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            # ffmpeg_resize_command 실행
            process = subprocess.Popen(ffmpeg_resize_command, startupinfo=startupinfo)
            ffmpeg_pid = process.pid
            process.wait()
            # 작업이 끝난 후 ffmpeg가 여전히 실행 중인지 확인
            if psutil.pid_exists(ffmpeg_pid):
                print("ffmpeg가 여전히 실행 중. 강제 종료합니다.")
                psutil.Process(ffmpeg_pid).terminate()

            os.remove('still_frame.png')

            still_output_filename = "still" + video_extension
            still_output_path = os.path.join(output_dir, still_output_filename)

            print(f"{selected_still_time}의 길이로 스틸을 제조합니다.")
            command = [
                str(ffmpeg_path),
                '-loop', '1',
                '-i', 're_still_frame.png',
                '-c:v', 'libx264',
                '-crf', '18',
                '-t', str(selected_still_time),
                '-r', str(fps),  # FPS 설정 부분
                '-s', str(resolution),
                '-preset', 'ultrafast',
                str(still_output_path)
            ]

            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            # 명령 실행
            process = subprocess.Popen(command, startupinfo=startupinfo)
            ffmpeg_pid = process.pid
            process.wait()

            # 작업이 끝난 후 ffmpeg가 여전히 실행 중인지 확인
            if psutil.pid_exists(ffmpeg_pid):
                print("ffmpeg가 여전히 실행 중. 강제 종료합니다.")
                psutil.Process(ffmpeg_pid).terminate()

            os.remove('re_still_frame.png')


            total_video_path = os.path.join(output_dir, "final" + video_extension )
            temp_output_path = temp_output_path.replace("\\", "/")
            still_output_path = still_output_path.replace("\\", "/")

            with open('files.txt', 'w', encoding='utf-8') as f:
                f.write(f"file '{temp_output_path}'\n")
                f.write(f"file '{still_output_path}'\n")

            # ffmpeg 명령 실행
            command = [
                str(ffmpeg_path),
                '-f', 'concat',
                '-safe', '0',
                '-probesize', '50M',
                '-analyzeduration', '100M',
                '-i', 'files.txt',
                '-c:v', 'copy',
                '-an',
                str(total_video_path)
            ]

            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            # 명령 실행
            process = subprocess.Popen(command, startupinfo=startupinfo)
            ffmpeg_pid = process.pid
            process.wait()
            # 작업이 끝난 후 ffmpeg가 여전히 실행 중인지 확인
            if psutil.pid_exists(ffmpeg_pid):
                print("ffmpeg가 여전히 실행 중. 강제 종료합니다.")
                psutil.Process(ffmpeg_pid).terminate()

            time.sleep(1)
            basename = os.path.basename(total_video_path)
            dirname = os.path.dirname(total_video_path)
            video_folder = os.path.join(dirname,"video_temp")

            shutil.move(total_video_path,video_folder)
            os.remove(still_output_path)
            os.remove(temp_output_path)

    except subprocess.CalledProcessError as e:
        print(f"오류 발생: {str(e)}")

def get_audio_duration(ffmpeg_path, video_path):
    full_audio_state = 0
    silence_parts =[]
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    try:
        # ffmpeg를 사용하여 오디오의 무음 부분을 탐지합니다.
        command = [
            ffmpeg_path,
            "-i", video_path,
            "-af", "silencedetect=noise=-30dB:d=0.5",
            "-f", "null", "-"
        ]
        result = subprocess.run(command,startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
        stderr = result.stderr

        if not isinstance(stderr, str):
            stderr = stderr.decode('utf-8')  # stderr를 문자열로 변환합니다.
        # 무음 부분의 시작과 종료 시간을 찾습니다.

        pattern = r'\[silencedetect @ [0-9a-f]+\] silence_(start|end): ([0-9.]+)'

        try:
            silence_parts = re.findall(pattern, stderr)
        except Exception as e:
            print("오류 발생:", e)
    except:
        full_audio_state = 1  ## 통으로 오디오가 조금도 비지 않는경우가 있네;; 그때는 밑에 구문을 사용


    if not silence_parts or full_audio_state ==1:
        # 무음 부분이 없는 경우, 전체 오디오 길이 반환
        ffprobe_path = os.path.join(os.path.dirname(ffmpeg_path), "ffprobe.exe")
        command = [
            ffprobe_path,
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "json",
            video_path
        ]

        result = subprocess.run(command,startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        duration = json.loads(result.stdout)['format']['duration']

        return float(duration) , 0 , float(duration)

    if len(silence_parts) == 2:
        temp_1 = ('start', '0')  # 실제 튜플
        temp_2 = ('end', '0')  # 실제 튜플
        temp_3 = silence_parts[0]
        temp_4 = silence_parts[1]
        silence_parts = []
        silence_parts.append(temp_1)
        silence_parts.append(temp_2)
        silence_parts.append(temp_3)
        silence_parts.append(temp_4)
        print(silence_parts)


    # 첫 무음 시작 시간과 마지막 무음 종료 시간을 찾습니다.
    first_silence_start = float(silence_parts[1][1])
    last_silence_end = float(silence_parts[-2][1]) if silence_parts[-1][0] == 'end' else get_audio_duration(ffmpeg_path, video_path)
    #[('start', '0'), ('end', '39.211'), ('start', '78.9296'), ('end', '97.472')] 이런식으로 나와서 가운데 2개를 뻈는데 추후 수정 여부 확인
    print(f"시작시간 :{first_silence_start}")
    print(f" 끝 시간 : {last_silence_end}")
    print(f" 길이는 : {(last_silence_end)-(first_silence_start)}")
    # 소리가 시작되는 첫 지점부터 끝나는 마지막 지점 사이의 길이를 반환합니다.

    return abs(last_silence_end) - abs(first_silence_start),abs(first_silence_start) ,abs(last_silence_end)


def compare_frames(frame_1, frame_2):

    grid_size = 6
    h, w = frame_1.shape[:2]
    grid_h, grid_w = h // grid_size, w // grid_size

    change_detected = False

    for i in range(grid_size):
        for j in range(grid_size):
            # 각 그리드의 시작점과 끝점을 계산합니다.
            start_row, start_col = i * grid_h, j * grid_w
            end_row, end_col = start_row + grid_h, start_col + grid_w

            # 각 그리드에 대한 상관관계를 계산합니다.
            grid_1 = frame_1[start_row:end_row, start_col:end_col]
            grid_2 = frame_2[start_row:end_row, start_col:end_col]
            correlation = calculate_correlation(grid_1, grid_2)

            # 상관관계가 임계값보다 낮은 경우, 출력합니다.
            if correlation < 0.998:
                print(f"Grid ({i}, {j}) - Correlation: {correlation}")
                change_detected = True
                return change_detected

    if not change_detected:
        change_detected = False
        return change_detected

def calculate_correlation(frame1, frame2):
    # 두 프레임이 완전히 같은지 확인
    return np.corrcoef(frame1.flatten(), frame2.flatten())[0, 1]
## -1에서 1 사이의 값을 리턴으로 갖는다.

def compare_frames(frame_1, frame_2): ## 36분할을 시도합니다.

    grid_size = 6
    h, w = frame_1.shape[:2]
    grid_h, grid_w = h // grid_size, w // grid_size
    cnt = 0
    change_detected = False

    for i in range(grid_size):
        for j in range(grid_size):
            # 각 그리드의 시작점과 끝점을 계산합니다.
            start_row, start_col = i * grid_h, j * grid_w
            end_row, end_col = start_row + grid_h, start_col + grid_w

            # 각 그리드에 대한 상관관계를 계산합니다.
            grid_1 = frame_1[start_row:end_row, start_col:end_col]
            grid_2 = frame_2[start_row:end_row, start_col:end_col]
            correlation = calculate_correlation(grid_1, grid_2)

            # 상관관계가 임계값보다 낮은 경우, 출력합니다.
            if correlation < 0.9998:
                print(f"Grid ({i}, {j}) - Correlation: {correlation}")
                cnt +=1
                change_detected = True
                return change_detected,cnt

    if not change_detected:
        change_detected = False
        return change_detected ,0


def append_still_frame_to_end(video_path, output_path,net_ip_folder_path, ffmpeg_path,selected_resolution,selected_channel,selected_still_time):


    print(f"selected still time : {selected_still_time}")
    base_name = os.path.basename(video_path)
    name, ext = os.path.splitext(base_name)
    file_name = name + ext

    output_folder_path = os.path.dirname(output_path)

    ###### step 0 앞에서 부터 읽어서 start_frame을 계산한다. , audio start 시간과 비교해서 더 빠른 시간으로 선택한다.
    cap = cv2.VideoCapture(video_path)
    fps = (cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_count = 0

    fps = int(fps)
    if fps == 29:
        fps = 30000/1001
    elif fps == 59:
        fps = 60000/1001

    while True:
        # 동영상에서 프레임을 읽어옴
        ret, frame = cap.read()

        # 더 이상 읽을 프레임이 없으면 반복문 종료
        if not ret:
            cap.release()
            raise

        # RGB 평균 계산
        mean_rgb = np.mean(frame)

        # RGB 평균이 8 이상이면 출력
        if mean_rgb > 8:
            start_frame_num = frame_count
            break
        frame_count += 1

    cap.release()

    audio_cal = get_audio_duration(ffmpeg_path, video_path)

    original_audio_length = audio_cal[0]
    start_time_of_audio = audio_cal[1]
    end_time_of_audio = audio_cal[2]

    print(f"오디오 시작 시간 :{start_time_of_audio}")
    print(f"오디오 끝 시간: {end_time_of_audio}")
    start_frame_num = start_frame_num
    start_frame_time = float(start_frame_num / fps)
    if int(start_time_of_audio) == 0 and int(end_time_of_audio) == 0:
        print("무음인 파일이라 종료 합니다.") ### 무음 파일일 경우 처리하지 않고 종료
        base_name = os.path.basename(video_path)
        net_remove_file_path = os.path.join(net_ip_folder_path,base_name)
        os.remove(net_remove_file_path)
        os.remove(video_path)
        raise

    #if int(start_time_of_audio*fps) < start_frame_num:
     #   start_frame_num = int(start_time_of_audio*fps)
      #  start_frame_time = float(start_frame_num/fps)
    #else:
     #   start_frame_num = start_frame_num
      #  start_frame_time = float(start_frame_num/fps)

    ###### step 0 끝 ###########################################################################


    #### step 1 블랙이 있다면 블랙 화면 직전까지 접근 -시작-
    video_path = video_path.replace('/', '\\')
    cap = cv2.VideoCapture(video_path)
    fps = (cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    fps = int(fps)
    if fps == 29:
        fps = 30000/1001
    elif fps == 59:
        fps = 60000/1001

    ## 0부터 시작이라 total_frames-1로 접근해야함
    for frame_number in range(total_frames - 1, -1, -1):
        cap = cv2.VideoCapture(video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            os.remove(os.path.join(net_ip_folder_path,os.path.basename(video_path)))
            raise
        variance = np.var(frame)
        # print(f"분산 값 :{variance}")
        # 0으로 나옵니다. 0.1로 경계값 해도 충분할 듯
        if variance < 0.1 :
            continue
        average_color = frame.mean()
        if average_color > 0.1:
            first_non_black_frame_cnt = frame_number
            prev_frame = frame
            break

    print("3까지 됨")
    #### step 1 블랙이 있다면 블랙 화면 직전까지 접근 -끝-

    cut_1_disolve_2_move_3_still_4 = 0 #cut,disolve, move 인지 판단하는 코드
    print("4까지 됨")
    ###################################################### step 2 끝 #################################
    if cut_1_disolve_2_move_3_still_4 == 0:
        ## 프레임만 5개 읽어봐서 still인지 확인해 보자 5프레임 간격
        target_frame = prev_frame
        frame_num = first_non_black_frame_cnt
        #### 5개 읽어볼 때 비교할 프레임
        i_want_know_still = 0
        if total_frames > 5:
            for i in range(1,6):
                cap = cv2.VideoCapture(video_path)
                cap.set(cv2.CAP_PROP_POS_FRAMES, first_non_black_frame_cnt -4*i)
                ret, frame = cap.read()
                cap.release()

                result = compare_frames(target_frame, frame)
                seperate_change = result[0]
                seperate_change_cnt = result[1]
                if not seperate_change:
                    print("스틸인 것 같습니다.")
                    i_want_know_still = 1

        if i_want_know_still == 1:
            cut_1_disolve_2_move_3_still_4 = 4
            ### 스틸 입니다.
    ###########################################################################

    if cut_1_disolve_2_move_3_still_4 == 0 and '_(_추가제안버전_)_' not in file_name:
        #### 디졸브와 단순 변화의 차이를 보기위해 0.5초기간의 밝기 값을 본다.
        brightness_values =[]

        prev_frame_mean =prev_frame.mean()
        gray_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)  # 그레이스케일로 변환
        brightness = gray_frame.mean()  # 밝기 값 계산
        brightness_values.append(brightness)  # 밝기 값 저장

        for i in range(1,int(fps/2)-2): ## 보통 1초 디졸브 해보면 알 수 있는데 2프레임은 정확도 향상을 위해 뺀다.
            cap = cv2.VideoCapture(video_path)
            cap.set(cv2.CAP_PROP_POS_FRAMES, first_non_black_frame_cnt - i)
            ret, frame = cap.read()
            cap.release()
            if ret:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 그레이스케일로 변환
                brightness = gray_frame.mean()  # 밝기 값 계산
                brightness_values.append(brightness)  # 밝기 값 저장

        # 첫 번째 요소와 나머지 요소들과의 차이를 계산하고 절대값을 취함
        differences = [abs(brightness_values[0] - value) for value in brightness_values[1:]]
        adjacent_differences = [abs(differences[i] - differences[i - 1]) for i in range(1, len(differences))]


        # 바로 앞 요소와의 차이를 구해본다.
        average_difference = sum(differences) / len(differences)

        # 결과 출력
        print("밝기값 Differences:", differences)
        print("변화값 average_ Differences :",adjacent_differences)
        # differences 리스트의 평균값을 계산하고 출력
        average_adjacent_differences = sum(adjacent_differences) / len(adjacent_differences)
        print("밝기 값 변화 평균 Average difference:", average_adjacent_differences)

        all_elements_less_than_015 = all(diff < 0.15 for diff in adjacent_differences) # adjacent_differences의 모든 값이 0.15보다 작은지 큰지 확인해 본다.
        ##### 디졸브 전환은 평균 차이값이 20이상이 나온다.
        ##### average_difference < 30 여기를 실험값으로 가야 할 거 같아 테스트가 필요함
        if prev_frame_mean >= 10:
            print("단순 이동 인것 같습니다.")
            cut_1_disolve_2_move_3_still_4 = 3
        elif average_difference < 10 and abs(differences[-1] - differences[0]) <0.15 :
            print("단순 이동 인것 같습니다.")
            cut_1_disolve_2_move_3_still_4 = 3

        else:
            cut_1_disolve_2_move_3_still_4 = 2
            print("추가제안버전이 필요해 제작합니다.")
            base_name = os.path.basename(video_path)
            name, ext = os.path.splitext(base_name)
            new_file_name = '_(_추가제안버전_)_' + name + ext
            new_file_path_in_ip_folder = os.path.join(net_ip_folder_path, new_file_name)
            try:
                shutil.copy(video_path, new_file_path_in_ip_folder)
            except:
                pass

    #######################################################################################
    ## 디졸브로 인한 추가 버전이라면 여기서 마무리 하고 export 하면 된다 ###

    if '_(_추가제안버전_)_' in file_name or cut_1_disolve_2_move_3_still_4 == 1 :
        print("디졸브 값 1 or 추가 제안 버전 입니다. (단순 컷변화)")
        cap = cv2.VideoCapture(video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, first_non_black_frame_cnt)
        ret, frame = cap.read()
        cap.release()

        last_still_frame_cnt = first_non_black_frame_cnt ## 여기 -1이 맞나..
        still_frame = frame

        # print(f"상관관계가 99.98% 이하인 첫 번째 프레임을 찾아 still을 만들 프레임 번호 : {last_still_frame_cnt}")
        # cv2.namedWindow("vewing las frame", cv2.WINDOW_NORMAL)  # 조절 가능한 창 생성
        # cv2.resizeWindow("vewing las frame", 320, 240)  # 창 크기를 640x480으로 조절
        # cv2.moveWindow("vewing las frame", 100, 100)
        # cv2.imshow("vewing las frame", still_frame)  # 조절된 크기의 창에 이미지 표시
        # cv2.waitKey(2000)  # 5초(5000 밀리초) 동안 대기
        # cv2.destroyAllWindows()  # 창 닫기

        if  end_time_of_audio >= (last_still_frame_cnt * fps):
            print("오디오가 더 길어 조정합니다.")
            selected_still_time = int(selected_still_time) + int(end_time_of_audio-(last_still_frame_cnt * fps) +2)
        elif (last_still_frame_cnt * fps) - end_time_of_audio < 2:
            selected_still_time = int(selected_still_time)+2

        if '_(_추가제안버전_)_' in file_name:
            print("추가 제안버전은 길이를 조절 합니다..")
            selected_still_time =  int(1)
        elif (last_still_frame_cnt * fps) - end_time_of_audio < 2:
            selected_still_time = int(2)

        create_video_with_still_frames(video_path, fps, output_folder_path, start_frame_num, first_non_black_frame_cnt,
                                       still_frame, ffmpeg_path, selected_resolution, selected_channel,
                                       selected_still_time)
        return  start_frame_time , float(first_non_black_frame_cnt/fps)

    ################################################################# 중간 step 끝#######################
    #### cut이나 still이나 차이가 없는거 같기도 해서 그냥 해본다 일단.
    if cut_1_disolve_2_move_3_still_4 == 3 or cut_1_disolve_2_move_3_still_4 == 4:
        print(" 값 3 or 4 (단순 이동 및 스틸)" )
        cnt = 0
        while True:
            cap = cv2.VideoCapture(video_path)
            cap.set(cv2.CAP_PROP_POS_FRAMES, first_non_black_frame_cnt-cnt)
            ret, frame = cap.read()
            cap.release()


            cap = cv2.VideoCapture(video_path)
            cap.set(cv2.CAP_PROP_POS_FRAMES, first_non_black_frame_cnt-cnt-1)
            fps = cap.get(cv2.CAP_PROP_FPS)
            ret, prev_frame = cap.read()
            cap.release()

            fps = int(fps)
            if fps == 29:
                fps = 30000 / 1001
            elif fps == 59:
                fps = 60000 / 1001


            result = compare_frames(frame, prev_frame)
            seperate_change = result[0]
            seperate_change_cnt = result[1]

            print(f"조각의 개수 : {seperate_change_cnt}")
            if seperate_change:
                i_want_know_still = 1
                target_frame_num = first_non_black_frame_cnt - cnt
                #target_frame_num=first_non_black_frame_cnt - cnt-1
                still_frame = frame
                break
            cnt += 1


        if  end_time_of_audio >= (target_frame_num * fps):
            print("오디오가 더 길어 조정합니다.")
            selected_still_time = int(selected_still_time) + int(end_time_of_audio-(target_frame_num * fps) +2)
        elif (target_frame_num * fps) - end_time_of_audio < 3:
            selected_still_time = int(selected_still_time)+3


        create_video_with_still_frames(video_path, fps, output_folder_path, start_frame_num, target_frame_num,
                                       still_frame, ffmpeg_path, selected_resolution, selected_channel,
                                       selected_still_time)
        return  start_frame_time , float(first_non_black_frame_cnt/fps)

    if cut_1_disolve_2_move_3_still_4 == 2:
        print("디졸브 값 2")
        threshold = (average_adjacent_differences)/5
        ### 확실한 1초간의 디졸브의 프레임간 밝기변화보다 더 작은 변화를 찾는다.
        cnt = 0
        state = 0
        while True:
            cap = cv2.VideoCapture(video_path)
            cap.set(cv2.CAP_PROP_POS_FRAMES, first_non_black_frame_cnt - cnt)
            ret, frame = cap.read()
            cap.release()

            cap = cv2.VideoCapture(video_path)
            cap.set(cv2.CAP_PROP_POS_FRAMES, first_non_black_frame_cnt - cnt -1)
            ret, prev_frame = cap.read()
            cap.release()

            if ret:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 그레이스케일로 변환
                brightness = gray_frame.mean()  # 밝기 값 계산

                gray_prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)  # 그레이스케일로 변환
                prev_brightness = gray_prev_frame.mean()  # 밝기 값 계산

                result = abs(prev_brightness -brightness)


            else:
                state = 1
                break

            if result < threshold:
                maybe_finish_disolve_frame = first_non_black_frame_cnt - cnt
                break
            cnt +=1

        if state == 1:
            raise

        cnt = 0
        while True:
            cap = cv2.VideoCapture(video_path)
            cap.set(cv2.CAP_PROP_POS_FRAMES, maybe_finish_disolve_frame - cnt)
            ret, frame = cap.read()
            cap.release()

            cap = cv2.VideoCapture(video_path)
            cap.set(cv2.CAP_PROP_POS_FRAMES, maybe_finish_disolve_frame - cnt -1)
            ret, prev_frame = cap.read()
            cap.release()

            result = compare_frames(frame, prev_frame)
            seperate_change = result[0]
            seperate_change_cnt = result[1]

            print(f"조각의 개수 : {seperate_change_cnt}")
            if seperate_change:
                i_want_know_still = 1
                target_frame_num=maybe_finish_disolve_frame - cnt
                still_frame = frame
                break
            cnt += 1

        create_video_with_still_frames(video_path, fps, output_folder_path, start_frame_num, target_frame_num,
                                       still_frame, ffmpeg_path, selected_resolution, selected_channel,
                                       selected_still_time)
        return  start_frame_time , float(first_non_black_frame_cnt/fps)

#######################  오디오 관련 모듈


def adjust_audio_volume(input_path, output_path, volume_change):
    # 오디오 파일 로드
    audio = AudioSegment.from_file(input_path)

    # 볼륨 조절 (volume_change는 변화량, 음수 값은 감소, 양수 값은 증가)
    adjusted_audio = audio + volume_change

    # 조절된 오디오 저장
    adjusted_audio.export(output_path, format="wav")


def compute_audio_similarity(audio_path_1, audio_path_2, threshold, silence_threshold=0.002):
    y1, sr1 = librosa.load(audio_path_1, sr=None)
    y2, sr2 = librosa.load(audio_path_2, sr=None)

    # 길이 맞추기
    if len(y1) > len(y2):
        y2 = np.pad(y2, (0, len(y1) - len(y2)))
    else:
        y1 = np.pad(y1, (0, len(y2) - len(y1)))

    # 크로스 코릴레이션 계산
    correlation = np.correlate(y1, y2, mode='valid')
    norm1 = np.linalg.norm(y1)
    norm2 = np.linalg.norm(y2)
    max_correlation = max(correlation) / (norm1 * norm2)

    print(f" 상관 : {max_correlation}")

    if max_correlation < 0.5:
        return None # 유사도가 낮음
    ### 0.8 이하의 유사도의 경우 완전 다른 소리로 보자
    else:
        return max_correlation


def rename_based_on_similarity(audio_temp_path, ffmpeg_path, threshold):
    audio_files = [f for f in os.listdir(audio_temp_path) if f.endswith('.wav')]
    channel_counter = 1
    try:
        for i in range(len(audio_files)):
            audio_file = audio_files[0]
            most_similar_file = None
            highest_similarity = 0
            if audio_file == "":
                print("검출 끝")
                continue

            for compare_audio_file in (audio_files):
                try:
                    if audio_file != compare_audio_file:

                        time.sleep(1)
                        audio_path_1 = os.path.join(audio_temp_path, audio_file)

                        audio_path_2 = os.path.join(audio_temp_path, compare_audio_file)


                        similarity = compute_audio_similarity(audio_path_1, audio_path_2, threshold=0.8,
                                                              silence_threshold=0.002)
                        time.sleep(1)
                        print(f"유사도는 {similarity}")
                        # if np.any(similarity > threshold) and np.any(similarity > highest_similarity):
                        if np.any(similarity > highest_similarity):
                            highest_similarity = similarity
                            most_similar_file = compare_audio_file
                            print(f"{audio_file}은 {most_similar_file}가장 유사 파일")
                        # if np.any(similarity > threshold)
                        #     top_similarity = similarity
                except:
                    pass


            # 루프 리스트에서 제거
            audio_files.remove(audio_file)

            if highest_similarity == 0 or highest_similarity >= 0.99:

                way = os.path.join(audio_temp_path, f"copy_{audio_file}")

                adjust_audio_volume(os.path.join(audio_temp_path, audio_file), way, -6)

                way2 = os.path.join(audio_temp_path, f"copy2_{audio_file}")

                shutil.copy(way, way2)

                os.remove(os.path.join(audio_temp_path, audio_file))

                os.rename(way, os.path.join(audio_temp_path, f"{channel_counter}ch.wav"))
                os.rename(way2, os.path.join(audio_temp_path, f"{channel_counter + 1}ch.wav"))

                channel_counter += 2

            else:

                print(f"{audio_file}이름바꾸기 시도")
                os.rename(
                    os.path.join(audio_temp_path, audio_file),
                    os.path.join(audio_temp_path, f"{channel_counter}ch.wav")
                )

                print(f"{most_similar_file} 이름바꾸기 시도 ")
                os.rename(
                    os.path.join(audio_temp_path, most_similar_file),
                    os.path.join(audio_temp_path, f"{channel_counter + 1}ch.wav")
                )
                channel_counter += 2

    except:
        pass

    def get_max_db(wav_file_path):
        # wav 파일에서 샘플레이트와 데이터 읽기
        rate, data = wavfile.read(wav_file_path)

        # .wav 파일의 데이터는 다양한 데이터 타입(int16, int32, float32 등)으로 반환될 수 있습니다.
        # float 형식으로 변환하여 계산을 쉽게 만듭니다.
        if data.dtype == np.int16:
            data = data / 32768.0
        elif data.dtype == np.int32:
            data = data / 2147483648.0

        # 최대 dB 계산
        max_db = 20 * np.log10(np.max(np.abs(data)))

        return max_db

    def get_db_value(wav_count):
        if wav_count == 2:
            return 0
        elif wav_count == 4:
            return -6
        elif wav_count == 6:
            return -9
        elif wav_count == 8:
            return -12
        else:
            return -15

    wav_files = [f for f in os.listdir(audio_temp_path) if
                 os.path.isfile(os.path.join(audio_temp_path, f)) and f.endswith('.wav')]
    wav_count = len(wav_files)

    # 대응하는 dB 값을 가져오기
    db_value = get_db_value(wav_count)
    print(f"Number of WAV files: {wav_count}")
    print(f"Corresponding dB value: {db_value}")
    time.sleep(1)
    # 각 .wav 파일의 dB 조절
    for wav_file in wav_files:
        wav_file_temp = "wav_temp.wav"
        input_path = os.path.join(audio_temp_path, wav_file)
        # 출력 파일은 원본 파일과 동일한 이름을 사용하므로 원본 파일을 덮어씁니다.
        output_path = os.path.join(audio_temp_path, wav_file_temp)

        max_vol = get_max_db(input_path)
        print(f"max vol은 {max_vol}")
        adjust_db = -15.0 - int(max_vol)
        adjust_db_str = str(int(adjust_db))

        # ffmpeg 명령 실행 시 콘솔 창이 뜨지 않도록 설정
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # FFmpeg를 사용하여 오디오 볼륨 조절
        cmd = [ffmpeg_path, '-i', input_path, '-map', f'0:a:0', '-af', f'volume={adjust_db_str}dB', output_path]
        subprocess.run(cmd, startupinfo=startupinfo)
        os.remove(input_path)
        time.sleep(1)
        os.rename(output_path, input_path)
        time.sleep(1)





def combine_audio_and_video(video_temp_folder_path, audio_temp_path, finish_folder_in_local_making_file_folder,net_ip_file_path, ffmpeg_path, selected_resolution,selected_channel):
    # video_temp 폴더에서 동영상 파일 찾기

    video_files = [f for f in os.listdir(video_temp_folder_path) if
                   f.endswith(('.mp4', '.mov', '.mxf', '.MP4', '.MOV', '.MXF'))]
    if not video_files:
        print("No video files found in video_temp directory!")
        return
    video_path = os.path.join(video_temp_folder_path, video_files[0])  # 첫 번째 동영상 파일 사용

    ####################################

    files = [f for f in os.listdir(audio_temp_path) if os.path.isfile(os.path.join(audio_temp_path, f))]
    ####################### 테스팅
    # 각 파일을 순회하며 채널 확인 및 변환
    for file in files:
        file_path = os.path.join(audio_temp_path, file)
        audio = AudioSegment.from_file(file_path)

        if audio.channels == 2:  # 2채널(스테레오) 확인
            mono_audio = audio.set_channels(1)  # 1채널(모노)로 변환

            # 볼륨을 -6dB 조정
            adjusted_mono_audio = mono_audio - 6

            # 조정된 오디오 저장
            adjusted_mono_audio.export(file_path, format="wav")  # 원본 파일을 덮어쓰기
            print(f"{file} was converted to mono and volume reduced by 6dB.")
        else:
            print(f"{file} is already mono.")

    ################ 테스팅
    # 홀수 및 짝수 ch 파일 정렬
    odd_files = sorted([f for f in files if 'ch' in f and int(f.split('ch')[0]) % 2 == 1])
    even_files = sorted([f for f in files if 'ch' in f and int(f.split('ch')[0]) % 2 == 0])

    # 2. 홀수와 짝수 ch를 분리하여 오디오 믹싱을 실시한다.
    if len(odd_files) == 1:
        os.rename(os.path.join(audio_temp_path, "1ch.wav"), os.path.join(audio_temp_path, "temp_R.wav")) ## LR변화
        os.rename(os.path.join(audio_temp_path, "2ch.wav"), os.path.join(audio_temp_path, "temp_L.wav"))
    else:
        # cmd 창을 숨기기 위한 설정
        # startupinfo = subprocess.STARTUPINFO()
        # startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        #
        # # odd_files 합치기
        # inputs_odd = ' '.join(['-i "' + os.path.join(audio_temp_path, f) + '"' for f in odd_files])
        # filter_complex_odd = f'amix=inputs={len(odd_files)}:duration=first:dropout_transition=2,loudnorm=I=-24'
        # cmd_odd = f'{ffmpeg_path} {inputs_odd} -filter_complex "{filter_complex_odd}" -acodec pcm_s16le "{os.path.join(audio_temp_path, "temp_L.wav")}"'
        #
        # subprocess.run(cmd_odd, shell=True, startupinfo=startupinfo)
        #
        #
        # # even_files 합치기
        # inputs_even = ' '.join(['-i "' + os.path.join(audio_temp_path, f) + '"' for f in even_files])
        # filter_complex_even = f'amix=inputs={len(even_files)}:duration=first:dropout_transition=2,loudnorm=I=-24'
        # cmd_even = f'{ffmpeg_path} {inputs_even} -filter_complex "{filter_complex_even}" -acodec pcm_s16le "{os.path.join(audio_temp_path, "temp_R.wav")}"'
        #
        # subprocess.run(cmd_even, shell=True, startupinfo=startupinfo)
        odd_files = sorted([f for f in files if 'ch' in f and int(f.split('ch')[0]) % 2 == 1])

        # 첫 번째 파일로 시작하여 나머지 파일을 믹싱
        mixed_audio = AudioSegment.from_file(os.path.join(audio_temp_path, odd_files[0]))
        for file in odd_files[1:]:
            next_audio = AudioSegment.from_file(os.path.join(audio_temp_path, file))
            mixed_audio = mixed_audio.overlay(next_audio)


        # # (선택적) 볼륨 조절 - 여기서는 볼륨을 -20dB로 조절합니다.
        # mixed_audio = mixed_audio - 15

        # 믹싱된 오디오 저장
        mixed_audio.export(os.path.join(audio_temp_path, "temp_L.wav"), format="wav")

        even_files = sorted([f for f in files if 'ch' in f and int(f.split('ch')[0]) % 2 == 0])

        # 첫 번째 파일로 시작하여 나머지 파일을 믹싱
        mixed_audio = AudioSegment.from_file(os.path.join(audio_temp_path, even_files[0]))
        for file in even_files[1:]:
            next_audio = AudioSegment.from_file(os.path.join(audio_temp_path, file))
            mixed_audio = mixed_audio.overlay(next_audio)


        # 믹싱된 오디오 저장
        mixed_audio.export(os.path.join(audio_temp_path, "temp_R.wav"), format="wav")

    # 6. ch이 붙은 모든 파일을 지운다.
    try:
        for f in odd_files:
            os.remove(os.path.join(audio_temp_path, f))
    except:
        pass
    try:
        for f in even_files:
            os.remove(os.path.join(audio_temp_path, f))
    except:
        pass


    if selected_channel == "8ch" or selected_channel == "8CH":
        print("오디오는 8채널로 진행 합니다.")
        # 7. temp_L 복사 및 이름 변경
        ##############################################################################
        time.sleep(1)
        for i, name in enumerate(["1ch", "3ch", "5ch", "7ch"]):
            # 예제: temp_L.wav 파일을 name.wav로 복사
            shutil.copy(os.path.join(audio_temp_path, 'temp_L.wav'), os.path.join(audio_temp_path, f"{name}.wav"))
            print("홀수채널 생성완료")

        # 8. temp_R 복사 및 이름 변경
        for i, name in enumerate(["2ch", "4ch", "6ch", "8ch"]):
            # 예제: temp_L.wav 파일을 name.wav로 복사
            shutil.copy(os.path.join(audio_temp_path, 'temp_R.wav'), os.path.join(audio_temp_path, f"{name}.wav"))
            print("짝수채널 생성완료")
        time.sleep(1)
        try:
            os.remove(os.path.join(audio_temp_path, 'temp_L.wav'))
            os.remove(os.path.join(audio_temp_path, 'temp_R.wav'))
        except:
            pass
    ########################### 아래로 대체 창원처럼 8ch 쓰고 싶으면 뒤에것을 살려서 하면 됨
    else:
        print("오디오는 2ch로 진행 합니다.")
        for i, name in enumerate(["1ch"]):
            # 예제: temp_L.wav 파일을 name.wav로 복사
            shutil.copy(os.path.join(audio_temp_path, 'temp_L.wav'), os.path.join(audio_temp_path, f"{name}.wav"))
            print("홀수채널 생성완료")

        # 8. temp_R 복사 및 이름 변경
        for i, name in enumerate(["2ch"]):
            # 예제: temp_L.wav 파일을 name.wav로 복사
            shutil.copy(os.path.join(audio_temp_path, 'temp_R.wav'), os.path.join(audio_temp_path, f"{name}.wav"))
            print("짝수채널 생성완료")
        time.sleep(1)
        try:
            os.remove(os.path.join(audio_temp_path, 'temp_L.wav'))
            os.remove(os.path.join(audio_temp_path, 'temp_R.wav'))
        except:
            pass
    ###################################
    # 파일이 존재하는지 확인하고, 존재한다면 접미사 추가

    # audio_temp 폴더에서 오디오 파일 모두 찾기
    audio_files = [os.path.join(audio_temp_path, f) for f in os.listdir(audio_temp_path) if f.endswith('.wav')]
    # FFmpeg 명령 생성
    audio_inputs = ' '.join([f'-i "{audio_file}"' for audio_file in audio_files])
    print(len(audio_files))

    audio_maps = ' '.join([f"-map 0:v:0"] + [f"-map {i + 1}:a:0" for i in range(len(audio_files))])

    video_path = os.path.normpath(video_path)
    net_ip_file_path = os.path.basename(net_ip_file_path)
    net_ip_file_path = os.path.splitext(net_ip_file_path)[0] + '.mov'
    output_video_path = os.path.join(finish_folder_in_local_making_file_folder,net_ip_file_path)

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    cmd = f'"{ffmpeg_path}" -i "{video_path}" {audio_inputs} -c:v prores_ks -profile:v 3 -c:a pcm_s16le -map 0:v:0 {audio_maps} "{output_video_path}"'

    # 세부 설정
    # -profile:v 0: ProRes 422 Proxy
    # -profile:v 1: ProRes 422 LT
    # -profile:v 2: ProRes 422 Standard
    # -profile:v 3: ProRes 422 HQ
    # -profile:v 4: ProRes 4444 (no alpha)
    # -profile:v 5: ProRes 4444 XQ (no alpha)

    process = subprocess.Popen(cmd, startupinfo=startupinfo, shell=True)
    ffmpeg_pid = process.pid
    # ... 필요한 작업 ...

    process.wait()

    # 작업이 끝난 후 ffmpeg가 여전히 실행 중인지 확인
    if psutil.pid_exists(ffmpeg_pid):
        print("ffmpeg가 여전히 실행 중. 강제 종료합니다.")

    time.sleep(1)
    return output_video_path



def find_files(base_path, target_files):
    found_files = {}

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file in target_files:
                found_files[file] = os.path.join(root, file)

    return found_files


def is_silent_audio(audio_path):
    try:
        with wave.open(audio_path, 'rb') as wav_file:
            # WAV 파일의 샘플 너비를 가져옴 (바이트 단위)
            sample_width = wav_file.getsampwidth()

            # WAV 파일의 모든 오디오 샘플을 읽음
            audio_data = wav_file.readframes(-1)

            # 오디오 데이터를 바이너리로 변환
            audio_data = bytearray(audio_data)

            # 모든 오디오 샘플이 0인지 확인
            return all(sample_width * i == 0 for i in audio_data)
    except Exception as e:
        print(f"오류 발생: {e}")
        return False


def extract_and_split_audio_channels_with_ffmpeg(ffmpeg_path,video_path, output_folder,start_frame_time,global_check_duration):
    # 오디오 트랙과 채널 정보를 확인

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    cmd = [ffmpeg_path, '-i', video_path, '-hide_banner']

    # FFmpeg 명령 실행
    process = subprocess.Popen(cmd,startupinfo=startupinfo, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, errors='replace')
    ffmpeg_pid = process.pid
    process.wait()
    # 작업이 끝난 후 ffmpeg가 여전히 실행 중인지 확인
    if psutil.pid_exists(ffmpeg_pid):
        print("ffmpeg가 여전히 실행 중. 강제 종료합니다.")
        psutil.Process(ffmpeg_pid).terminate()
    # FFmpeg 실행 결과 확인
    stdout, stderr = process.communicate()

    # "Audio:"를 포함하는 행 찾기
    audio_tracks = [line for line in stderr.splitlines() if "Audio:" in line]

    print("오디오 시작")
    # 각 오디오 트랙을 순회
    # 확장자 추출
    extension = os.path.splitext(video_path)[1]

    # 확장자가 .mp4 ,.mov의 경우
    if extension.lower() == '.MP4' or extension.lower() == '.mp4' or extension.lower() == '.MOV' or extension.lower() == '.mov':

        for i, track in enumerate(audio_tracks):
            if "stereo" in track:
                num_channels = 2
                print("스테레오입니다.")
            else:
                num_channels = 1# 간단하게 채널 수 파악
            base_output_name = os.path.join(output_folder, f"track_{i + 1}")

            # 채널이 1개인 경우
            if num_channels == 1:
                print(f"START_FRAME_TIME은 {start_frame_time} 채널 1")
                output_file = f"{base_output_name}.wav"
                # cmd = [ffmpeg_path, '-i', video_path, '-map', f'0:a:{i}', output_file]

                cmd = [
                    str(ffmpeg_path),
                    '-i', str(video_path),
                    '-ss', str(start_frame_time),
                    '-t', str(global_check_duration),
                    '-map', f'0:a:{i}',
                    '-af', 'asetpts=PTS-STARTPTS,volume=-15dB',
                    str(output_file)
                ]

                process = subprocess.Popen(cmd, startupinfo=startupinfo)
                ffmpeg_pid = process.pid
                process.wait()
                # 작업이 끝난 후 ffmpeg가 여전히 실행 중인지 확인
                if psutil.pid_exists(ffmpeg_pid):
                    print("ffmpeg가 여전히 실행 중. 강제 종료합니다.")
                    psutil.Process(ffmpeg_pid).terminate()

                # 오디오 파일이 무음인 경우 삭제
                if is_silent_audio(output_file):
                    print(f"트랙 {i + 1}의 오디오가 무음입니다. 파일을 삭제합니다.")
                    os.remove(output_file)

            # 채널이 2개인 경우
            elif num_channels == 2:
                # 왼쪽 채널 추출
                print(f"START_FRAME_TIME은 {start_frame_time} 채널 2")
                output_file_left = f"{base_output_name}_L.wav"
                cmd_left = [
                    str(ffmpeg_path),
                    '-i', video_path,
                    '-ss', str(start_frame_time),
                    '-t', str(global_check_duration),
                    '-map', f'0:a:{i}',
                    '-af', 'asetpts=PTS-STARTPTS, volume=-15dB, pan=mono|c0=c1', ## 왼쪽은 c1 오른쪽은 c0
                    '-ac', '1',
                    str(output_file_left)
                ]

                process = subprocess.Popen(cmd_left, startupinfo=startupinfo)
                ffmpeg_pid = process.pid
                process.wait()
                # 작업이 끝난 후 ffmpeg가 여전히 실행 중인지 확인
                if psutil.pid_exists(ffmpeg_pid):
                    print("ffmpeg가 여전히 실행 중. 강제 종료합니다.")
                    psutil.Process(ffmpeg_pid).terminate()

                # 오디오 파일이 무음인 경우 삭제
                if is_silent_audio(output_file_left):
                    print(f"트랙 {i + 1}의 왼쪽 채널 오디오가 무음입니다. 파일을 삭제합니다.")
                    os.remove(output_file_left)

                # 오른쪽 채널 추출
                output_file_right = f"{base_output_name}_R.wav"
                cmd_right = [
                    str(ffmpeg_path),
                    '-i', str(video_path),
                    '-ss', str(start_frame_time),
                    '-t', str(global_check_duration),
                    '-map', f'0:a:{i}',
                    '-af', 'asetpts=PTS-STARTPTS, volume=-15dB, pan=mono|c0=c0',
                    '-ac', '1',
                    str(output_file_right)
                ]
                process = subprocess.Popen(cmd_right, startupinfo=startupinfo)
                ffmpeg_pid = process.pid
                process.wait()
                # 작업이 끝난 후 ffmpeg가 여전히 실행 중인지 확인
                if psutil.pid_exists(ffmpeg_pid):
                    print("ffmpeg가 여전히 실행 중. 강제 종료합니다.")
                    psutil.Process(ffmpeg_pid).terminate()
                # 오디오 파일이 무음인 경우 삭제
                if is_silent_audio(output_file_left):
                    print(f"트랙 {i + 1}의 왼쪽 채널 오디오가 무음입니다. 파일을 삭제합니다.")
                    os.remove(output_file_left)
                # 오디오 파일이 무음인 경우 삭제
                if is_silent_audio(output_file_right):
                    print(f"트랙 {i + 1}의 오른쪽 채널 오디오가 무음입니다. 파일을 삭제합니다.")
                    os.remove(output_file_right)

        time.sleep(1)
    else:  # xmf의 경우
        # 각 오디오 트랙을 순회
        for i, track in enumerate(audio_tracks):

            if "stereo" in track:
                num_channels = 2
            else:
                num_channels = 1  # 간단하게 채널 수 파악

            base_output_name = os.path.join(output_folder, f"track_{i + 1}")


            # 채널이 1개인 경우
            if num_channels == 1:
                output_file = f"{base_output_name}.wav"
                # cmd = [ffmpeg_path, '-i', video_path, '-map', f'0:a:{i}', output_file]
                cmd = [
                    str(ffmpeg_path),
                    '-i', str(video_path),
                    '-ss', str(start_frame_time),
                    '-t', str(global_check_duration),
                    '-map', f'0:a:{i}',
                    '-af', 'asetpts=PTS-STARTPTS',
                    '-filter:a', 'volume=-15dB',
                    '-ar', '48000',  # 샘플 레이트를 48000Hz로 설정
                    '-acodec', 'pcm_s16le',
                    '-f', 'wav',
                    str(output_file)
                ]

                process = subprocess.Popen(cmd, startupinfo=startupinfo)
                ffmpeg_pid = process.pid
                process.wait()
                # 작업이 끝난 후 ffmpeg가 여전히 실행 중인지 확인
                if psutil.pid_exists(ffmpeg_pid):
                    print("ffmpeg가 여전히 실행 중. 강제 종료합니다.")
                    psutil.Process(ffmpeg_pid).terminate()

                # 오디오 파일이 무음인 경우 삭제
                if is_silent_audio(output_file):
                    print(f"트랙 {i + 1}의 오디오가 무음입니다. 파일을 삭제합니다.")
                    os.remove(output_file)

            # 채널이 2개인 경우
            elif num_channels == 2:
                # 왼쪽 채널 추출
                output_file_left = f"{base_output_name}_L.wav"
                cmd_left = [
                    str(ffmpeg_path),
                    '-i', str(video_path),
                    '-ss', str(start_frame_time),
                    '-t', str(global_check_duration),
                    '-map', f'0:a:{i}',
                    '-af', 'asetpts=PTS-STARTPTS, volume=-15dB, pan=mono|c0=c1',
                    '-ar', '48000',
                    '-acodec', 'pcm_s16le',
                    '-f', 'wav',  # 명시적으로 WAV 형식을 지정
                    str(output_file_left)
                ]

                process = subprocess.Popen(cmd_left, startupinfo=startupinfo)
                ffmpeg_pid = process.pid
                process.wait()
                # 작업이 끝난 후 ffmpeg가 여전히 실행 중인지 확인
                if psutil.pid_exists(ffmpeg_pid):
                    print("ffmpeg가 여전히 실행 중. 강제 종료합니다.")
                    psutil.Process(ffmpeg_pid).terminate()

                # 오디오 파일이 무음인 경우 삭제
                if is_silent_audio(output_file_left):
                    print(f"트랙 {i + 1}의 왼쪽 채널 오디오가 무음입니다. 파일을 삭제합니다.")
                    os.remove(output_file_left)

                # 오른쪽 채널 추출
                output_file_right = f"{base_output_name}_R.wav"
                cmd_right = [
                    str(ffmpeg_path),
                    '-i', str(video_path),
                    '-ss', str(start_frame_time),
                    '-t', str(global_check_duration),
                    '-map', f'0:a:{i}',
                    '-af', 'asetpts=PTS-STARTPTS, volume=-15dB, pan=mono|c0=c0',
                    '-ar', '48000',
                    '-acodec', 'pcm_s16le',
                    '-f', 'wav',  # 명시적으로 WAV 형식을 지정
                    str(output_file_right)
                ]
                process = subprocess.Popen(cmd_right, startupinfo=startupinfo)
                ffmpeg_pid = process.pid
                process.wait()
                # 작업이 끝난 후 ffmpeg가 여전히 실행 중인지 확인
                if psutil.pid_exists(ffmpeg_pid):
                    print("ffmpeg가 여전히 실행 중. 강제 종료합니다.")
                    psutil.Process(ffmpeg_pid).terminate()
                # 오디오 파일이 무음인 경우 삭제
                if is_silent_audio(output_file_left):
                    print(f"트랙 {i + 1}의 왼쪽 채널 오디오가 무음입니다. 파일을 삭제합니다.")
                    os.remove(output_file_left)
                # 오디오 파일이 무음인 경우 삭제
                if is_silent_audio(output_file_right):
                    print(f"트랙 {i + 1}의 오른쪽 채널 오디오가 무음입니다. 파일을 삭제합니다.")
                    os.remove(output_file_right)

        time.sleep(1)