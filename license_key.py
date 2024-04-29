import datetime
import hashlib
import sys
import uuid
import os
def License(txt_address,overdate,secrete_key):
    def get_mac_address():
        mac = uuid.getnode()
        mac_address = ''.join(('%012X' % mac)[i:i + 2] for i in range(0, 12, 2))
        return mac_address

    target_date = datetime.datetime.strptime(overdate, "%Y-%m-%d")

    # 현재 날짜와 시간 가져오기
    now = datetime.datetime.now()

    # 날짜 비교
    if target_date < now:
        # print("입력한 날짜는 미래입니다.")
        print('라이센스 확인 중')
        with open(txt_address, 'r+', encoding='utf-8') as file:
            file.seek(0)
            # 파일 내용 읽기
            content = file.read()
            mac_add=get_mac_address()
            input_string =str(mac_add)+str(secrete_key)
            # hashlib을 사용하여 sha256 해시 객체 생성
            hash_object = hashlib.sha256()
            # 입력 문자열을 바이트로 변환하고 해시
            hash_object.update(input_string.encode())
            # 해시 결과를 16진수 형식의 문자열로 변환
            hex_dig = hash_object.hexdigest()
            if str(content) == str(hex_dig)+str(secrete_key):
                print("라이센스 일치 진행합니다")
                return True
            else:
                print("라이센스가 맞지않아 종료합니다.")
                return False

    else:
        try:
            with open(txt_address, 'r+', encoding='utf-8') as file:
                pass
        except:
            with open(txt_address, 'w+', encoding='utf-8') as file:
                pass
            os.system(f'attrib +h "{txt_address}"') ## 파일 숨김 처리

        with open(txt_address, 'r+', encoding='utf-8') as file:
            file.seek(0)
            # 파일 내용 읽기
            content = file.read()
            if str(content)[-4:] == "0446":
                print('라이센스 확인 중')
                mac_add=get_mac_address()
                input_string =str(mac_add)+str(secrete_key)
                # hashlib을 사용하여 sha256 해시 객체 생성
                hash_object = hashlib.sha256()
                # 입력 문자열을 바이트로 변환하고 해시
                hash_object.update(input_string.encode())
                # 해시 결과를 16진수 형식의 문자열로 변환
                hex_dig = hash_object.hexdigest()
                if str(content) == str(hex_dig)+str(secrete_key):
                    return True
                else:
                    print("라이센스가 맞지않아 종료합니다.")
                    return False
            else:
                print('라이센스 생성중 ')
                mac_add=get_mac_address()
                input_string =str(mac_add)+str(secrete_key)
                # hashlib을 사용하여 sha256 해시 객체 생성
                hash_object = hashlib.sha256()
                # 입력 문자열을 바이트로 변환하고 해시
                hash_object.update(input_string.encode())
                # 해시 결과를 16진수 형식의 문자열로 변환
                hex_dig = str(hash_object.hexdigest())+str(secrete_key)
                file.write(hex_dig)
                return True


check_license =License("abc.txt","2024-08-06","0446")

print(check_license)