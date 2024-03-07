
import os
import sys

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


def find_ffprobe_path():
    # 현재 Python 실행 파일의 경로를 가져옵니다.
    executable_path = sys.executable

    # Python 실행 파일의 기본 디렉토리를 구합니다.
    base_path = os.path.dirname(executable_path)

    # 다양한 운영 체제에 대한 대상 파일들을 정의합니다.
    target_files = ['ffprobe', 'ffprobe.exe']

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
    ffprobe_path = found.get('ffprobe', found.get('ffprobe.exe', None))

    return ffprobe_path

def find_ffplay_path():
    # 현재 Python 실행 파일의 경로를 가져옵니다.
    executable_path = sys.executable

    # Python 실행 파일의 기본 디렉토리를 구합니다.
    base_path = os.path.dirname(executable_path)

    # 다양한 운영 체제에 대한 대상 파일들을 정의합니다.
    target_files = ['ffplay', 'ffplay.exe']

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
    ffplay_path = found.get('ffplay', found.get('ffplay.exe', None))

    return ffplay_path


def find_preset_epr_path(name_of_epr):
    # 현재 Python 실행 파일의 경로를 가져옵니다.
    executable_path = sys.executable

    # Python 실행 파일의 기본 디렉토리를 구합니다.
    base_path = os.path.dirname(executable_path)

    # 다양한 운영 체제에 대한 대상 파일들을 정의합니다.
    target_files = [name_of_epr]

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
    epr_path = found.get(name_of_epr, None)

    return epr_path
