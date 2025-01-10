import cv2
import time

def main():
    rtsp_url = "rtsp://root:root@192.168.0.90/axis-media/media.amp?videocodec=mjpeg&compression=0"
    
    gst_pipeline = (
        f"rtspsrc location={rtsp_url} ! "
        "rtpjpegdepay ! "
        "jpegdec ! "
        "videoconvert ! "
        "appsink"
    )

    cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)
    if not cap.isOpened():
        print("Не удалось открыть поток.")
        return

    cv2.namedWindow("Axis MJPEG", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Axis MJPEG", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Для подсчёта FPS
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
        elapsed = current_time - prev_time
        if elapsed >= 1.0:
            fps = frame_count / elapsed
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

        cv2.imshow("Axis MJPEG", frame)

        # Выход по нажатию 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
