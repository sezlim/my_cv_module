# -*- coding: utf-8 -*-
import os
import shutil
import time
from pymediainfo import MediaInfo
import platform

def detect_folder_and_move_file(working_folder, move_folder, target_extensions=['mxf']):
    
# 사용 예: detect_folder_and_move_file("작업_폴더_경로", "이동_폴더_경로") - 아무 확장자도 넣지 않으면 mxf 만 타겟으로 실행 
# 또는 detect_folder_and_move_file("작업_폴더_경로", "이동_폴더_경로", ['mov', 'mp4']) - 확장자 명시도 가능 

    def lock_file(f):
        if platform.system() == 'Windows':
            import msvcrt
            msvcrt.locking(f.fileno(), msvcrt.LK_LOCK, os.path.getsize(f.name))
        else:
            import fcntl
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)

    def unlock_file(f):
        if platform.system() == 'Windows':
            import msvcrt
            msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, os.path.getsize(f.name))
        else:
            import fcntl
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    def check_file_stability(file_path, duration=23):
        initial_size = os.path.getsize(file_path)
        initial_mtime = os.path.getmtime(file_path)

        for _ in range(3):
            print("체크중")
            time.sleep(duration)
            current_size = os.path.getsize(file_path)
            current_mtime = os.path.getmtime(file_path)

            if current_size == initial_size and current_mtime == initial_mtime:
                # 크기와 수정 시간이 모두 일치할 경우에만 계속 진행
                continue
            else:
                # 크기 또는 수정 시간 중 하나라도 일치하지 않으면 False 반환
                return False

        # 세 번 모두 크기와 수정 시간이 일치하면 True 반환
        return True

    for file in os.listdir(working_folder):
        file_path = os.path.join(working_folder, file)

        if any(file.lower().endswith(ext) for ext in target_extensions) and os.path.isfile(file_path):
            try:
                media_info = MediaInfo.parse(file_path)

                if media_info.tracks[0].duration is not None:
                    if check_file_stability(file_path):
                        with open(file_path, 'r+b') as f:
                            try:
                                lock_file(f)
                                os.utime(file_path, None) # 파일의 수정시간 변경
                                shutil.move(file_path, os.path.join(move_folder, file))
                            finally:
                                unlock_file(f)
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