import cv2
import threading
import time
import os
import sys

# -----------------------------------------------------------------------------
# Класс, который в фоновом потоке захватывает кадры с камеры
# -----------------------------------------------------------------------------
class CameraReader:
    def __init__(self, rtsp_url, backend=cv2.CAP_FFMPEG):
        self.rtsp_url = rtsp_url
        self.backend = backend
        self.capture = None
        self.ret = False
        self.frame = None
        self.running = False
        self.thread = None

    def start(self):
        """Запуск фонового потока чтения кадров"""
        self.capture = cv2.VideoCapture(self.rtsp_url, self.backend)
        if not self.capture.isOpened():
            print("Не удалось открыть RTSP-поток.")
            return False

        self.running = True
        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start()
        return True

    def update(self):
        """Фоновый цикл чтения кадров"""
        while self.running:
            ret, frame = self.capture.read()
            if not ret:
                # Если вдруг поток отвалился, можно сделать небольшую паузу
                time.sleep(0.01)
                continue
            self.ret = ret
            self.frame = frame

    def stop(self):
        """Остановка чтения и освобождение ресурсов"""
        self.running = False
        if self.thread is not None:
            self.thread.join()
        if self.capture is not None:
            self.capture.release()

# -----------------------------------------------------------------------------
# Основная функция
# -----------------------------------------------------------------------------
def main():
    # Попытка поднять приоритет процесса (на Linux обычно работает, на Windows - может потребовать доп. инструментов)
    try:
        if sys.platform.startswith('linux'):
            # Уменьшаем nice-значение, чтобы повысить приоритет (минимум -20)
            os.nice(-10)  # или -15, -19 и т.д.
        elif sys.platform.startswith('win'):
            # Для Windows проще запустить скрипт с повышенным приоритетом в самом окружении
            print("Чтобы повысить приоритет в Windows, запустите скрипт от имени администратора или используйте psutil.")
    except Exception as e:
        print(f"Не удалось изменить приоритет: {e}")

    rtsp_url = "rtsp://root:root@192.168.0.90/axis-media/media.amp?compression=0"
    
    # Создаём объект фонового чтения
    camera = CameraReader(rtsp_url)

    if not camera.start():
        # Если поток не открылся, выходим
        return

    # Создаём окно и делаем его полноэкранным
    cv2.namedWindow("Axis", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Axis", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        # Берём кадр, который уже прочитан фоновым потоком
        frame = camera.frame

        if frame is not None:
            cv2.imshow("Axis", frame)

        # Закрытие по кнопке 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Останавливаем поток и освобождаем ресурсы
    camera.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
