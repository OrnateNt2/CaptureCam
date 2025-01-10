import cv2
import time

def main():
    rtsp_url = "rtsp://root:root@192.168.0.90/axis-media/media.amp?compression=100"

    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print("Не удалось открыть RTSP")
        return

    cv2.namedWindow("Axis RTSP Stream", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Axis RTSP Stream", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    prev_time = time.time()
    frame_count = 0
    fps = 0.0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Ошибка чтения кадра.")
            break

        frame_count += 1
        current_time = time.time()
        elapsed_time = current_time - prev_time
        if elapsed_time >= 1.0:
            fps = frame_count / elapsed_time
            frame_count = 0
            prev_time = current_time

        cv2.putText(
            frame, 
            f"FPS: {fps:.2f}", 
            (10, 30), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            1.0, 
            (0, 255, 0), 
            2
        )

        cv2.imshow("Axis RTSP Stream", frame)

        # Нажмите 'q', чтобы выйти
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
