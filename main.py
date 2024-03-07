import sys

import ffmpeg_finder
import file_ready_checker
import lsj_jsx_module
import module



import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import Toplevel
from tkinter import messagebox
import os
import shutil
import time
import win32com.client
import threading
import psutil
import random
import re
import subprocess
import glob
################################################



# def check_date_and_exit():
#     import ntplib
#     from time import ctime
#     import sys
#     from datetime import datetime
#     try:
#         # NTP 서버에서 현재 시간을 가져옵니다.
#         client = ntplib.NTPClient()
#         response = client.request('pool.ntp.org')
#         current_time = datetime.strptime(ctime(response.tx_time), "%a %b %d %H:%M:%S %Y")
#
#         # 종료할 날짜를 설정합니다. 여기서는 2024년 2월 6일입니다.
#         exit_date = datetime(2026, 2, 6)
#
#         # 현재 시각이 설정한 날짜 이상인지 확인합니다.
#         if current_time >= exit_date:
#             print("현재 시각이 2024년 2월 6일 이상입니다. 프로그램을 종료합니다.")
#             sys.exit()  # 프로그램 종료
#         else:
#             print("프로그램을 계속 실행합니다.")
#     except Exception as e:
#         print(f"시간을 확인하는 도중 오류가 발생했습니다: {e}")
#
#
# # 함수 호출
# check_date_and_exit()

##################################################



#### 쓰레딩 간 공유될 변수 선언####
state_of_gui_exit = 0
state_of_multi_1_exit = 0
state_of_multi_2_exit = 0
state_data_lock = threading.Lock()
# 0은 시작전 1은 시작 2는 종료 및 타 쓰레딩 종료 요청

##### 글로벌 변수 선언 #######

ffmpeg_path = ffmpeg_finder.find_ffmpeg_path()
ffprobe_path = ffmpeg_finder.find_ffprobe_path()
ffplay_path  = ffmpeg_finder.find_ffplay_path()

input_folder_path =""
output_folder_path =""
AME_file_path =""
selected_resolution =""
selected_audio_channel =""
selected_still_time =""
my_ip =""
net_working_folder_path=""
local_working_folder_path =""






# 1 시작 버튼 안누른 상태
# 2 시작버튼은 눌러 작동중인 상태
# 3 종료 요청이 들어왔지만 아직 하던 작업이 있는 상태
# 4 하던 작업까지 끝난 상태

##############################


def ame_working_in_cli(ame_path, script_path, pid_save_path):
    # 명령어 구성 (shell=True 제거)
    command = [ame_path, '--console', 'es.processFile', script_path]

    # subprocess.Popen을 사용하여 프로세스 시작 (백그라운드에서 실행)
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text=True,
                               encoding='cp949',
                               creationflags=subprocess.CREATE_NO_WINDOW)  # 백그라운드 실행 설정

    # PID 얻기
    pid = process.pid
    print("PID:", pid)

    # 메모장에 pid를 적어 놓음
    with open(pid_save_path, 'w', encoding='cp949') as file:
        file.write(str(pid))

    return pid


def want_know_korea_word_in_path():
    def contains_korean(text):
        return any('\uAC00' <= char <= '\uD7A3' for char in text)

    # 현재 실행 중인 파이썬 인터프리터의 절대 경로
    current_dir = os.path.dirname(sys.executable)
    current_dir = os.path.dirname(current_dir)

    # 경로에 한글이 포함되어 있는지 확인
    if contains_korean(current_dir):
        print("경로에 한글이 포함되어 있습니다:", current_dir)
        return True
    else:
        print("경로에 한글이 포함되어 있지 않습니다.", current_dir)
        return False


