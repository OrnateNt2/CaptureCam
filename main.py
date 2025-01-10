import requests
import cv2
import numpy as np

def get_snapshot(ip="192.168.0.90", user="root", password="root"):
    url = f"http://{ip}/axis-cgi/jpg/image.cgi"

    resp = requests.get(url, auth=(user, password), timeout=5)
    resp.raise_for_status()  #  исключение, если статус не 200

    arr = np.frombuffer(resp.content, dtype=np.uint8)
    frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    return frame

def main():
    frame = get_snapshot(ip="192.168.0.90", user="admin", password="admin")

    if frame is None:
        print("Не удалось получить изображение.")
        return

    cv2.imshow("Axis", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
#pip install requests opencv-python

