import time
import psutil
import requests

def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    response = requests.post(url, data=data)
    return response.json()

def is_process_running(process_name):
    """프로세스가 실행 중인지 확인"""
    for process in psutil.process_iter(attrs=['name']):
        if process.info['name'] == process_name:
            return True
    return False

def monitor_processes(target_processes, token, chat_id, check_interval=5):
    """여러 프로세스를 감시하고 종료되면 메시지 전송"""
    print(f"Monitoring processes: {', '.join(target_processes)}")
    running_processes = set(target_processes)
    
    while running_processes:
        for process in list(running_processes):
            if not is_process_running(process):
                message = f"⚠️ {process} 프로세스가 종료되었습니다!"
                send_telegram_message(token, chat_id, message)
                print(f"Message sent to Telegram: {process} has stopped.")
                running_processes.remove(process)
        time.sleep(check_interval)

if __name__ == "__main__":
    TELEGRAM_BOT_TOKEN = "8066368285:AAF8bxqmYWE2-hX6fgxPpYZIYz1sep5nDcc"
    TELEGRAM_CHAT_ID = "6661552092"
    PROCESS_NAMES = ["bithumb.exe", "upbit.exe"]  # 감시할 프로그램 목록
    
    monitor_processes(PROCESS_NAMES, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)