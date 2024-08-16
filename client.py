import cv2

# url = "rtsp://807e9439d5ca.entrypoint.cloud.wowza.com:1935/app-rC94792j/068b9c9a_stream2"
# url = "rtsp://localhost:8554/test"
url = "rtsp://172.23.24.52:8554/test"
# url = "rtsp://172.23.24.130/ch1/stream1"
cap = cv2.VideoCapture(url)
if not cap.isOpened():
    print("Cannot open RTSP stream.")
    exit()

cv2.namedWindow('RTSP Stream', cv2.WINDOW_NORMAL)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Cannot receive frame (stream end?). Exiting ...")
        break

    cv2.imshow('RTSP Stream', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
