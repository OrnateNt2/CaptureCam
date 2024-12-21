import cv2

def main():
    # Укажем RTSP-URL с учётом логина и пароля
    rtsp_url = "rtsp://admin:admin@192.168.0.90/axis-media/media.amp"

    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print("Не удалось открыть RTSP-поток.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Ошибка чтения кадра.")
            break

        # Переводим в ч/б, чтобы удобнее найти самое яркое место
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Находим мин/макс значения яркости и их координаты
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(gray)
        # maxLoc вернёт (x, y) самого яркого пикселя

        # Размер «квадратика», который хотим нарисовать
        size = 20  
        x, y = maxLoc
        
        # Рисуем красный прямоугольник вокруг самой яркой точки
        # Левая верхняя точка: (x - size, y - size)
        # Правая нижняя точка: (x + size, y + size)
        cv2.rectangle(frame, (x - size, y - size), (x + size, y + size),
                      (0, 0, 255), 2)

        # Выводим кадр с выделенным пятном
        cv2.imshow("Axis RTSP Stream - Brightest Spot", frame)

        # Выход по нажатию клавиши 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
