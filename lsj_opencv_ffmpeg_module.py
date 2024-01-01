"""
포함 되어 있는 함수 모듈 및 설멸

1. erase_end_part_black_or_disolve(input_file):
1. 영상을 뒷부분 부터 읽어 블랙 디졸브로 끝난다면 블랙 디졸브 직전의 프레임 번호와 그떄의 frame을 반환한다.
1. 용도 <광고 스틸제작 뒷부분 블랙제거>



2. audio_ch_and_mode(input_file, ffprobe_path=None):
2. 오디오의 채널수와 스테레오 , 모노 등의 설정 값을 알려준다.



3. find_audio_start_end(file_path,duration = 1 ,threshold=0):
3. 오디오 및 비디오 파일에서 전체 길이중 소리가 처음 나오는 시간, 소리가 더 이상 나오지 않는 구간의 시작 시간을 알려준다.
3. 이 두 구간 사이가 실제적으로 소리가 나오는 시간이다.
3. 용도 < 광고에서 앞이나 뒤에 스틸이 길에 붙어있을때 실제적 사용 부분 탐지>



4. make_still_video_to_proress_hq(input_file, output_file,video_width,video_height, duration, ffmpeg_path=None):
4. png 혹은 jpg 파일을 넣으면 proress hq로 지정한 해상도와 길이만큼의 스틸 동영상을 만든다.
4. 용도 스틸용 비디오 



5. calculate_match_percentage(frame, input_picture, grid_size,Match_Rate)
5. opencv로 읽은 frame 과 jpg, png등의 input_picture가 얼마나 유사도를 갖고 있는지 보여주는 함수
5. grid는 화면을 몇 조각으로 분할 할 것인지 나타낸다 예) 8 일 경우 8*8 = 64개로 화면을 분할해 유사도 비교
5. Match_Rate의 경우는 rgb값이 얼마나 유사해야 같은 것으로 인식하냐의 입력 값이다. 0~255 까지로 표현되는 색상값을
5. 0~100 까지의 퍼센트 입력하여 100일경우 100% 완전 같은 값이여야 같은 것으로 인식한다는 것이다. 보통 99.5 로해서 99.5% 이상 값이 같다면 
5. 일치하는 걸로 본다. 99.5라는 뜻은 r =100, r=99.5 는 같다고 보는 것이다. (실제론 0~255 까지라서 scale up 되어 99.2 정도까지는 같다고 볼 듯.. ) 



6.find_cbf_mean(input_data, ranges = None, only_need_total_rgb_mean = False):
6. frame, jpg, png, 모두 input_data에 입력 가능하다.
6. RGB 전체 평균 / R 평균 / G 평균 /B 평균 /밝기 값 평균 / 영상 주파수 평균 을 가져오는 함수 
    <예시> <영상주파수만 가져오고 싶다면>
    frequency_mean = find_cbf_mean(input_picture)[5]
    print(frequency_mean) 
6. 자막이 들어가지 못하는 화면의 바깥 5% 부분등 부분만 추려서 위의 값들도 구할 수 있다.(ranges 변수 사용)
    <추가>  <아래서 u자 모형만 긁어서 추출>
    input_picture = 'path_to_image.jpg'
    # 예시: U자 모양 영역 지정
    u_shape_ranges = ["0:120,0:180", "990:1080,0:180"]  # x는 0~120 y는 0~180 부분과 x는 990~1000, y는 0~180 부분을 추려서 검사하겠다. 
    result = find_cbf_mean(input_picture, ranges=u_shape_ranges)
6. 모든 값들이 필요없고 단순히 rgb_total_mean만 필요한 경우도 있다. 이 경우 변수 only_need_rgb_mean = True 로 해주면 된다.
    아무래도 조금 더 빠르다.
    <사용 예시>
    input_picture = frame
    ranges = [
        "300:600,0:45",  # 첫 번째 범위
        "300:600,675:719",  # 두 번째 범위 (720의 경우 0~ 719 까지 픽셀을 가지고 있다 0이 있어서 1씩 당겨 짐)
    ]
    result = find_cbf_mean(input_picture,ranges,True)
    
    이 경우 화면의 상단과 하단의 가운데 부분만 평균을 측정하게 된다. 이게 계속 0으로 검은색인데 전체 화면은 색상이 있다면
    "영화"를 tv에서 상영하면서 위에 검은색 바 처리한 "레터박스"가 있는 화면으로 볼 수 있다.


7.-------
find_cut_change(input_file, start_frame_cnt, threshold):

동영상 파일의 start_frame_cnt(지정프레임) 부터 한 프레임씩 세어 보면서 밝기 차이가 threshold 이상 차이가 난다면
이전 컷과 현재 컷을 히스토그램 비교해 본다.  히스토그램 유사도가 95% 이하라면 컷 변경이 됏음으로 인식하며
그떄의 프레임수, 프레임, 컷 변경까지의 프레임 개수 를 반환한다. (어두운 화면에서 블랙이 낄 경우를 대비해 어두운 화면에는 더 정밀한 검출이 들어간다.)
히스토그램 유사도를 포함시킨이유는 카메라 감독의 손떨림으로 인해 컷이 바뀐 것으로 감지 할 수 있기 때문이다.
<용도>
프레임 수 - 다음 컷 변경 탐지를 이어서 하기 위해 마무리 지점의 프레임 번호를 받는다.
프레임 - 변경된 컷이 블랙인지, 오류 파일인지 등등 검출 대상이 되는 화면이다
변경까지 프레임 수 - 이게 너무 짧다면 소위 튄 화면일 수 있다. 만약 컷 번경이 5프레임 이하에서 일어난다면
                PD가 이 화면을 1/6 초 (30p 가정) 만 사용했다는 건데 이건 실수로 튄 것이다.
                <튄 화면이 아니더라도 이렇게 짧은 컷 변화를 했다면 눈으로 QC하도록 해야 함.>
7--------


"""
ㄴ








