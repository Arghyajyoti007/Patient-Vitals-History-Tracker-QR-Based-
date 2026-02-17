import cv2


def scan_qr():
    cap = cv2.VideoCapture(0)
    # OpenCV's built-in QR detector (No extra DLLs needed!)
    detector = cv2.QRCodeDetector()

    print("Scanning for Patient QR...")
    while True:
        _, frame = cap.read()
        # data is the decoded text, bbox is the location
        data, bbox, _ = detector.detectAndDecode(frame)

        if data:
            print(f"QR Found: {data}")
            cap.release()
            cv2.destroyAllWindows()
            return data

        cv2.imshow("Hospital Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break