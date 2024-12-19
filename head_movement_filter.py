import cv2
import mediapipe as mp
import time
import numpy as np

# Inisialisasi Mediapipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh

# Posisi dan opsi yang akan dipilih (formasi 4-3-3)
positions = [
    {"name": "GK", "options": ["A", "B"]},
    {"name": "LB", "options": ["C", "D"]},
    {"name": "LCB", "options": ["E", "F"]},
    {"name": "RCB", "options": ["G", "H"]},
    {"name": "RB", "options": ["I", "J"]},
    {"name": "CMF1", "options": ["K", "L"]},
    {"name": "DMF", "options": ["M", "N"]},
    {"name": "CMF2", "options": ["O", "P"]},
    {"name": "LWF", "options": ["Q", "R"]},
    {"name": "CF", "options": ["S", "T"]},
    {"name": "RWF", "options": ["U", "V"]}
]

# Player data and dummy images for testing
player_images = {
    "gk1": cv2.imread("gk1.png"),
    "gk2": cv2.imread("gk2.png"),
    "gk3": cv2.imread("gk3.png"),
    "gk4": cv2.imread("gk4.png"),
    "lb1": cv2.imread("lb1.png"),
    "lb2": cv2.imread("lb2.png"),
    "lb3": cv2.imread("lb3.png"),
    "lb4": cv2.imread("lb4.png"),
    "lcb1": cv2.imread("cb1.png"),
    "lcb2": cv2.imread("cb2.png"),
    "lcb3": cv2.imread("cb3.png"),
    "lcb4": cv2.imread("cb4.png"),
    "rcb1": cv2.imread("cb5.png"),
    "rcb2": cv2.imread("cb6.png"),
    "rcb3": cv2.imread("cb7.png"),
    "rcb4": cv2.imread("cb8.png"),
    "rb1": cv2.imread("rb1.png"),
    "rb2": cv2.imread("rb2.png"),
    "rb3": cv2.imread("rb3.png"),
    "rb4": cv2.imread("rb4.png"),
    "cmf1": cv2.imread("cm1.png"),
    "cmf2": cv2.imread("cm2.png"),
    "cmf3": cv2.imread("cm3.png"),
    "cmf4": cv2.imread("cm4.png"),
    "dmf1": cv2.imread("dm1.png"),
    "dmf2": cv2.imread("dm2.png"),
    "dmf3": cv2.imread("dm3.png"),
    "dmf4": cv2.imread("dm4.png"),
    "lwf1": cv2.imread("lw1.png"),
    "lwf2": cv2.imread("lw1.png"),
    "lwf3": cv2.imread("lw1.png"),
    "lwf4": cv2.imread("lw1.png"),
    "cf1": cv2.imread("cf1.png"),
    "cf2": cv2.imread("f2.png"),
    "cf3": cv2.imread("cf3.png"),
    "cf4": cv2.imread("cf4.png"),
    "rwf1": cv2.imread("rw1.png"),
    "rwf2": cv2.imread("rw2.png"),
    "rwf3": cv2.imread("rw3.png"),
    "rwf4": cv2.imread("rw4.png")
}

# Fungsi untuk mengubah ukuran gambar
def resize_image(image, width):
    aspect_ratio = image.shape[1] / image.shape[0]  # Rasio aspek (lebar/tinggi)
    height = int(width / aspect_ratio)  # Hitung tinggi berdasarkan lebar
    resized_image = cv2.resize(image, (width, height))
    return resized_image

# Fungsi untuk menghitung sudut kepala
def calculate_head_angle(nose_tip, face_center_x):
    delta_x = nose_tip.x - face_center_x
    return delta_x * 200  # Scaling sensitivitas lebih kecil untuk respons lebih cepat