import cv2 
import numpy as np

def calculate_grid_brightness(frame, grid_size):
    """프레임을 grid_size x grid_size 격자로 나누고, 각 격자의 평균 밝기를 계산합니다."""
    h, w = frame.shape[:2]
    grid_h, grid_w = h // grid_size, w // grid_size
    brightness_grid = np.zeros((grid_size, grid_size))

    for i in range(grid_size):
        for j in range(grid_size):
            grid = frame[i * grid_h:(i + 1) * grid_h, j * grid_w:(j + 1) * grid_w]
            brightness_grid[i, j] = np.mean(grid)

    return brightness_grid

def erase_end_part_black_or_disolve(input_file):

    # 동영상 파일을 열기
    cap = cv2.VideoCapture(input_file)

    if not cap.isOpened():
        print("Error: 동영상 파일을 열 수 없습니다.")
        return -1

    # 동영상의 총 프레임 수 확인
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # RGB 평균값이 8보다 큰 첫 프레임 찾기
    for frame_idx in range(total_frames - 1, -1, -1):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            continue

        if frame.mean() > 8:
            previous_brightness = np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
            break

    if frame_idx == 0:
        print("조건에 맞는 프레임을 찾지 못했습니다.")
        return -1

    # 밝기 변화가 0.5 이하인 프레임 찾기
    
    for next_frame_idx in range(frame_idx - 1, -1, -1):
        cap.set(cv2.CAP_PROP_POS_FRAMES, next_frame_idx)
        ret, frame = cap.read()
        if not ret:
            continue

        current_brightness = np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
        if abs(current_brightness - previous_brightness) <= 0.5:
            print(f"밝기 변화가 0.5 이하인 프레임 발견: 프레임 인덱스 {next_frame_idx+1}")
            break
        previous_brightness = current_brightness
   
    previous_frame = frame
    next_frame_idx = next_frame_idx+1
    
    for third_frame_idx in range(next_frame_idx - 1, -1, -1):
        cap.set(cv2.CAP_PROP_POS_FRAMES, third_frame_idx )
        ret, frame = cap.read()
        if not ret:
            continue

        if previous_frame is not None:
            current_grid = calculate_grid_brightness(frame, 8)
            previous_grid = calculate_grid_brightness(previous_frame, 8)

            # 모든 격자에서 밝기 차이가 1 이하인지 확인
            if np.all(np.abs(current_grid - previous_grid) <= 1):
                print(f"모든 격자에서 밝기 변화가 1 이하인 프레임 발견: 프레임 인덱스 {third_frame_idx+1}")
                return third_frame_idx +1 , previous_frame

        previous_frame = frame

    print("밝기 변화가 2 이상인 구간이 있는 프레임을 찾지 못했습니다.")
    return -1 ,None

