import cv2
import threading
import time
import os
import sys

class CameraReader:
    def __init__(self, rtsp_url, backend=cv2.CAP_FFMPEG):
        self.rtsp_url = rtsp_url
        self.backend = backend
        self.capture = None

        self.ret = False
        self.frame = None

        self.running = False
        self.thread = None

        # Для статистики
        self.frame_count = 0
        self.last_time = 0.0
        self.fps = 0.0

    def start(self):
        self.capture = cv2.VideoCapture(self.rtsp_url, self.backend)
        if not self.capture.isOpened():
            print("Не удалось открыть RTSP-поток")
            return False

        # Читаем информацию о текущих параметрах (если доступно)
        width  = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps    = self.capture.get(cv2.CAP_PROP_FPS)
        print(f"Открыт поток (Ш x В = {width} x {height}, FPS={fps:.2f})")

        self.running = True
        self.thread = threading.Thread(target=self._update_loop, daemon=True)
        self.thread.start()
        return True

    def _update_loop(self):
        self.last_time = time.time()
        
        while self.running:
            ret, frame = self.capture.read()
            if not ret:
                # Если не прочитали кадр, делаем небольшую паузу
                time.sleep(0.01)
                continue

            self.ret = ret
            self.frame = frame
            
            # Считаем FPS примерно раз в секунду
            self.frame_count += 1
            current_time = time.time()
            elapsed = current_time - self.last_time

            if elapsed >= 1.0:
                self.fps = self.frame_count / elapsed
                self.frame_count = 0
                self.last_time = current_time

        # Когда выходим из цикла
        self.capture.release()

    def stop(self):
        self.running = False
        if self.thread is not None:
            self.thread.join()

    def get_frame(self):
        """
        Возвращаем последний прочитанный кадр и флаг успешности.
        """
        return self.ret, self.frame

    def get_fps(self):
        return self.fps


def main():
    try:
        if sys.platform.startswith('linux'):
            os.nice(-10)  
        else:
            print("Изменение приоритета поддерживается только на Linux (по умолчанию).")
    except Exception as e:
        print(f"Не удалось изменить приоритет: {e}")

    rtsp_url = "rtsp://root:root@192.168.0.90/axis-media/media.amp?compression=0"
    # rtsp_url = "rtspsrc location=rtsp://root:root@192.168.0.90/axis-media/media.amp?compression=0 ! decodebin ! videoconvert ! appsink"

    camera = CameraReader(rtsp_url, backend=cv2.CAP_FFMPEG)
    # Для GStreamer можно попробовать: backend=cv2.CAP_GSTREAMER

    if not camera.start():
        return

    cv2.namedWindow("Axis", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Axis", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    prev_frame_time = time.time()

    while True:
        ret, frame = camera.get_frame()
        current_fps = camera.get_fps()

        if ret and frame is not None:
            current_time = time.time()
            delay_ms = (current_time - prev_frame_time) * 1000.0
            prev_frame_time = current_time

            stats_text = (
                f"Camera FPS: {current_fps:.2f} | "
                f"Display Delay: {delay_ms:.2f} ms"
            )
            cv2.putText(frame, stats_text, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0), 2)

            cv2.imshow("Axis", frame)

        # Нажмите 'q' для выхода
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