class App:
    def __init__(self, root):
        global state_of_multi_1_exit, state_of_multi_2_exit, state_of_gui_exit
        with state_data_lock:  # 공유 변수에만 락을 적용
            state_of_gui_exit = 1

        def checking_state_of_exit():
            global state_of_multi_1_exit,state_of_multi_2_exit,state_of_gui_exit
            with state_data_lock:  # 공유 변수에만 락을 적용
                state_of_gui_exit = 2

            def do_nothing():
                pass

            def actions_after_timeout():
                new_window.destroy()
                self.start_btn.config(state=tk.NORMAL)

            root.protocol("WM_DELETE_WINDOW", do_nothing)

            new_window = Toplevel(root)
            new_window.title("종료 요청")
            new_window.lift()
            new_window.attributes('-topmost', True)

            new_window.protocol("WM_DELETE_WINDOW", do_nothing)


            tk.Label(new_window,
                     text=f"\n\n 종료를 요청했습니다.\n\n\n 작업중인 작업까지 마치고 종료합니다. \n\n\n 자동으로 닫힙니다.\n\n", fg="black",
                     font=("Arial", 12, "bold")).pack()

            def check_state():
                global state_of_multi_1_exit, state_of_multi_2_exit, state_of_gui_exit
                with state_data_lock:  # 공유 변수에만 락을 적용
                    state_of_multi_1 = state_of_multi_1_exit
                    state_of_multi_2 = state_of_multi_2_exit
                print(f"멀티 작업 상태 입니다 -> 멀티 1 : {state_of_multi_1}             멀티 2 : {state_of_multi_2}")
                if state_of_multi_1 == 2 and state_of_multi_2 == 2:
                    new_window.destroy()
                    root.destroy()
                    sys.exit()
                elif state_of_multi_1 == 0 and state_of_multi_2 == 0:
                    new_window.destroy()
                    root.destroy()
                    sys.exit()
                else:
                    new_window.after(10000, check_state)

            new_window.after(10, check_state)


        self.root = root
        root.title("AME를 통한 광고 자동 제작기_Q&A(32391)")
        root.geometry('500x600')
        root.protocol("WM_DELETE_WINDOW", checking_state_of_exit)

        label_1 = tk.Label(root, text="-" * 70, font=("Arial", 12, "bold"))
        label_1.pack()

        # label_1 = tk.Label(root, text="경로 입력 후 시작을 눌러 주세요 ", fg="blue", font=("Arial", 14, "bold"))

        label_2 = tk.Label(root, text="경로 입력 후 시작을 눌러 주세요", font=("Arial", 12, "bold"))
        label_2.pack(pady=10)
        label_3 = tk.Label(root, text="-" * 70, font=("Arial", 12, "bold"))
        label_3.pack()

        # 입고 버튼 및 레이블
        self.input_btn = tk.Button(root, text="입력 폴더", command=self.select_input_folder)
        self.input_btn.pack(pady=5)
        self.input_label = tk.Label(root, text="미완성 광고를 넣을 폴더를 입력하세요.", fg="blue", font=("Arial", 10, "bold"))
        self.input_label.pack(pady=5)

        label_4 = tk.Label(root, text="-" * 70, font=("Arial", 12, "bold"))
        label_4.pack()

        # 출고 버튼 및 레이블
        self.output_btn = tk.Button(root, text="출력 폴더", command=self.select_output_folder)
        self.output_btn.pack(pady=5)
        self.output_label = tk.Label(root, text="스틸, 오디오 표준화 후 파일이 나올 장소 입니다.", fg="blue", font=("Arial", 10, "bold"))
        self.output_label.pack(pady=5)

        label_5 = tk.Label(root, text="-" * 70, font=("Arial", 12, "bold"))
        label_5.pack()

        # AME 경로 버튼 및 레이블
        self.ame_btn = tk.Button(root, text="프리미어 경로", command=self.select_ame_folder)
        self.ame_btn.pack(pady=5)
        self.ame_label = tk.Label(root, text="Adobe_Premiere 경로를 선택해주세요", fg="blue", font=("Arial", 10, "bold"))
        self.ame_label.pack(pady=5)

        label_6 = tk.Label(root, text="-" * 70, font=("Arial", 12, "bold"))
        label_6.pack()
        label_7 = tk.Label(root, text="-" * 29 + "출력 옵션" + "-" * 29 , font=("Arial", 12, "bold"))
        label_7.pack()

        # 옵션 프레임
        option_frame = tk.Frame(root)
        option_frame.pack(pady=5)

        # 해상도 선택 라디오 버튼
        resolution_frame = tk.LabelFrame(option_frame, text="출력 해상도")
        resolution_frame.pack(side=tk.LEFT, padx=10)
        self.resolution_var = tk.StringVar(value="HD")
        self.resolution_radio_buttons = [
            tk.Radiobutton(resolution_frame, text="HD", variable=self.resolution_var, value="HD"),
            tk.Radiobutton(resolution_frame, text="UHD", variable=self.resolution_var, value="UHD")
        ]
        for rb in self.resolution_radio_buttons:
            rb.pack(anchor=tk.W)
        # 오디오 채널 선택 라디오 버튼
        channel_frame = tk.LabelFrame(option_frame, text="출력 오디오 채널")
        channel_frame.pack(side=tk.LEFT, padx=10)
        self.channel_var = tk.StringVar(value="2CH")
        self.channel_radio_buttons = [
            tk.Radiobutton(channel_frame, text="2CH", variable=self.channel_var, value="2CH"),
            tk.Radiobutton(channel_frame, text="8CH", variable=self.channel_var, value="8CH")
        ]
        for rb in self.channel_radio_buttons:
            rb.pack(anchor=tk.W)


        # 스틸 시간 선택 드롭다운 메뉴
        still_time_frame = tk.LabelFrame(option_frame, text="끝 스틸 시간")
        still_time_frame.pack(side=tk.LEFT, padx=10)
        self.still_time_var = tk.StringVar()
        self.still_time_combobox = ttk.Combobox(still_time_frame, textvariable=self.still_time_var, values=[str(i) for i in range(1, 51)])
        self.still_time_combobox.set('10')  # 기본값 설정
        self.still_time_combobox.pack()


        label_8 = tk.Label(root, text="-" * 70, font=("Arial", 12, "bold"))
        label_8.pack()

        # 시작 버튼
        self.start_btn = tk.Button(root, text="시작", command=self.start_processing)
        self.start_btn.pack(pady=10)
        # 상태 레이블 (초기에는 숨겨져 있음)

    def select_input_folder(self):
        global input_folder_path, output_folder_path, AME_file_path
        folder = filedialog.askdirectory()
        self.input_label.config(text=folder if folder else "입고 폴더를 선택해주세요")
        input_folder_path = folder

    def select_output_folder(self):
        global input_folder_path,output_folder_path,AME_file_path
        folder = filedialog.askdirectory()
        self.output_label.config(text=folder if folder else "출고 폴더를 선택해주세요")
        output_folder_path =folder
    def select_ame_folder(self):
        global input_folder_path, output_folder_path, AME_file_path ,local_working_folder_path
        def if_link_path(file_path):
            # 파일 경로가 바로가기인지 확인
            if file_path.endswith('.lnk'):
                # Create a shell object
                shell = win32com.client.Dispatch("WScript.Shell")
                # Resolve the shortcut
                shortcut = shell.CreateShortCut(file_path)
                # Return the target path
                return shortcut.Targetpath
            else:
                # 파일 경로가 바로가기가 아니면 원래의 경로를 반환
                return file_path

        self.start_btn.config(state=tk.DISABLED)


        file_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
        file_path = if_link_path(file_path)
        self.ame_label.config(text=file_path if file_path else "Adobe_Media_Encoder 경로를 선택해주세요")

        file_name = os.path.basename(file_path).replace(" ", "").lower()
        if os.path.basename(file_name) == "adobepremierepro.exe":
            path =os.path.dirname(file_path)
            path =os.path.dirname(path)

            print(path)
            def find_media_encoder_exe(path):
                """
                프리미어로 잘못 선택했을지라도 ame를 찾아보자
                """
                target_name = "adobemediaencoder.exe"  # 타겟 파일 이름의 소문자화 및 띄어쓰기 제거 버전
                for root, dirs, files in os.walk(path):
                    for file in files:
                        # 파일 이름을 소문자로 변환하고 띄어쓰기를 제거한 후 비교
                        if file.replace(" ", "").lower() == target_name:
                            return os.path.join(root, file)
                return None
            path = find_media_encoder_exe(path)
            file_path = path

        AME_file_path = file_path

        AME_file_path = if_link_path(AME_file_path)

        def check_words_in_file_path(file_path):
            # 파일 경로를 소문자로 변환
            file_path_lower = file_path.lower()

            # 확인할 단어들
            words = ['adobe', 'media', 'encoder']

            # 모든 단어가 파일 경로에 있는지 확인
            return all(word in file_path_lower for word in words)


        if check_words_in_file_path(str(file_path)):
            ##################################### 이미 실행 되어 있으면 ame를 종료하는 구문####################
            def kill_process_by_name(name):
                """ 주어진 이름의 프로세스를 찾아서 종료한다. """
                for proc in psutil.process_iter(['name']):
                    if proc.info['name'] == name:
                        proc.kill()
                        print(f"Process {name} has been terminated.")
                        return

                print(f"No process with name {name} is running.")

            # 프로세스 이름 설정 (예: 'Adobe Media Encoder.exe')
            process_name = os.path.basename(AME_file_path)
            try:
                kill_process_by_name(process_name)
            except:
                pass
            ##################################### 이미 실행 되어 있으면 ame를 종료하는 구문 - 끝 ####################

            def long_running_task_1():
                new_window = Toplevel(root)
                new_window.title("작동확인")
                new_window.lift()
                new_window.attributes('-topmost', True)

                def do_nothing():
                    pass

                def actions_after_timeout():
                    new_window.destroy()
                    self.start_btn.config(state=tk.NORMAL)

                new_window.protocol("WM_DELETE_WINDOW", do_nothing)

                tk.Label(new_window,
                         text=f"\n\n 어도비 미디어 인코더의 <정상 작동> 을 확인하고 있습니다.\n\n 로그인 없이도 <개발자 모드> 사용은 가능하지만 \n\n  <구독&결제> 없는 <상업적 사용>은 불법입니다.\n\n 꼭 결제 후 사용해야 합니다.  \n\n 최대 60초가 소요됩니다. \n\n\n 자동으로 닫힙니다.\n\n", fg="black",
                         font=("Arial", 12, "bold")).pack()


            ### 테스트를 진행 합니다.
                def long_running_task_1_1():

                    module.make_folder(local_working_folder_path,"pre_check",True)
                    pre_check_folder = os.path.join(local_working_folder_path,"pre_check")
                    lsj_jsx_module.screenshot_and_save(os.path.join(pre_check_folder,"before.jpg"))
                    ############################################################

                    current_dir = os.path.dirname(sys.executable)
                    folder_of_resolution = os.path.join(current_dir,"지우지마시오_프리셋저장소")

                    folder_of_HD_resolution = os.path.join(folder_of_resolution, "HD_프리셋_2CH")
                    print(f"폴더경로   {folder_of_HD_resolution}")

                    # .epr 확장자를 가진 모든 파일 경로를 가져옵니다.
                    epr_files = glob.glob(os.path.join(folder_of_HD_resolution, '*.epr'))

                    # 최신 파일을 찾기 위해 파일들을 수정 시간을 기준으로 정렬합니다.
                    epr_files.sort(key=os.path.getmtime, reverse=True)

                    # 최신 .epr 파일의 경로를 변수에 저장합니다.
                    if epr_files:
                        latest_epr_file = epr_files[0]
                        print("가장 최신의 .epr 파일 경로:", latest_epr_file)
                    else:
                        print(".epr 파일을 찾을 수 없습니다.")


                    pre_setting_epr_file_path = latest_epr_file

                    try:
                        shutil.copy(pre_setting_epr_file_path,pre_check_folder)
                    except:
                        pass

                    pre_setting_epr_file_path = os.path.join(pre_check_folder,os.path.basename(pre_setting_epr_file_path))
                    input_jpg_path = os.path.join(pre_check_folder,"before.jpg")
                    output_jpg_to_mxf_path =  os.path.join(pre_check_folder,"after.mxf")
                    status_of_making_process_txt_path = os.path.join(pre_check_folder, "status.txt")
                    jsx_file_path = os.path.join(pre_check_folder, "js_jpg_to_mxf.jsx")
                    pid_save_path = os.path.join(pre_check_folder, "pid.txt")
                    try:
                        lsj_jsx_module.make_jsx_file(input_jpg_path, pre_setting_epr_file_path ,output_jpg_to_mxf_path, status_of_making_process_txt_path,jsx_file_path)
                    except:
                        new_window = Toplevel(root)
                        new_window.title("오류")
                        tk.Label(new_window,
                                 text=f"어도비 미디어 작동 확인 테스트에 실패했습니다.\n\n\n 내부 파일중 하나를 지운 것 같습니다 \n\n\n 실행파일을 다시 받아 설치해 주세요 \n\n\n 5초 후 꺼집니다. ",
                                 fg="red",
                                 font=("Arial", 12, "bold")).pack()

                        # 창을 최상위로 만들기
                        new_window.lift()
                        new_window.attributes('-topmost', True)

                        def do_nothing():
                            pass

                        def actions_after_timeout():
                            new_window.destroy()
                            sys.exit()

                        new_window.protocol("WM_DELETE_WINDOW", do_nothing)
                        # 5초 후 창 닫기
                        new_window.after(5000, actions_after_timeout)


                    print("어도비 미디어 인코더 작동 체크 입니다. jpg를 mxf로 변환시켜 봅니다.")
                    ame_working_in_cli(AME_file_path, jsx_file_path,pid_save_path)
                    return

                def long_running_task_1_2():
                    global  AME_file_path
                    pre_check_folder = os.path.join(local_working_folder_path, "pre_check")
                    status_of_making_process_txt_path = os.path.join(pre_check_folder, "status.txt")
                    pid_save_path = os.path.join(pre_check_folder, "pid.txt")
                    cnt=0
                    while True:
                        if os.path.exists(status_of_making_process_txt_path):
                            with open(status_of_making_process_txt_path, 'r', encoding='cp949') as file:
                                content = file.read().strip()
                                if content == "시작":
                                    print(content)
                                if content == "실행완료":
                                    able_to_use =True
                                    break
                                if content == "실행실패":
                                    able_to_use = False
                                    print("실행에 실패하였습니다.")
                                    break
                        else:
                            print("상태 메모장 생성을 기다립니다.")
                        cnt += 1
                        if cnt > 20:
                            able_to_use = False
                            print("실행에 실패하였습니다.")
                            break
                        time.sleep(4)  # 3초 대기


                    with open(pid_save_path, 'r', encoding='cp949') as file:
                        pid = int(file.read().strip())

                    def terminate_process_by_pid(pid):
                        try:
                            # PID로 프로세스 객체를 가져옵니다.
                            process = psutil.Process(pid)
                            # 프로세스 종료
                            process.terminate()
                            return f"PID {pid} 프로세스가 종료되었습니다."
                        except psutil.NoSuchProcess:
                            return f"PID {pid}를 가진 프로세스가 존재하지 않습니다."
                        except psutil.AccessDenied:
                            return f"PID {pid} 프로세스를 종료할 권한이 없습니다."
                        except Exception as e:
                            return f"오류 발생: {e}"

                    print(terminate_process_by_pid(pid))



                    if able_to_use == True:

                        new_window_2 = Toplevel(new_window)
                        new_window_2.title("작동확인")
                        new_window_2.lift()
                        new_window_2.attributes('-topmost', True)

                        new_window_2.protocol("WM_DELETE_WINDOW", do_nothing)

                        tk.Label(new_window_2,
                                 text=f"\n\n <미디어 인코더>사용 가능합니다. \n\n\n 사용하겠습니다. \n\n\n 3초 후 자동으로 닫힙니다.\n\n", fg="blue",
                                 font=("Arial", 12, "bold")).pack()
                        time.sleep(1)
                        module.make_folder(local_working_folder_path, "pre_check", True)
                        return
                    if able_to_use == False:

                        new_window_2 = Toplevel(new_window)
                        new_window_2.title("작동확인")
                        new_window_2.lift()
                        new_window_2.attributes('-topmost', True)

                        new_window_2.protocol("WM_DELETE_WINDOW", do_nothing)

                        tk.Label(new_window_2,
                                 text=f"\n\n <미디어 인코더>사용 불가입니다. \n\n\n 인코더의 버전을 확인해 주세요 \n\n\n 5초 후 자동으로 닫힙니다.\n\n", fg="red",
                                 font=("Arial", 12, "bold")).pack()
                        file_path = "맞지 않는 버전의 프로그램 입니다."
                        AME_file_path = "맞지 않는 버전의 프로그램 입니다."
                        self.ame_label.config(text=file_path)
                        time.sleep(5)
                        return



                thread_1_1 = threading.Thread(target=long_running_task_1_1)
                thread_1_1.start()

                thread_1_2 = threading.Thread(target=long_running_task_1_2)
                thread_1_2.start()

                thread_1_1.join()
                thread_1_2.join()
                new_window.destroy()

                self.start_btn.config(state=tk.NORMAL) # 다시 시작버튼 활성화 시켜야 함
                return

            thread_1 = threading.Thread(target=long_running_task_1)
            thread_1.start()



        elif file_path != "":
            new_window = Toplevel(root)
            new_window.title("오류")
            tk.Label(new_window,
                     text=f"어도비 미디어 인코더가 아닌 것 같습니다.\n\n\n 경로 : {AME_file_path} \n\n\n 파일 경로에 'adobe', 'media', 'encoder'라는 단어가 있어야 합니다.\n\n\n 5초 후 자동으로 닫힙니다.", fg="red",
                     font=("Arial", 12, "bold")).pack()

            # 창을 최상위로 만들기
            new_window.lift()
            new_window.attributes('-topmost', True)

            def do_nothing():
                pass

            def actions_after_timeout():
                new_window.destroy()
                self.start_btn.config(state=tk.NORMAL)

            new_window.protocol("WM_DELETE_WINDOW", do_nothing)
            # 5초 후 창 닫기
            new_window.after(5000, actions_after_timeout)
            file_path = "Adobe_Media_Encoder 경로를 선택해주세요"
            AME_file_path =""
            self.ame_label.config(text=file_path)



    def start_processing(self):
        global input_folder_path, output_folder_path, AME_file_path,selected_still_time,selected_resolution,selected_audio_channel,my_ip,net_working_folder_path,local_working_folder_path
        # 시작 버튼 클릭시 조건 만족 확인
        if input_folder_path == "" or output_folder_path == "" or AME_file_path == "" or AME_file_path == "맞지 않는 버전의 프로그램 입니다.":
            return
        else:
            def show_confirmation_msgbox():
                # 기본 윈도우 생성
                root = tk.Tk()
                root.withdraw()  # 기본 윈도우 숨기기

                # 메시지 박스 표시
                messagebox.showinfo("확인 요청", "계정등록과 월구독 결제가 없어도 작동 합니다. \n\n 하지만 <상업적 사용은 불법>입니다. \n\n  미결제 사용에 대한 <책임은 지지 않습니다> \n\n 확인하셨습니까?")

                # GUI 앱 종료
                root.destroy()

            show_confirmation_msgbox()
        my_ip = module.get_my_ip_address()
        working_folder_name = my_ip+"_PC의_작업폴더"
        net_working_folder_path = os.path.join(input_folder_path,working_folder_name)
        finish_folder_path = os.path.join(input_folder_path,"작업완료(원본)_삭제해도됩니다")
        module.make_folder(input_folder_path,working_folder_name,False)
        module.make_folder(input_folder_path,"작업완료(원본)_삭제해도됩니다", False)
        ## make_folder(r'/Users/imsejin/Desktop/입', "new_folder",True) << 이미 폴더가 있을 시 "new_folder" 내부 파일들 모두 삭제
        # 조건 만족시 시행

        # 글로벌 변수 변경
        selected_resolution =  self.resolution_var.get()
        selected_audio_channel = self.channel_var.get()
        selected_still_time = self.still_time_var.get()


        # 버튼 비활성화
        self.input_btn.config(state=tk.DISABLED)
        self.output_btn.config(state=tk.DISABLED)
        self.ame_btn.config(state=tk.DISABLED)
        self.start_btn.config(state=tk.DISABLED)
        for rb in self.resolution_radio_buttons + self.channel_radio_buttons:
            rb.config(state=tk.DISABLED)

        # 콤보박스 비활성화
        self.still_time_combobox.config(state=tk.DISABLED)



        # 하단 "작동중" 글자
        print(f"선택된 해상도: {self.resolution_var.get()}, 오디오 채널: {self.channel_var.get()}, 스틸 시간: {self.still_time_var.get()}초")
        # self.status_label = tk.Label(root, text=f"광고제작기 작동 중 \n\n 해상도 : {self.resolution_var.get()} \n\n 오디오 채널 : {self.channel_var.get()} \n\n 스틸시간 : {self.still_time_var.get()}초 ", fg="red", font=("Arial", 15, "bold"))
        # self.status_label.pack(pady=10)
        self.status_label = tk.Label(root, text=f"광고제작기 작동 중", fg="red", font=("Arial", 15, "bold"))
        self.status_label.pack(pady=10)

        def long_running_task_1(input_folder_path,net_working_folder_path):
            while True:
                try:
                    global state_of_multi_1_exit, state_of_multi_2_exit, state_of_gui_exit

                    with state_data_lock:  # 공유 변수에만 락을 적용
                        state_of_multi_1_exit = 1
                        state_of_gui = state_of_gui_exit

                    if state_of_gui == 2:
                        with state_data_lock:  # 공유 변수에만 락을 적용
                            state_of_multi_1_exit = 2
                        return

                    # 작업 대상 파일의 조건이 까다로워 멀티 프로세싱을 통해 작업 조건을 만족하는 파일을 따로 파악한다.
                    # 이렇게 되면 메인 작업 도중에도 다음 파일의 조건을 확인 할 수 있으며
                    # 바로 다음 동영상 작업을 실시 할 수 있다.
                    my_ip = module.get_my_ip_address()
                    working_folder_name = my_ip + "_PC의_작업폴더"
                    net_working_folder_path = os.path.join(input_folder_path, working_folder_name)
                    finish_folder_path = os.path.join(input_folder_path, "작업완료(원본)_삭제해도됩니다")
                    module.make_folder(input_folder_path, working_folder_name, False)
                    module.make_folder(input_folder_path, "작업완료(원본)_삭제해도됩니다", False)

                    def count_files(directory, extensions):
                        """ 주어진 확장자를 가진 파일의 개수를 세는 함수 """
                        count = 0
                        for root, dirs, files in os.walk(directory):
                            for file in files:
                                if file.lower().endswith(tuple(extensions)):
                                    count += 1
                        return count

                    extensions = ['mov', 'mxf', 'mp4','avi','mkv']
                    file_count = count_files(net_working_folder_path, extensions)
                    input_folder_path_count = count_files(input_folder_path,extensions)
                    ## ip 폴더에 동영상이 몇개인지 확인한다. 2개 이상일 시 ip 폻더로의 이동작업을 하지 않는다. 여러대의 pc를 돌릴때를 대비하여 너무 많이 한 pc가 가져가지 않음

                    if int(input_folder_path_count) == 0:
                        print("작업할 파일이 없습니다. 100초를 쉬었다 다시 들여다 봅니다")
                        time.sleep(100)
                        continue

                    if int(file_count) >= 2:
                        print("이미 대상작업 파일이 충분합니다")
                        time.sleep(10)
                        continue
                    else:
                        moving_file_path=file_ready_checker.detect_folder_and_move_file(input_folder_path,net_working_folder_path,['mov', 'mxf', 'mp4','avi','mkv'])
                        # 또는 detect_folder_and_move_file"작업_폴더_경로", "이동_폴더_경로", ['mov', 'mp4']) - 확장자 명시도 가능
                        # input_path의 ip 작업폴더로 이동
                        ################## 이름오류로 인한 미실행을 막기위한 코드 추가 ########
                        def replace_spaces_with_underscores(folder_path, extensions):
                            for root, dirs, files in os.walk(folder_path):
                                for file in files:
                                    if any(file.endswith(ext) for ext in extensions):
                                        new_name = file.replace(' ', '_')
                                        new_name = new_name.replace('<', '_')
                                        new_name = new_name.replace('>', '_')
                                        new_name = new_name.replace(':', '_')
                                        new_name = new_name.replace('"', '_')
                                        new_name = new_name.replace('|', '_')
                                        new_name = new_name.replace('?', '_')
                                        new_name = new_name.replace('*', '_')
                                        if new_name != file:
                                            os.rename(os.path.join(root, file), os.path.join(root, new_name))
                                            print(f"Renamed '{file}' to '{new_name}'")

                        replace_spaces_with_underscores(net_working_folder_path, extensions)
                        ################## 이름오류로 인한 미실행을 막기위한 코드 추가 ########
                        print("이동이 끝났습니다.")
                        time.sleep(10)
                        continue
                except Exception as e:
                    # 10초간 대기
                    time.sleep(10)
                    # 오류 메시지 출력
                    print("오류가 발생했습니다 멀티 1 쉬었다가 다시 시작합니다.: ", e)
                    # 오류 후 재시도
                    continue


        def long_running_task_2(net_working_folder_path,finish_folder_path):
            while True:
                try:
                    global input_folder_path, output_folder_path, AME_file_path, selected_still_time, selected_resolution, selected_audio_channel, local_working_folder_path
                    global ffmpeg_path,ffprobe_path,ffplay_path
                    global state_of_multi_1_exit, state_of_multi_2_exit, state_of_gui_exit

                    with state_data_lock:  # 공유 변수에만 락을 적용
                        state_of_multi_2_exit = 1
                        state_of_gui = state_of_gui_exit

                    if state_of_gui == 2:
                        with state_data_lock:  # 공유 변수에만 락을 적용
                            state_of_multi_2_exit = 2
                        return
                    ## 이제 여기에 main 작업 때려 넣으면 됨

                    my_ip = module.get_my_ip_address()
                    working_folder_name = my_ip + "_PC의_작업폴더"
                    net_working_folder_path = os.path.join(input_folder_path, working_folder_name)
                    net_finish_folder_path = os.path.join(input_folder_path, "작업완료(원본)_삭제해도됩니다")
                    module.make_folder(input_folder_path, working_folder_name, False)
                    module.make_folder(input_folder_path, "작업완료(원본)_삭제해도됩니다", False)


                    don_t_erase_folder_in_finish_folder_name = "지우지마시오_"+my_ip
                    don_t_erase_folder_in_finish_folder_path = os.path.join(output_folder_path,don_t_erase_folder_in_finish_folder_name)
                    module.make_folder(os.path.dirname(don_t_erase_folder_in_finish_folder_path),don_t_erase_folder_in_finish_folder_name,True)
                    # 폴더를 만들고 이미 있다면 내부 파일을 삭제 합니다.

                    local_making_file_folder = os.path.join(local_working_folder_path,"making_folder")
                    video_temp_folder_in_local_making_file_folder = os.path.join(local_making_file_folder,"video_temp")
                    audio_temp_folder_in_local_making_file_folder = os.path.join(local_making_file_folder,"audio_temp")
                    finish_folder_in_local_making_file_folder = os.path.join(local_making_file_folder,"finish")

                    module.make_folder(local_working_folder_path,"making_folder",True)
                    module.make_folder(local_working_folder_path, "pre_check", True)
                    module.make_folder(local_making_file_folder, "video_temp", True)
                    module.make_folder(local_making_file_folder, "audio_temp", True)
                    module.make_folder(local_making_file_folder, "finish", True)


                    #### 필요한 폴더 생성 작업 끝#############################################

                    ### 메인 작업 ####
                    working_file_path = module.move_ip_file_to_local(net_working_folder_path, local_making_file_folder)


                    ## 파일을 로컬로 옮깁니다. 로컬 스토리지가 파일 크기보다 10배 이상 사용가능한 용량이 있어야 합니다.
                    ## 용량이 10배가 안되면 작업하지 않고 작업 불가 폴더로 옮기게 됩니다.

                    time.sleep(1)

                    if working_file_path == None:
                        # 1초에서 60초 사이의 무작위 시간을 생성
                        random_sleep_time = random.randint(1, 60)
                        # 생성된 시간만큼 대기
                        time.sleep(random_sleep_time)
                        continue

                    result_time = module.append_still_frame_to_end(working_file_path, video_temp_folder_in_local_making_file_folder, net_working_folder_path, ffmpeg_path, selected_resolution,selected_audio_channel, selected_still_time)
                    start_time = float(result_time[0])
                    end_time = float(result_time[1])
                    duration = float(result_time[1]) - float(result_time[0])
                    module.extract_and_split_audio_channels_with_ffmpeg(ffmpeg_path,working_file_path, audio_temp_folder_in_local_making_file_folder,start_time,duration )


                    module.rename_based_on_similarity(audio_temp_folder_in_local_making_file_folder, ffmpeg_path, threshold=0.90)

                    time.sleep(1)
                    net_ip_file_path = working_file_path
                    hq_result_path = module.combine_audio_and_video(video_temp_folder_in_local_making_file_folder, audio_temp_folder_in_local_making_file_folder, finish_folder_in_local_making_file_folder,net_ip_file_path, ffmpeg_path, selected_resolution,selected_audio_channel)
                    time.sleep(1)

                    exe_path = os.path.dirname(sys.executable)
                    folder_of_resolution = os.path.join(exe_path, "지우지마시오_프리셋저장소")

                    if selected_resolution == "HD" or selected_resolution == "hd":
                        if selected_audio_channel == "2ch" or selected_audio_channel == "2CH":
                            folder_of_HD_resolution = os.path.join(folder_of_resolution,"HD_프리셋_2CH")
                            # module.make_folder(folder_of_resolution,"HD_프리셋_2CH", False)
                            # .epr 확장자를 가진 모든 파일 경로를 가져옵니다.
                            epr_files = glob.glob(os.path.join(folder_of_HD_resolution, '*.epr'))

                            # 최신 파일을 찾기 위해 파일들을 수정 시간을 기준으로 정렬합니다.
                            epr_files.sort(key=os.path.getmtime, reverse=True)

                            # 최신 .epr 파일의 경로를 변수에 저장합니다.
                            if epr_files:
                                latest_epr_file = epr_files[0]
                                print("가장 최신의 .epr 파일 경로:", latest_epr_file)
                            else:
                                print(".epr 파일을 찾을 수 없습니다.")
                        if  selected_audio_channel == "8ch" or selected_audio_channel == "8CH":
                            folder_of_HD_resolution = os.path.join(folder_of_resolution, "HD_프리셋_8CH")
                            # module.make_folder(folder_of_resolution, "HD_프리셋_8CH", False)
                            # .epr 확장자를 가진 모든 파일 경로를 가져옵니다.
                            epr_files = glob.glob(os.path.join(folder_of_HD_resolution, '*.epr'))

                            # 최신 파일을 찾기 위해 파일들을 수정 시간을 기준으로 정렬합니다.
                            epr_files.sort(key=os.path.getmtime, reverse=True)

                            # 최신 .epr 파일의 경로를 변수에 저장합니다.
                            if epr_files:
                                latest_epr_file = epr_files[0]
                                print("가장 최신의 .epr 파일 경로:", latest_epr_file)
                            else:
                                print(".epr 파일을 찾을 수 없습니다.")
                    if selected_resolution == "UHD" or selected_resolution == "uhd":
                        if selected_audio_channel == "2ch" or selected_audio_channel == "2CH":
                            folder_of_UHD_resolution = os.path.join(folder_of_resolution,"UHD_프리셋_2CH")
                            # module.make_folder(folder_of_resolution,"UHD_프리셋_2CH", False)
                            # .epr 확장자를 가진 모든 파일 경로를 가져옵니다.
                            epr_files = glob.glob(os.path.join(folder_of_UHD_resolution, '*.epr'))

                            # 최신 파일을 찾기 위해 파일들을 수정 시간을 기준으로 정렬합니다.
                            epr_files.sort(key=os.path.getmtime, reverse=True)

                            # 최신 .epr 파일의 경로를 변수에 저장합니다.
                            if epr_files:
                                latest_epr_file = epr_files[0]
                                print("가장 최신의 .epr 파일 경로:", latest_epr_file)
                            else:
                                print(".epr 파일을 찾을 수 없습니다.")
                        if selected_audio_channel == "8ch" or selected_audio_channel == "8CH":
                            folder_of_UHD_resolution = os.path.join(folder_of_resolution,"UHD_프리셋_8CH")
                            # module.make_folder(folder_of_resolution,"UHD_프리셋_8CH", False)
                            # .epr 확장자를 가진 모든 파일 경로를 가져옵니다.
                            epr_files = glob.glob(os.path.join(folder_of_UHD_resolution, '*.epr'))

                            # 최신 파일을 찾기 위해 파일들을 수정 시간을 기준으로 정렬합니다.
                            epr_files.sort(key=os.path.getmtime, reverse=True)

                            # 최신 .epr 파일의 경로를 변수에 저장합니다.
                            if epr_files:
                                latest_epr_file = epr_files[0]
                                print("가장 최신의 .epr 파일 경로:", latest_epr_file)
                            else:
                                print(".epr 파일을 찾을 수 없습니다.")

                    ## jsx 파일 제작 및 생성
                    module.make_folder(local_working_folder_path, "pre_check", True)
                    pre_check_folder = os.path.join(local_working_folder_path, "pre_check")
                    base_name_of_hq_file =os.path.basename(hq_result_path)
                    base_name_of_hq_file = base_name_of_hq_file.split(".")[0]+".mxf"
                    result_mxf_file_path = os.path.join(pre_check_folder,base_name_of_hq_file)
                    status_of_making_process_txt_path = os.path.join(pre_check_folder, "status.txt")
                    jsx_file_path = os.path.join(pre_check_folder, "hq_to_mxf.jsx")
                    pid_save_path = os.path.join(pre_check_folder, "pid.txt")
                    lsj_jsx_module.make_jsx_file(hq_result_path, latest_epr_file, result_mxf_file_path,status_of_making_process_txt_path, jsx_file_path)
                    ame_working_in_cli(AME_file_path, jsx_file_path, pid_save_path)

                    time.sleep(2)

                    while True:
                        if os.path.exists(status_of_making_process_txt_path):
                            with open(status_of_making_process_txt_path, 'r', encoding='cp949') as file:
                                content = file.read().strip()
                                if content == "시작":
                                    print(content)
                                    if os.path.exists(result_mxf_file_path):
                                        try:
                                            with open(pid_save_path, 'r', encoding='cp949') as file:
                                                pid = int(file.read().strip())
                                            process = psutil.Process(pid)
                                            if process.is_running():  # ame가 돌아가고 있는지 확인
                                                pass
                                        except psutil.NoSuchProcess:
                                            raise  # ame가 꺼진것으로 보고 종료 합니다.
                                            return
                                if content == "실행완료":
                                    if os.path.exists(result_mxf_file_path):
                                        try:
                                            with open(pid_save_path, 'r', encoding='cp949') as file:
                                                pid = int(file.read().strip())
                                            process = psutil.Process(pid)
                                            if process.is_running():  # ame가 돌아가고 있는지 확인
                                                pass
                                        except psutil.NoSuchProcess:
                                            raise  # ame가 꺼진것으로 보고 종료 합니다.
                                            return

                                        xmp_file_folder_path =os.path.dirname(result_mxf_file_path)

                                        def find_xmp_files(folder_path):
                                            # 폴더 내의 모든 파일과 디렉토리 목록을 가져옵니다.
                                            files_and_directories = os.listdir(folder_path)

                                            # .xmp 확장자를 가진 파일만 필터링합니다.
                                            xmp_files = [file for file in files_and_directories if file.endswith('.xmp')]

                                            return xmp_files

                                        # .xmp 파일 목록을 찾아냅니다.
                                        xmp_files_found = find_xmp_files(xmp_file_folder_path)

                                        # 결과 출력
                                        if xmp_files_found:
                                            print("Found .xmp files을 찾았습니다. 작업이 완료 되었습니다.:", xmp_files_found)
                                            able_to_use = True
                                            break
                                        else:
                                            try:
                                                with open(pid_save_path, 'r', encoding='cp949') as file:
                                                    pid = int(file.read().strip())
                                                process = psutil.Process(pid)
                                                if process.is_running(): #ame가 돌아가고 있는지 확인
                                                    print("AME의 결과물 생성을 기다립니다.")
                                                    time.sleep(10)
                                                    continue
                                            except psutil.NoSuchProcess:
                                                raise # ame가 꺼진것으로 보고 종료 합니다.
                                                return
                                    else:
                                        able_to_use = False
                                        print("실행에 실패하였습니다.")
                                        break
                                if content == "실행실패":
                                    able_to_use = False
                                    print("실행에 실패하였습니다.")
                                    break
                        else:
                            print("상태 메모장 생성을 기다립니다.")
                        time.sleep(5)  # 5초 대기

                    with open(pid_save_path, 'r', encoding='cp949') as file:
                        pid = int(file.read().strip())

                    def terminate_process_by_pid(pid):
                        try:
                            # PID로 프로세스 객체를 가져옵니다.
                            process = psutil.Process(pid)
                            # 프로세스 종료
                            process.terminate()
                            return f"PID {pid} 프로세스가 종료되었습니다."
                        except psutil.NoSuchProcess:
                            return f"PID {pid}를 가진 프로세스가 존재하지 않습니다."
                        except psutil.AccessDenied:
                            return f"PID {pid} 프로세스를 종료할 권한이 없습니다."
                        except Exception as e:
                            return f"오류 발생: {e}"

                    print(terminate_process_by_pid(pid))

                    if content == "실행실패":
                        print("HQ에서 mxf 제작에 실패했습니다")
                        raise
                    print("모든 작업을 마쳤습니다.")
                    time.sleep(1)
                    try:
                        os.mkdir(don_t_erase_folder_in_finish_folder_path)
                    except:
                        pass
                    shutil.move(result_mxf_file_path,don_t_erase_folder_in_finish_folder_path)
                    ip_finish_folder_file_path = os.path.join(don_t_erase_folder_in_finish_folder_path,os.path.basename(result_mxf_file_path))
                    #output_folder의 ip 주소 안에 있는 파일 경로

                    finish_folder_path = os.path.dirname(don_t_erase_folder_in_finish_folder_path)
                    ## output 폴더 경로

                    def name_change(folder_path, full_file_path):
                        # full_file_path에서 파일 이름과 확장자 분리
                        base_name = os.path.basename(full_file_path)
                        name, ext = os.path.splitext(base_name)

                        # "(중복이름있음)_" 제거
                        while name.startswith("(중복이름있음)_"):
                            name = name[len("(중복이름있음)_"):]

                        # 중복 확인 및 이름 변경
                        new_name = name
                        count = 1
                        while True:
                            is_duplicate = False
                            for root, dirs, files in os.walk(folder_path):
                                for file in files:
                                    current_file_path = os.path.join(root, file)

                                    # 현재 파일이 full_file_path와 같으면 건너뛰기
                                    if current_file_path == full_file_path:
                                        continue

                                    if file == base_name:
                                        is_duplicate = True
                                        break

                                if is_duplicate:
                                    break

                            if not is_duplicate:
                                break

                            # 중복되는 경우 새 이름 생성
                            new_name = f"(중복이름있음)_{count}_{name}"
                            base_name = new_name + ext
                            count += 1

                        return base_name  # 새로운 파일 이름(확장자 포함) 반환

                    last_file_full_path = os.path.join(finish_folder_path,name_change(finish_folder_path, ip_finish_folder_file_path))
                    shutil.move(ip_finish_folder_file_path,last_file_full_path)


                    # finish_folder_file_path =os.path.join(finish_folder_path,os.path.basename(ip_finish_folder_file_path))

                    ##### nas의 ip 작업 폴더에 있던 파일을 _작업 완료 폴더로 옴겨야 한다.
                    net_ip_file_path = os.path.join(net_working_folder_path, os.path.basename(working_file_path))
                    base_name = name_change(os.path.dirname(net_working_folder_path),net_ip_file_path)

                    net_finish_file_full_path = os.path.join(net_finish_folder_path,base_name)

                    print("마지막 처리 입니다")

                    shutil.move(net_ip_file_path,net_finish_file_full_path)
                    def count_files(directory, extensions):
                        """ 주어진 확장자를 가진 파일의 개수를 세는 함수 """
                        count = 0
                        for root, dirs, files in os.walk(directory):
                            for file in files:
                                if file.lower().endswith(tuple(extensions)):
                                    count += 1
                        return count

                    extensions = ['mov', 'mxf', 'mp4','avi','mkv']
                    input_folder_path_count = count_files(input_folder_path,extensions)
                    if int(input_folder_path_count) == 0:
                        time.sleep(100)
                    continue
                except Exception as e:
                    # 오류 메시지 출력
                    print("오류가 발생했습니다 멀티 2 쉬었다가 다시 시작합니다.: ", e)
                    time.sleep(5)
                    continue


        ####################################################################################################################################
        thread_1 = threading.Thread(target=long_running_task_1,args=(input_folder_path,net_working_folder_path))
        thread_1.start()

        thread_2 = threading.Thread(target=long_running_task_2,args=(net_working_folder_path,finish_folder_path))
        thread_2.start()




