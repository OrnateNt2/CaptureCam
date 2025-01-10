import cv2

def main():
    rtsp_url = "rtsp://root:root@192.168.0.90/axis-media/media.amp"

    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print("Не удалось открыть RTSP-поток.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Ошибка чтения кадра.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(gray)
        size = 20  
        x, y = maxLoc
        
        cv2.rectangle(frame, (x - size, y - size), (x + size, y + size),
                      (0, 0, 255), 2)

        cv2.imshow("Axis", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
