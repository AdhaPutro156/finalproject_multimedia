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

# Muat gambar pemain
player_images = {
    "A": cv2.imread("player_A.jpg"),
    "B": cv2.imread("player_B.jpg"),
    "C": cv2.imread("player_C.jpg"),
    "D": cv2.imread("player_D.jpg"),
    "E": cv2.imread("player_E.jpg"),
    "F": cv2.imread("player_F.jpg"),
    "G": cv2.imread("player_G.jpg"),
    "H": cv2.imread("player_H.jpg"),
    "I": cv2.imread("player_I.jpg"),
    "J": cv2.imread("player_J.jpg"),
    "K": cv2.imread("player_K.jpg"),
    "L": cv2.imread("player_L.jpg"),
    "M": cv2.imread("player_M.jpg"),
    "N": cv2.imread("player_N.jpg"),
    "O": cv2.imread("player_O.jpg"),
    "P": cv2.imread("player_P.jpg"),
    "Q": cv2.imread("player_Q.jpg"),
    "R": cv2.imread("player_R.jpg"),
    "S": cv2.imread("player_S.jpg"),
    "T": cv2.imread("player_T.jpg"),
    "U": cv2.imread("player_U.jpg"),
    "V": cv2.imread("player_V.jpg")
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