# 사용법 print(erase_end_part_black_or_disolve(r"/Users/imsejin/Desktop/출/프레임 검출 테스트용 동영상.mxf"))
# 사용 예시 광고 파일등을 뒤에서 부터 읽어서 블랙이 껴있으면 그 이전, 블랙 디졸브로 끝나면 디졸브의 시작점을 잡아서 프레임 번호화 프레임을 알려줍니다.
# 광고 자동 제작기에 쓰려고 만듬;;; 
# 앞에 블랙 제거, 뒤에 블랙 및 스틸 만들려고  만든 모듈입니다.

##### 모둘 2############
import subprocess
import json
import os

def audio_ch_and_mode(input_file, ffprobe_path=None):
    # ffmpeg 경로 설정
    print(ffprobe_path)
    if ffprobe_path is None:
        ffprobe_path = os.getenv('FFMPEG_PATH', 'ffprobe')  # 환경변수에서 찾거나 기본값 'ffprobe'

    try:
        # ffprobe 명령 구성
        cmd = [
            ffprobe_path,
            '-v', 'error', 
            '-select_streams', 'a:0',  # 첫 번째 오디오 스트림 선택
            '-show_entries', 'stream=channels,channel_layout',
            '-of', 'json',
            input_file
        ]

        # Windows에서 cmd 창이 나타나지 않도록 설정
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # ffprobe 명령 실행
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, startupinfo=startupinfo)
        
        # 결과를 JSON으로 파싱
        info = json.loads(result.stdout)

        # 오디오 스트림 정보 추출
        channels = info['streams'][0]['channels']
        layout = info['streams'][0].get('channel_layout', '')

        # 채널과 모드 결정
        mode = 'stereo' if 'stereo' in layout else 'mono' if channels == 1 else 'multi-channel'
        return channels, mode

    except Exception as e:
        return "Error: " + str(e)

# 사옹 예시 _print(audio_ch_and_mode(r"/Users/imsejin/Desktop/출/프레임 검출 테스트용 동영상.mxf",r"/Users/imsejin/Downloads/ffprobe"))


from moviepy.editor import VideoFileClip, AudioFileClip
import numpy as np
import os

def find_audio_start_end(file_path,duration = 1 ,threshold=0):
    """
    비디오 또는 오디오 파일에서 소리가 시작되는 부분과 끝나는 부분을 탐지합니다.

    :param file_path: 소리를 탐지할 파일 경로 (비디오 또는 오디오 파일)
    :param threshold: 소리를 감지하기 위한 임계값 (기본값: 0.01)
    :return: (시작 초, 끝 초) 튜플
    """
    file_extension = os.path.splitext(file_path)[-1].lower()  # 파일 확장자 추출 및 소문자로 변환

    if file_extension in ('.mp4', '.avi', '.mkv', '.mov', '.mxf'):
        clip = VideoFileClip(file_path)
        sample_rate = clip.fps
    else:
        clip = AudioFileClip(file_path)
        sample_rate = clip.fps // 2

    total_duration = clip.duration

    start_time = None
    end_time = None
    t = 0
    while t < int(total_duration):
        subclip = clip.subclip(t, t + duration)
        audio = subclip.audio.to_soundarray() if hasattr(subclip, 'audio') else None

        if audio is not None:
            audio_energy = np.sum(audio**2) / float(len(audio))
            if audio_energy > threshold:
                if start_time is None:
                    start_time = t
                break  # 원하는 조건을 만족하면 전체 루프를 중단합니다.
        
        t += duration   # 다음 반복을 위해 t 값을 증가시킵니다.
                

    # 뒤에서부터 탐색하여 끝 시간 결정
    if start_time is not None:
        t = int(total_duration) - duration   # 정수로 시작 시간 설정
        while t < int(total_duration):
            subclip = clip.subclip(t, t + duration)
            audio = subclip.audio.to_soundarray() if hasattr(subclip, 'audio') else None

            if audio is not None:
                audio_energy = np.sum(audio**2) / float(len(audio))
                if audio_energy > threshold:
                    end_time = t
                    break
            
            t -= duration  # 다음 반복을 위해 t 값을 1씩 증가시킵니다.
    else:
        end_time = None

    return (start_time, end_time)