# Fungsi untuk menampilkan hasil di lapangan sesuai formasi 4-3-3
def create_field_with_players(selected_players, frame):
    field_color = (34, 139, 34)  # Warna hijau lapangan
    frame_height, frame_width, _ = frame.shape

    # Koordinat posisi pemain di lapangan sesuai formasi yang diminta
    positions_coords = [
        (frame_width // 2, 100),  # LB (Kiri atas)
        (100, 150), (frame_width - 100, 150),  # LW dan RW
        (frame_width // 2, 200),  # CMF1
        (100, 250),  # LCB
        (frame_width // 4, 350), (frame_width // 2, 350), (frame_width // 4 * 3, 350),  # GK, DMF, CF
        (100, 450),  # RCB
        (frame_width // 2, 500),  # CMF2
        (100, 550), (frame_width - 100, 550)  # RB dan RW
    ]

    # Menampilkan gambar pemain sesuai posisi dalam formasi
    for i, player in enumerate(selected_players):
        if i < len(positions_coords):  # Pastikan tidak melebihi koordinat yang tersedia
            x, y = positions_coords[i]

            # Tampilkan gambar pemain jika tersedia
            if player in player_images and player_images[player] is not None:
                player_img = player_images[player]
                resized_img = resize_image(player_img, 50)  # Atur lebar menjadi 80 piksel
                img_h, img_w, _ = resized_img.shape

                # Periksa apakah gambar bisa muat di dalam frame
                if y - img_h // 2 >= 0 and y + img_h // 2 <= frame_height and x - img_w // 2 >= 0 and x + img_w // 2 <= frame_width:
                    y_offset = y - img_h // 2
                    x_offset = x - img_w // 2
                    frame[y_offset:y_offset + img_h, x_offset:x_offset + img_w] = resized_img

            # Tampilkan nama pemain sesuai posisinya (misal: GK, LB, CF, dll.)
            cv2.putText(frame, player, (x - 30, y + 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    return frame

# Fungsi untuk menampilkan gambar pada frame
def overlay_image(background, overlay, position):
    if overlay is None:
        return background

    x, y = position
    h, w, _ = overlay.shape
    if y + h > background.shape[0] or x + w > background.shape[1]:
        return background  # Jangan menampilkan jika keluar dari frame

    alpha_overlay = overlay[:, :, 3] / 255.0 if overlay.shape[-1] == 4 else None
    if alpha_overlay is not None:
        for c in range(0, 3):
            background[y:y + h, x:x + w, c] = (
                alpha_overlay * overlay[:, :, c] +
                (1 - alpha_overlay) * background[y:y + h, x:x + w, c]
            )
    else:
        background[y:y + h, x:x + w] = overlay

    return background

# Fungsi utama
def main():
    cap = cv2.VideoCapture(0)
    selected_players = []
    current_position_index = 0
    debounce_time = 1.0  # Waktu debounce dalam detik (dikurangi)
    cooldown_time = 0.5  # Waktu cooldown tambahan setelah pemilihan (dikurangi)
    last_selection_time = time.time()

    stability_threshold = 5  # Jumlah frame yang stabil untuk konfirmasi
    stable_count = 0  # Hitungan stabilitas arah

    previous_angle_direction = None

    with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Konversi frame ke RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(frame_rgb)

            # Jika ada wajah yang terdeteksi
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    nose_tip = face_landmarks.landmark[1]
                    left_cheek = face_landmarks.landmark[234]
                    right_cheek = face_landmarks.landmark[454]
                    top_head = face_landmarks.landmark[10]  # Titik atas kepala

                    # Hitung pusat wajah
                    face_center_x = (left_cheek.x + right_cheek.x) / 2
                    head_angle = calculate_head_angle(nose_tip, face_center_x)

                    # Ambang batas sudut kepala untuk deteksi gerakan
                    angle_threshold = 15  # Ambang batas lebih kecil untuk sensitivitas yang lebih tinggi

                    # Pilihan berdasarkan arah kepala
                    current_time = time.time()
                    direction = None
                    if head_angle > angle_threshold:
                        direction = "right"
                    elif head_angle < -angle_threshold:
                        direction = "left"

                    # Hitung stabilitas arah
                    if direction == previous_angle_direction:
                        stable_count += 1
                    else:
                        stable_count = 0  # Reset jika arah berubah

                    previous_angle_direction = direction

                    if stable_count >= stability_threshold and current_position_index < len(positions):
                        if current_time - last_selection_time >= cooldown_time:  # Tambahkan cooldown
                            if direction == "right":  # Kepala ke kanan
                                selected_players.append(positions[current_position_index]["options"][1])
                                current_position_index += 1
                            elif direction == "left":  # Kepala ke kiri
                                selected_players.append(positions[current_position_index]["options"][0])
                                current_position_index += 1

                            last_selection_time = current_time
                            stable_count = 0  # Reset stabilitas

                    # Tampilkan gambar di atas kepala
                    frame_height, frame_width, _ = frame.shape
                    text_position_left = (
                        int(top_head.x * frame_width) - 200,
                        int((top_head.y - 0.1) * frame_height)
                    )
                    text_position_right = (
                        int(top_head.x * frame_width) + 50,
                        int((top_head.y - 0.1) * frame_height)
                    )

                    # Tampilkan gambar pilihan kiri dan kanan
                    if current_position_index < len(positions):
                        position = positions[current_position_index]
                        left_image = player_images[position["options"][0]]
                        right_image = player_images[position["options"][1]]

                        # Tempelkan gambar di posisi yang sesuai
                        frame = overlay_image(frame, left_image, (text_position_left[0], text_position_left[1]))
                        frame = overlay_image(frame, right_image, (text_position_right[0], text_position_right[1]))

            # Menampilkan informasi posisi yang tetap di bagian atas
            if current_position_index < len(positions):
                position = positions[current_position_index]
                # Hanya menampilkan nama posisi (misalnya: Posisi: GK)
                info_position_text = f"Posisi: {position['name']}"
                cv2.putText(frame, info_position_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            # Jika semua pemain sudah dipilih
            if current_position_index >= len(positions):
                frame = create_field_with_players(selected_players, frame)
                # Simpan hasil pemilihan pemain ke file JPG
                cv2.imwrite("starting_eleven_custom_form.jpg", frame)

                cv2.imshow("Starting Eleven", frame)
                # Tampilkan hasil selama 10 detik sebelum keluar
                cv2.waitKey(10000)
                break

            # Tampilkan frame
            cv2.imshow("Starting Eleven Selection", frame)

            # Keluar dengan 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