if __name__ == "__main__":

    if want_know_korea_word_in_path():
        new_window = tk.Tk()
        new_window.title("작동 불가")

        def do_nothing():
            pass

        def actions_after_timeout():
            new_window.destroy()
            sys.exit()


        current_dir = os.path.dirname(sys.executable)
        current_dir = os.path.dirname(current_dir)

        new_window.protocol("WM_DELETE_WINDOW", do_nothing)

        tk.Label(new_window,
                 text=f"\n\n---------------<작동 불가>---------------\n\n실행파일 경로 : {current_dir}\n\n\n 실행파일의 경로에 한글이 있으면 작동하지 않습니다. \n\n 15초 후 자동으로 닫힙니다.\n\n",
                 fg="black",
                 font=("Arial", 12, "bold")).pack()
        # 5초 후 창 닫기
        new_window.after(12000, actions_after_timeout)

    elif ffmpeg_path == None or ffprobe_path == None:
        new_window = tk.Tk()
        new_window.title("작동 불가")


        def do_nothing():
            pass


        def actions_after_timeout():
            new_window.destroy()
            sys.exit()


        current_dir = os.path.dirname(sys.executable)
        current_dir = os.path.dirname(current_dir)

        new_window.protocol("WM_DELETE_WINDOW", do_nothing)

        tk.Label(new_window,
                 text=f"\n\n---------------<작동 불가>---------------\n\n ffmpeg 위치를 찾지 못했습니다.\n\n 폴더 압축 해제 후 파일을 이동하지 말고 그대로 사용하세요 \n\n 10초 후 자동으로 닫힙니다.\n\n",
                 fg="black",
                 font=("Arial", 12, "bold")).pack()
        # 5초 후 창 닫기
        new_window.after(10000, actions_after_timeout)

    else:
        current_dir = os.path.dirname(sys.executable)
        current_dir = os.path.dirname(current_dir) #한 폴더 위로 올라갔습니다.
        local_working_folder_path = os.path.join(current_dir,"don_t_erase_working_folder")
        try:
            module.make_folder(current_dir, "don_t_erase_working_folder", True)
        except:
            pass


    root = tk.Tk()
    app = App(root)
    root.mainloop()