""" 사용 예제
file_path = r"/Users/imsejin/Desktop/출/프레임 검출 테스트용 동영상.mxf"
result = find_audio_start_end(file_path,0.1)

if result:
    start, end = result
    print(f"Audio or Video starts at {start} seconds and ends at {end} seconds.")
else:
    print("이 파일은 비디오 또는 오디오 파일이 아닙니다.")
"""

###################


import subprocess
import os
from PIL import Image

def fix_gbr_to_rgb(input_file, output_file):
    img = Image.open(input_file)

    # 이미지의 모드가 GBR인 경우 RGB로 변환
    if img.mode == 'RGB':
        img = img.convert('RGB')
    # 이미지의 모드가 RGBA인 경우 RGB로 변환
    if img.mode == 'RGBA':
        img = img.convert('RGB')
        
    # 수정된 이미지 저장
    img.save(output_file)
    
def generate_unique_filename(base_path, ext):
    counter = 1
    unique_path = base_path + ext

    # 파일이 이미 존재하는지 확인하고, 중복된 경우 숫자를 증가시키면서 새로운 이름 생성
    while os.path.exists(unique_path):
        unique_path = f"{base_path}_{counter}{ext}"
        counter += 1

    return unique_path

def make_still_video_to_proress_hq(input_file, output_file,video_width,video_height, duration, ffmpeg_path=None):
    # GBR에서 RGB로 이미지 색 채널 순서 수정
    temp_input_file = "temp_rgb_input.jpg"
    base_path, ext = os.path.splitext(temp_input_file)
    temp_input_file = generate_unique_filename(base_path, ext) # 결과물 이름 중복 예방
    fix_gbr_to_rgb(input_file, temp_input_file)

    # 입력 파일의 확장자를 확인하여 jpg 또는 png 여부를 검사
    if not temp_input_file.lower().endswith(('.jpg', '.jpeg', '.png')):
        raise ValueError("입력 파일은 jpg 또는 png 확장자를 가져야 합니다.")

    # 확장자 변경
    output_base, _ = os.path.splitext(output_file)
    output_file = output_base + ".mov"

    base_path, ext = os.path.splitext(output_file)
    output_file = generate_unique_filename(base_path, ext) # 결과물 이름 중복 예방
    
    
    # ffmpeg_path가 주어지지 않았을 경우, 기본 경로로 설정
    if ffmpeg_path is None:
        ffmpeg_path = "ffmpeg"

    # ffmpeg를 사용하여 동영상 생성
    cmd = [
        ffmpeg_path,
        '-loop', '1',  # 이미지를 지속적으로 반복
        '-t', str(duration),
        '-i', temp_input_file,
        '-c:v', 'prores_ks',  # 'prores_ks' 인코더 사용
        '-profile:v', '3',  # ProRes 422 HQ 프로파일
        '-pix_fmt', 'yuv420p',
        '-s', f'{video_width}x{video_height}',  # 레퍼런스 비디오의 해상도 사용
        output_file  # 출력 파일 경로
    ]



    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"동영상 생성이 완료되었습니다. 출력 파일: {output_file}")
        os.remove(temp_input_file)
        return output_file
    except subprocess.CalledProcessError as e:
        print("오류 발생:", e)
        os.remove(temp_input_file)
        return None
"""
그림파일과 , 해상도, 시간을 입력하면 proress hq로 스틸 동영상을 만듭니다.
(광고 프로그램에 스틸추가용으로 사용하기 위해 만들었습니다.)
make_still_video_to_proress_hq(input_file, output_file,video_width,video_height, duration, ffmpeg_path=None):
# 예제 사용법:
input_file = "input.png"
output_file = "output.mp4"
duration = 10  # 초 단위
reference_video = r"/Users/imsejin/Desktop/출/프레임 검출 테스트용 동영상.mxf"
video_width =1920
video_height =1080
make_still_video_to_proress_hq(input_file, output_file,video_width,video_height,10, r"/Users/imsejin/Downloads/ffmpeg")
"""

#######################################
import cv2
import numpy as np

