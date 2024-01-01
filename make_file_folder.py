# -*- coding: utf-8 -*-

import os
import shutil

def make_folder(parent_folder, folder_name, clear=True):
    # 폴더 경로 생성
    folder_path = os.path.join(parent_folder, folder_name)

    # 폴더가 이미 존재하는 경우
    if os.path.exists(folder_path):
        if clear:
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


import os
import time
from datetime import datetime, timedelta

def old_file_delete(target_folder, days, create_time=False, child_folder=False):
    # 현재 시간에서 days만큼 이전의 시간을 계산
    cutoff_time = datetime.now() - timedelta(days=days)

    # 주어진 폴더를 순회
    for root, dirs, files in os.walk(target_folder):
        if not child_folder:
            # 하위 폴더의 파일은 무시
            dirs[:] = []
            # 이렇게 하면 For 문으로 돌아야 하는 dir 리스트를 다 지워서 자기 자신만 돌게 됨 즉 하위폴더는 검색 안함 
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # 파일의 생성 시간 또는 수정 시간을 가져옴
                if create_time:
                    file_time = datetime.fromtimestamp(os.path.getctime(file_path)) ## 생성일 기준 체크
                else:
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path)) ## 수정일 기준 체크 

                # 파일이 cutoff_time보다 오래되었으면 삭제
                if file_time < cutoff_time:
                    os.remove(file_path)
                    print(f"Deleted old file: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

# 사용 예: old_file_delete("/path/to/target", 30, create_time=True, child_folder=True)
# 사용 예: old_file_delete("/path/to/target", 30, Faslse, False) # 생성일이 아닌 수정일, 하위폴더 검색 안함 
# 뒤에 True False에 따른 옵션 설명
# True True   생성일 기준, 하위 폴더의 파일들 삭제 
# True False  생성일 기준, 하위 폴더의 파일들 유지 (타겟 폴더 안의 파일만 삭제)
# False True  수정일 기준, 하위 폴더의 파일들 삭제
# False False 수정일 기준, 하위 폴더의 파일들 유지 (타겟 폴더 안의 파일만 삭제)


def make_or_append_txt(file_path, word, append=True):
    try:
        if not append:
            # append가 False인 경우, 파일의 내용을 삭제하고 word를 쓰기 모드로 열어 씁니다.
            with open(file_path, 'w') as file:
                if isinstance(word, (str, int)):
                    # word가 문자열이나 숫자인 경우에만 처리
                    file.write(str(word) + '\n')
                    print(f"Written '{word}' to {file_path}")
                elif isinstance(word, list):
                    # word가 리스트인 경우 각 항목을 파일에 추가
                    for item in word:
                        file.write(str(item) + '\n')
                        print(f"Written '{item}' to {file_path}")
                else:
                    print("Unsupported data type. Only str, int, or list allowed.")
        else:
            # append가 True인 경우, 파일을 추가 모드로 열어서 word를 추가합니다.
            with open(file_path, 'a') as file:
                if isinstance(word, (str, int)):
                    # word가 문자열이나 숫자인 경우에만 처리
                    file.write(str(word) + '\n')
                    print(f"Appended '{word}' to {file_path}")
                elif isinstance(word, list):
                    # word가 리스트인 경우 각 항목을 파일에 추가
                    for item in word:
                        file.write(str(item) + '\n')
                        print(f"Appended '{item}' to {file_path}")
                else:
                    print("Unsupported data type. Only str, int, or list allowed.")
    except Exception as e:
        print(f"Error: {e}")



# 사용 예: make_or_append_txt("example.txt", "Hello")
# 사용 예: make_or_append_txt("example.txt", [1, 2, 3])
# 사용 예: make_or_append_txt("example.txt", 42, append=False)
# 사용 예 : make_or_append_txt(r'/Users/imsejin/Desktop/입/test.txt', "테스트",True)
# True의 경우 메모장에 마지막 줄에 추가, False의 경우 메모장 내용을 삭제하고 내용 추가 입니다.
