import cv2

def main():
    rtsp_url = "rtsp://root:root@192.168.0.90/axis-media/media.amp"

    cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)

    if not cap.isOpened():
        print("Не удалось открыть RTSP-поток.")
        return

    cv2.namedWindow("Axis", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Axis", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Ошибка чтения кадра.")
            break

        cv2.imshow("Axis", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
