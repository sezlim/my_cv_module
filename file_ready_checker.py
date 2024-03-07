# -*- coding: utf-8 -*-
import os
import shutil
import time
from pymediainfo import MediaInfo
import platform
import random
import sys
import socket


def move_file(file_path, move_folder):
    with open(file_path, 'r+') as lock:
        print(f"파일 {file_path} 잠금에 성공했습니다.")
        time.sleep(3)
        new_file_path = file_path

        if new_file_path:
            destination = os.path.join(move_folder, os.path.basename(new_file_path))
        else:
            # 파일 이동
            destination = os.path.join(move_folder, os.path.basename(file_path))

    shutil.move(file_path, destination)
    print(f"File moved to {destination}")


def check_file_stability(file_path, duration=23):

    initial_size = os.path.getsize(file_path)
    initial_mtime = os.path.getmtime(file_path)
    state = 0
    for _ in range(3):
        time.sleep(duration)
        current_size = os.path.getsize(file_path)
        current_mtime = os.path.getmtime(file_path)

        if current_size == initial_size and current_mtime == initial_mtime:
            # 크기와 수정 시간이 모두 일치할 경우에만 계속 진행
            continue
        else:
            # 크기 또는 수정 시간 중 하나라도 일치하지 않으면 False 반환
            state = 1
            break

    if state == 1:
        return False
    # 세 번 모두 크기와 수정 시간이 일치하면 True 반환
    else:
        return True
def detect_folder_and_move_file(working_folder, move_folder, target_extensions=['mxf']):
    
# 사용 예: detect_folder_and_move_file("작업_폴더_경로", "이동_폴더_경로") - 아무 확장자도 넣지 않으면 mxf 만 타겟으로 실행 
# 또는 detect_folder_and_move_file("작업_폴더_경로", "이동_폴더_경로", ['mov', 'mp4']) - 확장자 명시도 가능
    try:
        files = os.listdir(working_folder)

        # 파일 리스트를 무작위로 섞음
        random.shuffle(files)

        for file in files:

            file_path = os.path.join(working_folder, file)
            if not os.path.isfile(file_path):
                continue

            # 현재 Python 실행 파일의 경로를 가져옵니다.
            executable_path = sys.executable
            # Python 실행 파일의 기본 디렉토리를 구합니다.
            base_folder_path = os.path.dirname(executable_path)
            full_path = os.path.join(working_folder,file)
            def compare_file_size_with_folder_capacity(full_path, base_folder_path,mutilple):
                # 파일 크기 얻기
                file_size = os.path.getsize(full_path)

                # 폴더의 가용 용량 얻기
                total, used, free = shutil.disk_usage(base_folder_path)

                # 파일 크기와 폴더의 가용 용량 비교
                if file_size*mutilple <= free:
                    return True  # 파일을 폴더에 저장할 수 있는 충분한 공간이 있음
                else:
                    return False  # 폴더에 충분한 공간이 없음

            if compare_file_size_with_folder_capacity(full_path,base_folder_path,10) == False:
                print("로컬 pc의 용량이 모자라 작업을 할 수 없습니다. 따로 폴더로 빼 놓습니다.")


                def get_ip_address():
                    try:
                        # hostname을 얻습니다.
                        hostname = socket.gethostname()
                        # hostname에 해당하는 IP 주소를 얻습니다.
                        ip_address = socket.gethostbyname(hostname)
                        return ip_address
                    except socket.gaierror as e:
                        return "IP 주소를 얻을 수 없습니다."

                ip = get_ip_address()
                subfolder_name = f"경고!(pc의_용량이_모자랍니다)_{ip}"
                # 하위 폴더 이름 생성
                # 하위 폴더 경로 생성
                subfolder_path = os.path.join(working_folder, subfolder_name)

                # 하위 폴더 생성 (이미 존재하지 않는 경우)
                if not os.path.exists(subfolder_path):
                    os.makedirs(subfolder_path)
                    print(f"Folder '{subfolder_name}' created in {working_folder}")
                else:
                    print(f"Folder '{subfolder_name}' already exists.")

                continue
            else:
                def get_ip_address():
                    try:
                        # hostname을 얻습니다.
                        hostname = socket.gethostname()
                        # hostname에 해당하는 IP 주소를 얻습니다.
                        ip_address = socket.gethostbyname(hostname)
                        return ip_address
                    except socket.gaierror as e:
                        return "IP 주소를 얻을 수 없습니다."

                ip = get_ip_address()
                subfolder_name = f"경고!(pc의_용량이_모자랍니다)_{ip}"
                subfolder_path = os.path.join(working_folder, subfolder_name)
                try:
                    shutil.rmtree(subfolder_path)
                except:
                    pass

            file_path = os.path.join(working_folder, file)
            print(f"file_path는 :{file_path}")
        # for file in os.listdir(working_folder):
        #     file_path = os.path.join(working_folder, file)
            if any(file.lower().endswith(ext) for ext in target_extensions) and os.path.isfile(file_path):
                try:
                    media_info = MediaInfo.parse(file_path)

                    duration_info_state = 0
                    for track in media_info.tracks:
                        if track.track_type == 'Video':
                            duration = getattr(track, 'duration', None)
                            if duration is not None:  ## duration이라는  목록이 있으면 - => 전부 이동된 파일이면
                                break
                            else:  # 여기로 빠지는 것이 불완전 파일 잡았을 때
                                duration_info_state = 1
                                break
                    if duration_info_state == 1:
                        continue

                    if media_info.tracks[0].duration is not None:
                        print("스테빌리티 체크")
                        if check_file_stability(file_path):
                            os.utime(file_path, None) # 파일의 수정시간 변경
                            move_file(file_path, move_folder)
                            moved_file_path = os.path.join(move_folder,os.path.basename(file_path))
                            return moved_file_path

                except Exception as e:
                    print(f"Error processing file {file}: {e}")

        return False

    except Exception as e:
        print(f"Error processing file {file}: {e}")

