import ssl
import socket

# 확인하려는 서버의 호스트명
hostname = 'apis.data.go.kr'
port = 443

try:
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            # 연결에 사용된 TLS 버전 출력
            print(f"사용 중인 TLS 버전: {ssock.version()}")

except Exception as e:
    print(f"연결 오류 발생: {e}")