def calculate_match_percentage(frame, input_picture, grid_size,Match_Rate):
    
    def resize_image_to_frame(frame, input_picture):
        """주어진 프레임의 크기에 맞게 이미지를 리사이즈합니다."""
        frame_height, frame_width = frame.shape[:2]
        resized_image = cv2.resize(input_picture, (frame_width, frame_height))
        return resized_image
    
    def calculate_grid_rgb(frame, grid_size):
        h, w = frame.shape[:2]
        grid_h, grid_w = h // grid_size, w // grid_size
        rgb_grid = np.zeros((grid_size, grid_size, 3))

        for i in range(grid_size):
            for j in range(grid_size):
                grid = frame[i * grid_h:(i + 1) * grid_h, j * grid_w:(j + 1) * grid_w]
                rgb_grid[i, j] = np.mean(grid, axis=(0, 1))

        return rgb_grid
    
    def percentage_to_atol(percentage):
        """퍼센트 값을 역으로 계산하여 atol 값으로 변환합니다.
        100%는 완전한 일치를, 0%는 모든 차이를 허용합니다."""
        max_difference = 255
        inverted_percentage = 100 - percentage
        atol = (inverted_percentage / 100) * max_difference
        return atol

    
    resized_image = resize_image_to_frame(frame, input_picture)
    frame_rgb_grid = calculate_grid_rgb(frame, grid_size)
    input_rgb_grid = calculate_grid_rgb(resized_image, grid_size)

    atol = percentage_to_atol(Match_Rate)
    # 일치하는 격자의 수를 계산 tol은 픽셀 값 오차를 허용하는 값이다. 예를들어 atol =10 이면 rgb 0~255까지 중 2 비교 값이 값차이가 10 이내이면 같다고 본다.
    # 0~100% 까지 숫자를 인자로 받아 함수를 통해 atol 값을 받아 아래 적용한다. def percentage_to_atol(percentage):
    match_count = np.sum(np.isclose(frame_rgb_grid, input_rgb_grid, atol)) / 3  # atol은 색상 차이의 허용 범위를 조정합니다

    # 일치하는 백분율 계산
    total_grids = grid_size * grid_size
    match_percentage = (match_count / total_grids) * 100

    return match_percentage


######################## 사용예
# calculate_match_percentage(frame, "abc.jpg", 8 ,99.9)  calculate_match_percentage(프레임, 그림파일, 조각 격자 수 ,일치 퍼센트) 
# abc.jpg 파일을 frame 과 같은 사이즈로 바꾸고 (opencv_에서 read로 읽은 frame)
# 8x8 로 조각을 낸다음 각 조각 부분을 비교해서 99.9% 일치하는 부분이 몇 조각 있는지 퍼센트로 보여줍니다.
# 사용 예시) 어도비 미디어 오류 배경에 자막은 살아서 올라가있는 경우, 오류화면과 캡쳐 프레임 두개를 비교하면 90% 이상 일치 하겠죠 ..?

import cv2
import numpy as np

def find_cbf_mean(input_data, ranges = None, only_need_total_rgb_mean = False):
    """이미지 파일 또는 OpenCV 프레임에서 여러 평균값을 계산합니다."""
    
    # 입력 데이터가 파일 경로인지 확인
    if isinstance(input_data, str):
        # 이미지 파일 로드
        image = cv2.imread(input_data, cv2.IMREAD_UNCHANGED)
    else:
        # 이미 배열 형태의 이미지(OpenCV 프레임)로 가정
        image = input_data

    # 알파 채널이 있는 경우 제거
    if image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    # 지정된 범위들에 대해 이미지 처리
    if ranges:
        selected_areas = []
        for range in ranges:
            x_range, y_range = range.split(',')
            x_start, x_end = map(int, x_range.split(':'))
            y_start, y_end = map(int, y_range.split(':'))
            selected_area = image[y_start:y_end, x_start:x_end]
            selected_areas.append(selected_area)

        # 선택된 영역들을 하나로 결합
        if selected_areas:
            image = np.concatenate(selected_areas, axis=0)
    if only_need_total_rgb_mean == False:
        # RGB 채널의 평균 계산
        mean_rgb = cv2.mean(image)[:3]
        mean_r, mean_g, mean_b = mean_rgb

        # 밝기 값 평균
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        mean_brightness = np.mean(gray_image)

        # 영상 주파수 평균
        f = np.fft.fft2(gray_image)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = 20*np.log(np.abs(fshift))
        mean_frequency = np.mean(magnitude_spectrum)

        return np.mean(mean_rgb), mean_r, mean_g, mean_b, mean_brightness, mean_frequency
    else:
        mean_rgb = cv2.mean(image)[:3]
        mean_r, mean_g, mean_b = mean_rgb
        return np.mean(mean_rgb)