# 사용 예: detect_folder_and_move_file("작업_폴더_경로", "이동_폴더_경로") - 아무 확장자도 넣지 않으면 mxf 만 타겟으로 실행 
# 또는 detect_folder_and_move_file"작업_폴더_경로", "이동_폴더_경로", ['mov', 'mp4']) - 확장자 명시도 가능 


# 디음 조건을 만족하면 working folder 에서 move_folder로 파일을 이동시킵니다.
# 1. mxf 파일일 것
# 2. media info 상에 duation 이 있을 것 (duartion이 없는 파일은 프리미어에서 아직 다 만들어지지 않은 파일 입니다.) 
# 3. 단독 점유가 가능할 것 
# 4. 23초 동안 3번 체크해서 파일크기가 더 이상 변하지 않고, 수정시간이 변하지 않아야 한다.
# <4> 네트워크 부하가 많을 시 파일 크기가 변하지 않는데 다 만들어지지 않은 경우가 있다. (순간적인 병목 현상), 이 떄도 수정시간은 "분" 단위로 변경됨으로 체크한다. 

# <추가>
# 1. 이동하기 전에 파일의 수정시간을 현재 시각으로 변경합니다.  <작업이 다 끝나고 파일을 주기적으로 지워주기 위한 근거 입니다.>
# 2. move_folder를 보고 파일의 수정시간이 2일 이상인 파일이 있다면 삭제합니다. 
 

# 사용 예시
# detect_folder_and_move_file(r'/Users/imsejin/Desktop/입', r'/Users/imsejin/Desktop/출')
# detect_folder_and_move_file(r'/Users/imsejin/Desktop/입', r'/Users/imsejin/Desktop/출',['mxf', 'mov', 'mp4'])


## 사용 주의 
## 마지막에 파일을 이동시키는 함수는 Move를 사용했습니다. 같은 스토리지나 드라이브 안에 있다면 상관이 없겠지만
## 다른 드라이브나 네트워크로 move 시키는 경우 복사로 실행되고 복사되는 시간이 있겠죠 ?? 그 사이에 작업하지 않도록 주의하거나 같은 드라이브에서 이동하여 사용하시면 됩니다.
## Q&A 32391 ##



import os

def how_many_files_in_folder(folder_path, extension_contain_dot=""):
    ## 폴더안에 특정 파일, 혹은 특정 확장자의 파일이 몇개인지 세는 함수
    ## 내가 원하는 파일의 개수가 0일때는 오래쉬었다가 작업해도 된다.

    file_count = 0

    # 폴더 내의 모든 파일과 서브 폴더를 반복
    for item in os.listdir(folder_path):
        # 완전한 파일 경로
        full_path = os.path.join(folder_path, item)

        # 파일인지 확인
        if os.path.isfile(full_path):
            # 확장자 확인
            if extension_contain_dot:
                if os.path.splitext(item)[1].lower() == extension_contain_dot.lower():
                    file_count += 1
            else:
                file_count += 1

    return file_count

# 함수 사용 예시
# folder_path = 'path/to/your/folder'  # 폴더 경로 지정
# print(how_many_files_in_folder(folder_path, ".mxf"))  # ".mxf" 확장자를 가진 파일의 개수
# print(how_many_files_in_folder(folder_path))  # 폴더 내의 모든 파일 개수
