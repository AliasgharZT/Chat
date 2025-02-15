import socket
import threading

# لیستی برای نگهداری اتصالات کلاینت‌ها
clients = []
 
def handle_client(client_socket, addr):
    print(f"Connection from {addr} has been established.")
    clients.append(client_socket)  # اضافه کردن کلاینت به لیست
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')  # دریافت پیام
            if not message:
                break
            print(f"Received from {addr}: {message}")
            # ارسال پیام به تمام کلاینت‌های دیگر
            broadcast_message(f"{addr}: {message}", client_socket)
        except:
            break
    # حذف کلاینت از لیست در صورت قطع اتصال
    clients.remove(client_socket)
    client_socket.close() 

def broadcast_message(message, sender_socket):
    for client in clients:
        if client != sender_socket:  # پیام به فرستنده ارسال نشود
            try:
                client.sendall(message.encode('utf-8'))
            except:
                pass  

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))  # تنظیم آدرس و پورت
    server.listen(5) 
    print("Server is listening... (type 'exit' to stop)")

    # ترد جداگانه برای پذیرش اتصالات کلاینت‌ها
    def accept_clients():
        while True:
            try:
                client_socket, addr = server.accept()
                client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
                client_thread.start()
            except:
                break 

    # اجرای ترد پذیرش کلاینت‌ها
    accept_thread = threading.Thread(target=accept_clients, daemon=True)
    accept_thread.start()

    # حلقه مدیریت سرور برای بررسی دستور خروج
    try:
        while True:
            cmd = input()
            if cmd.lower() == "exit":
                print("Shutting down server...")
                server.close()
                break
    except KeyboardInterrupt:
        print("\nServer is shutting down...")
        server.close()

if __name__ == "__main__":
    main()
