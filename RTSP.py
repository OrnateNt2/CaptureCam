import cv2

def main():
    rtsp_url = "rtsp://admin:admin@192.168.0.90/axis-media/media.amp"

    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print("Не удалось открыть RTSP")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Ошибка чтения")
            break

        cv2.imshow("Axis RTSP Stream", frame)

        #  'q', чтобы выйти из цикла
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
#pip install opencv-python