# 사용 예 find_cbf_mean("abc.png") 혹은 find_cbf_mean(frame) :
# jpg or png or 프레임(opencv로 read 후 전달)의 rgb 전체평균, r 평균, g 평균 ,b 평균, 밝기 평균, 주파수 평균을 반환한다.
# 실행파일 옆에 "정밀 검출 폴더" 등을 만들고 거기에 jpg나 png를 넣어 시작전 위와 같은 데이터들을 확보 해 두면
# 검출에 사용할 수 있다. 예를들어 오류 "adobe_media_error.jpg" 파일을 넣어 놓는다면,
# 이 파일과 이 그림판 파일의 rgb 전체평균, r 평균, g 평균 ,b 평균, 밝기 평균, 주파수 평균이 모두 10% 오차 범위에서 일치하는
# 파일이 있을까?, 일치하지 않는 화면인데 이 조건에 해당한다면, 그것은 검출기에서 눈으로 확인하고 skip하면 된다;
"""
1. RGB 전체 평균
2. R 평균
3. G 평균
4. B 평균
5. 밝기 값 평균
6. 영상 주파수 평균
각 값을 개별로 쓰고 싶으면 ? (프로그래밍 언어는 0부터 시작 )
<예시> <영상주파수만 가져오고 싶다면>
frequency_mean = find_cbf_mean(input_picture)[5]
print(frequency_mean) 

<추가버전>  <영상에서 부분만 긁어서 하고 싶은경우 > <아래서 u자 모형만 긁어서 추출>
input_picture = 'path_to_image.jpg'
# 예시: U자 모양 영역 지정
u_shape_ranges = ["0:120,0:180", "990:1080,0:180"] 
result = find_cbf_mean(input_picture, ranges=u_shape_ranges)

<추가예시>
input_picture = 'path_to_image.jpg'
ranges = [
    "0:120,0:180",  # 첫 번째 범위
    "990:1080,0:180",  # 두 번째 범위
    "x1_start:x1_end,y1_start:y1_end",  # 세 번째 범위
    "x2_start:x2_end,y2_start:y2_end",  # 네 번째 범위
    # ... 추가 범위
    "x9_start:x9_end,y9_start:y9_end"  # 열 번째 범위
]
result = find_cbf_mean(input_picture, ranges=ranges)


<사용예시>

좌상단 우상단을 제외한 하위, 바깥 부분에 u자공간은 자막이 들어갈 수 없는 공간이다.

이 공간의 주파수 평균, 색상 평균은 오류파일이라면 같을 수 밖에 없다.
보통 u자로 하고 두꼐를 5% 정도 로 하면 95% 이상의 일치 조건을 걸었을 때 검출한다.


input_picture = 'path_to_image.jpg'
ranges = [
    "300:600,0:45",  # 첫 번째 범위
    "300:600,675:719",  # 두 번째 범위 (720의 경우 0~ 719 까지 픽셀을 가지고 있다 0이 있어서 1씩 당겨 짐)
]
result = find_cbf_mean(input_picture, ranges=ranges)

이거 해보면 레터박스 (영화를 tv에서 상영해서 해상도 때문에 상단에 '검은 바' 깔아 놓는 것) 체크 가능

 find_cbf_mean(input_data, ranges = None, only_need_total_rgb_mean = True):
 이렇게 할 시 total_rgb_mean만 반환하여 더 빠르다.
"""


import cv2
import numpy as np
def calculate_average_rgb(image_chunk):
    # 이미지 조각의 평균 RGB 값을 계산합니다.
    average_color_per_row = np.average(image_chunk, axis=0)
    average_color = np.average(average_color_per_row, axis=0)
    return average_color

def count_low_average_chunks(converted_frame, chunk_size=(8, 8)):
    # 이미지의 높이와 너비를 얻습니다.
    height, width, _ = converted_frame.shape
    
    # 조각의 개수를 세는 변수를 초기화합니다.
    count = 0

    # 이미지를 8x8 크기의 조각으로 나누어 각 조각을 처리합니다.
    for y in range(0, height, chunk_size[1]):
        for x in range(0, width, chunk_size[0]):
            chunk = converted_frame[y:y+chunk_size[1], x:x+chunk_size[0]]
            average_color = calculate_average_rgb(chunk)

            # 평균 RGB 값이 모두 1보다 작은 경우, count를 증가시킵니다.
            if all(i < 1 for i in average_color):
                count += 1

    return count

