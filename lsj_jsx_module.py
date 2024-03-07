
from PIL import ImageGrab

def make_jsx_file(input_video_path, preset_epr_path, output_load_of_video_path, status_txt_path, making_jsx_path):

    input_video_path = input_video_path.replace("\\", "\\\\")
    preset_epr_path = preset_epr_path.replace("\\", "\\\\")
    output_load_of_video_path = output_load_of_video_path.replace("\\", "\\\\")
    status_txt_path = status_txt_path.replace("\\", "\\\\")

    jsx_content = f"""
var input_video_path = "{input_video_path}";
var preset_epr_path = "{preset_epr_path}";
var output_load_of_video_folder_path = "{output_load_of_video_path}";
var status_txt_path = "{status_txt_path}";

var watchFolderObj = app.getWatchFolder();
if (watchFolderObj) {{
  watchFolderObj.removeAllWatchFolders();
}} else {{
  $.writeln("Watch folder object is not valid");
}}

var exporter = app.getExporter(); // Adobe 애플리케이션에서 내보내기 기능을 제어하는 객체를 가져옵니다. $.sleep(10000); // 10,000 밀리초 == 10초

// 'status.txt' 파일에 "시작"을 기록합니다.
var statusFile = new File(status_txt_path);
statusFile.open("w"); // 쓰기 모드로 파일을 엽니다.
statusFile.writeln("시작");
statusFile.close();

if (exporter) {{
    exporter.removeAllBatchItems();

    var encoderWrapper  = exporter.exportItem(input_video_path, output_load_of_video_folder_path, preset_epr_path); // 지정된 소스 파일을 대상 경로로 내보내기 시작합니다.

    exporter.addEventListener("onEncodeComplete", function(eventObj) {{
        // 변환 작업이 완료되었을 때 호출될 이벤트 리스너입니다.
        statusFile.open("w"); // 쓰기 모드로 파일을 엽니다.
        statusFile.writeln("실행완료");
        statusFile.close();
    }}, false);

    exporter.addEventListener("onError", function(eventObj) {{
        // 변환 중 오류가 발생했을 때 호출될 이벤트 리스너입니다.
        statusFile.open("w"); // 쓰기 모드로 파일을 엽니다.
        statusFile.writeln("실행실패");
        statusFile.close();
    }}, false);
}}
"""
    with open(making_jsx_path, 'w', encoding='utf-8') as file:
        file.write(jsx_content)
    return




def screenshot_and_save(save_path):
    # 스크린샷 찍기
    screenshot = ImageGrab.grab()
    # 스크린샷을 JPG 형식으로 저장
    screenshot.save(save_path, "JPEG")

# 함수 사용 예시

