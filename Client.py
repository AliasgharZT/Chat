
import socket
import threading

def receive_messages(sock):
    while True: 
        try:
            # دریافت پیام از سرور
            message = sock.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except: 
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))  # اتصال به سرور (آدرس IP و پورت را تنظیم کنید)

    # اجرای ترد برای دریافت پیام‌ها
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start() 

    print("Connected to the server. You can start sending messages.")
    while True:
        message = input()  # دریافت ورودی از کاربر
        client.sendall(message.encode('utf-8'))  # ارسال پیام به سرور

if __name__ == "__main__":
    main()

