import cv2
import mediapipe as mp
import pyautogui

# Inisialisasi kamera dan model deteksi tangan
cam = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

# Ukuran layar
screen_width, screen_height = pyautogui.size()

index_y = 0

while True:
    # Baca frame dari kamera
    ret, frame = cam.read()
    if not ret:
        break

    # Balikkan frame untuk tampilan cermin
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape

    # Ubah frame ke format RGB
    color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(color)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            # Gambar landmark pada tangan
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark

            for id, landmark in enumerate(landmarks):
                x, y = int(landmark.x * frame_width), int(landmark.y * frame_height)
                if id == 8:  # Indeks jari telunjuk
                    # Gambar lingkaran pada jari telunjuk
                    cv2.circle(frame, (x, y), 10, (0, 255, 255), cv2.FILLED)

                    # Hitung posisi kursor pada layar
                    index_x = int(screen_width * x / frame_width)
                    index_y = int(screen_height * y / frame_height)
                    
                    # Pindahkan kursor ke posisi yang dihitung
                    pyautogui.moveTo(index_x, index_y)

                if id == 4:  # Indeks jari jempol
                    # Gambar lingkaran pada jari jempol
                    cv2.circle(frame, (x, y), 10, (0, 255, 255), cv2.FILLED)

                    # Hitung posisi kursor pada layar
                    thumb_x = int(screen_width * x / frame_width)
                    thumb_y = int(screen_height * y / frame_height)

                    if abs(index_y - thumb_y) < 30:
                        print('click')
                        pyautogui.click()

    # Tampilkan frame
    cv2.imshow('Frame', frame)

    # Keluar dari loop saat tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Bersihkan dan tutup
cam.release()
cv2.destroyAllWindows()