def calculate_histogram(image):
    # 그레이스케일 이미지로 변환
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 히스토그램 계산
    hist = cv2.calcHist([gray_image], [0], None, [256], [0, 256])
    # 히스토그램 정규화
    hist = cv2.normalize(hist, hist).flatten()
    return hist

def find_cut_change(input_file, start_frame_cnt, threshold):
    # 동영상 파일 열기
    cap = cv2.VideoCapture(input_file)
    if not cap.isOpened():
        return None, None, None

    frame_count = 0
    prev_brightness = None
    prev_frame_hist = None
    prev_frame = None
    
    # 지정된 프레임으로 이동
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame_cnt)
    while True:
        # 프레임 읽기
        ret, frame = cap.read()

        # 프레임 읽기 실패 시 종료
        if not ret:
            break

        # 현재 프레임의 밝기 계산
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        current_brightness = np.mean(frame_gray)

        # 첫 프레임의 정보 설정
        if prev_brightness is None:
            prev_frame = frame
            prev_brightness = current_brightness
            frame_count += 1
            continue
        # 어두운 화면에서 블랙이 끼는 경우가 있을 수 있으니 밝기갑이 35이하일 경우 세밀하게 검사하는 로직을 추가한다.(10배 가중치)
        if current_brightness < 35  and abs(current_brightness - prev_brightness) > (threshold/10):
            converted_frame = np.copy(frame)
            # 2보다 큰 모든 값에 대해 255로 설정
            converted_frame[converted_frame > 2] = 255
            chunk_size=(8, 8)
            total_size = chunk_size[0] * chunk_size[1]
            cnt_of_black = count_low_average_chunks(converted_frame, chunk_size)
            
            if (cnt_of_black/total_size)*100 > 20 : #64 조각 중 진짜 블랙이 (20% 이상이라면) 보수적으로 잡았습니다 
                cap.release()
                return start_frame_cnt + frame_count, frame, frame_count
            ## 이거 떄문에 겁나 느려졌을 듯 ;;; 별 수 없는 듯;;
            
        # 밝기 변화가 임계값을 초과하면
        elif current_brightness >= 35 and abs(current_brightness - prev_brightness) > threshold:
            # 이전 프레임과 현재 프레임의 히스토그램 유사도 계산
                    # 현재 프레임의 히스토그램 계산
            prev_frame_hist = calculate_histogram(prev_frame)
            current_frame_hist =calculate_histogram(f)
            hist_similarity = cv2.compareHist(prev_frame_hist, current_frame_hist, cv2.HISTCMP_CORREL)

            # 히스토그램 유사도가 95% 이하일 경우에만 컷 변경으로 간주
            # 컷 변경 경계값을 보수적으로 하면 , 카메라 감독이 손을 떨 경우에도 컷으로 보는 경우가 있다. 그런 경우를 필터링 하려고 넣어준 조건이다.
            if hist_similarity < 0.95:  ## 바퀸컷과 이전컷의 유사도가 95% 이하여야 한다..
                cap.release()
                return start_frame_cnt + frame_count, frame, frame_count

        # 이전 프레임 정보 업데이트
        prev_frame = frame
        prev_brightness = current_brightness
        frame_count += 1

    cap.release()
    return None, None, None

'''
find_cut_change(input_file, start_frame_cnt, threshold):
동영상 파일의 start_frame_cnt(지정프레임) 부터 한 프레임씩 세어 보면서 밝기 차이가 threshold 이상 차이가 난다면
이전 컷과 현재 컷을 비교해봐서 히스토그램 유사도가 95% 이하라면 컷 변경이 됏음으로 인식하며
그떄의 프레임수, 프레임, 컷 변경까지의 프레임 개수 를 반환한다.
<용도>
프레임 수 - 다음 컷 변경 탐지를 이어서 하기 위해 마무리 지점의 프레임 번호를 받는다.
프레임 - 변경된 컷이 블랙인지, 오류 파일인지 등등 검출 대상이 되는 화면이다
변경까지 프레임 수 - 이게 너무 짧다면 소위 튄 화면일 수 있다. 만약 컷 번경이 5프레임 이하에서 일어난다면
                PD가 이 화면을 1/6 초 (30p 가정) 만 사용했다는 건데 이건 실수로 튄 것이다.
                <튄 화면이 아니더라도 이렇게 짧은 컷 변화를 했다면 눈으로 QC하도록 해야 함.>
'''
