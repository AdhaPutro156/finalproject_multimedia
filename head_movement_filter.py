import cv2
import numpy as np
import mediapipe as mp
import time
import random

# Fungsi untuk menghitung sudut kepala berdasarkan ujung hidung dan pusat wajah
def calculate_head_angle(nose_tip, face_center_x):
    angle = (nose_tip.x - face_center_x) * 100
    return angle

# Fungsi untuk mengubah ukuran gambar ke lebar dan tinggi yang ditentukan
def resize_image(image, width, height):
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

# Fungsi untuk menempatkan gambar di atas frame latar belakang pada posisi yang ditentukan
def overlay_image(background, overlay, position):
    x, y = position
    h, w, _ = overlay.shape
    background_height, background_width, _ = background.shape

# Menyesuaikan ukuran overlay agar sesuai dengan area yang tersedia
    if x + w > background_width:
        w = background_width - x
    if y + h > background_height:
        h = background_height - y

# Mengubah ukuran gambar overlay agar sesuai dengan area yang tersedia
    overlay_resized = cv2.resize(overlay, (w, h), interpolation=cv2.INTER_AREA)

# Menempatkan gambar overlay yang telah diubah ukuran ke latar belakang
    background[y:y+h, x:x+w] = overlay_resized
    return background

# Kamus untuk menyimpan poin pemain untuk berbagai pemain
player_points = {
    "gk1": 85, "gk2": 90, "gk3": 70, "gk4": 88,
    "lb1": 77, "lb2": 80, "lb3": 82, "lb4": 78,
    "lcb1": 75, "lcb2": 85, "lcb3": 87, "lcb4": 80,
    "rcb1": 88, "rcb2": 82, "rcb3": 79, "rcb4": 81,
    "rb1": 76, "rb2": 85, "rb3": 80, "rb4": 78,
    "cmf1": 82, "cmf2": 89, "cmf3": 84, "cmf4": 81,
    "dmf1": 87, "dmf2": 85, "dmf3": 90, "dmf4": 80,
    "lwf1": 88, "lwf2": 92, "lwf3": 84, "lwf4": 86,
    "cf1": 95, "cf2": 90, "cf3": 88, "cf4": 91,
    "rwf1": 89, "rwf2": 87, "rwf3": 86, "rwf4": 84
}

# Fungsi untuk membuat kanvas tampilan hasil untuk pemain yang dipilih
def create_result_display(selected_players):
    canvas_height = 720
    canvas_width = 1280
    canvas = np.ones((canvas_height, canvas_width, 3), dtype=np.uint8) * 34

    # Adjusted coordinates for 4-3-3 formation
    positions = {
        "goalkeeper": [(canvas_width // 2, canvas_height - 100)],  # Goalkeeper position
        "defenders": [
            (canvas_width // 2 - 300, canvas_height - 250),  # LB
            (canvas_width // 2 - 100, canvas_height - 250),  # LCB
            (canvas_width // 2 + 100, canvas_height - 250),  # RCB
            (canvas_width // 2 + 300, canvas_height - 250)   # RB
        ],
        "midfielders": [
            (canvas_width // 2 - 200, canvas_height - 450),  # LMF
            (canvas_width // 2, canvas_height - 400),        # CMF
            (canvas_width // 2 + 200, canvas_height - 450)   # RMF
        ],
        "forwards": [
            (canvas_width // 2 - 300, canvas_height - 600),  # LWF
            (canvas_width // 2, canvas_height - 650),        # CF
            (canvas_width // 2 + 300 , canvas_height - 600)   # RWF
        ]
    }

# Menggunakan nilai dari kamus player_points untuk mendapatkan skor pemain yang dipilih
    player_scores = [player_points[player] for player in selected_players]
    total_score = sum(player_scores)

    if total_score >= 900:
        team_rating = "Very Very Very Nice Team!"
    elif total_score >= 800:
        team_rating = "Good Team"
    elif total_score >= 700:
        team_rating = "Better Team"
    elif total_score >= 600:
        team_rating = "Goodluck Team"
    else:
        team_rating = "Bad Team"

# Menampilkan pemain sesuai dengan formasi
    for i, player in enumerate(selected_players):
        img = resize_image(player_images[player], 80, 80)
        if i == 0:  # Goalkeeper
            x, y = positions["goalkeeper"][0]
        elif i < 5:  # Defenders
            x, y = positions["defenders"][i - 1]
        elif i < 8:  # Midfielders
            x, y = positions["midfielders"][i - 5]
        elif i < 11:  # Forwards
            x, y = positions["forwards"][i - 8]
        else:
            continue  # Melewati jika ada lebih dari 11 pemain

        canvas[y:y+img.shape[0], x:x+img.shape[1]] = img
        cv2.putText(canvas, f"{player_scores[i]} Pts", (x, y + img.shape[0] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

# Menampilkan total skor dan rating tim
    cv2.putText(canvas, f"Total Score: {total_score}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
    cv2.putText(canvas, team_rating, (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)

    return canvas

# Player data and dummy images for testing
player_images = {
    "gk1": cv2.imread("player_gk1.jpg"),
    "gk2": cv2.imread("player_gk2.jpg"),
    "gk3": cv2.imread("player_gk3.jpg"),
    "gk4": cv2.imread("player_gk4.jpg"),
    "lb1": cv2.imread("player_lb1.jpg"),
    "lb2": cv2.imread("player_lb2.jpg"),
    "lb3": cv2.imread("player_lb3.jpg"),
    "lb4": cv2.imread("player_lb4.jpg"),
    "lcb1": cv2.imread("player_lcb1.jpg"),
    "lcb2": cv2.imread("player_lcb2.jpg"),
    "lcb3": cv2.imread("player_lcb3.jpg"),
    "lcb4": cv2.imread("player_lcb4.jpg"),
    "rcb1": cv2.imread("player_rcb1.jpg"),
    "rcb2": cv2.imread("player_rcb2.jpg"),
    "rcb3": cv2.imread("player_rcb3.jpg"),
    "rcb4": cv2.imread("player_rcb4.jpg"),
    "rb1": cv2.imread("player_rb1.jpg"),
    "rb2": cv2.imread("player_rb2.jpg"),
    "rb3": cv2.imread("player_rb3.jpg"),
    "rb4": cv2.imread("player_rb4.jpg"),
    "cmf1": cv2.imread("player_cmf1.jpg"),
    "cmf2": cv2.imread("player_cmf2.jpg"),
    "cmf3": cv2.imread("player_cmf3.jpg"),
    "cmf4": cv2.imread("player_cmf4.jpg"),
    "dmf1": cv2.imread("player_dmf1.jpg"),
    "dmf2": cv2.imread("player_dmf2.jpg"),
    "dmf3": cv2.imread("player_dmf3.jpg"),
    "dmf4": cv2.imread("player_dmf4.jpg"),
    "lwf1": cv2.imread("player_lwf1.jpg"),
    "lwf2": cv2.imread("player_lwf2.jpg"),
    "lwf3": cv2.imread("player_lwf3.jpg"),
    "lwf4": cv2.imread("player_lwf4.jpg"),
    "cf1": cv2.imread("player_cf1.jpg"),
    "cf2": cv2.imread("player_cf2.jpg"),
    "cf3": cv2.imread("player_cf3.jpg"),
    "cf4": cv2.imread("player_cf4.jpg"),
    "rwf1": cv2.imread("player_rwf1.jpg"),
    "rwf2": cv2.imread("player_rwf2.jpg"),
    "rwf3": cv2.imread("player_rwf3.jpg"),
    "rwf4": cv2.imread("player_rwf4.jpg")
}

# Memeriksa apakah gambar dimuat dengan benar
for player, image in player_images.items():
    if image is None:
        print(f"Error loading image for {player}. Check the file path.")

positions = [
    {"name": "GK", "options": ["gk1", "gk2", "gk3", "gk4"]},
    {"name": "LB", "options": ["lb1", "lb2", "lb3", "lb4"]},
    {"name": "LCB", "options": ["lcb1", "lcb2", "lcb3", "lcb4"]},
    {"name": "RCB", "options": ["rcb1", "rcb2", "rcb3", "rcb4"]},
    {"name": "RB", "options": ["rb1", "rb2", "rb3", "rb4"]},
    {"name": "CMF1", "options": ["cmf1", "cmf2", "cmf3", "cmf4"]},
    {"name": "DMF", "options": ["dmf1", "dmf2", "dmf3", "dmf4"]},
    {"name": "CMF2", "options": ["cmf1", "cmf2", "cmf3", "cmf4"]},
    {"name": "LWF", "options": ["lwf1", "lwf2", "lwf3", "lwf4"]},
    {"name": "CF", "options": ["cf1", "cf2", "cf3", "cf4"]},
    {"name": "RWF", "options": ["rwf1", "rwf2", "rwf3", "rwf4"]}
]

# Fungsi utama untuk menjalankan program
def main():
    cap = cv2.VideoCapture(0)
    selected_players = []
    current_position_index = 0
    debounce_time = 1.0
    cooldown_time = 0.3
    last_selection_time = time.time()

    stability_threshold = 5
    stable_count = 0
    previous_angle_direction = None
    confirmed_selection = False  # New variable to track confirmation

    selected_options = {}  # Store selected options for each position

    with mp.solutions.face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(frame_rgb)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    nose_tip = face_landmarks.landmark[1]
                    left_cheek = face_landmarks.landmark[234]
                    right_cheek = face_landmarks.landmark[454]
                    top_head = face_landmarks.landmark[10]

                    face_center_x = (left_cheek.x + right_cheek.x) / 2
                    head_angle = calculate_head_angle(nose_tip, face_center_x)

                    angle_threshold = 15
                    direction = None
                    if head_angle > angle_threshold:
                        direction = "right"
                    elif head_angle < -angle_threshold:
                        direction = "left"
                    else:
                        direction = None

                    if direction == previous_angle_direction:
                        stable_count += 1
                    else:
                        stable_count = 0

                    previous_angle_direction = direction

                    if stable_count >= stability_threshold and current_position_index < len(positions):
                        current_time = time.time()
                        if current_time - last_selection_time >= cooldown_time:
                            position = positions[current_position_index]
                            if position["name"] not in selected_options:
                                selected_options[position["name"]] = random.sample(position["options"], 2)  # Select two random options

                            left_image = player_images[selected_options[position["name"]][0]]
                            right_image = player_images[selected_options[position["name"]][1]]

                            face_width = int(abs(right_cheek.x - left_cheek.x) * frame.shape[1])
                            face_height = int(abs(top_head.y - nose_tip.y) * frame.shape[0])

                            left_image_resized = resize_image(left_image, face_width, face_height)
                            right_image_resized = resize_image(right_image, face_width, face_height)

                            frame = overlay_image(frame, left_image_resized, (50, 100))
                            frame = overlay_image(frame, right_image_resized, (400, 100))

                            if direction == "left" or direction == "right":
                                confirmed_selection = True

                            if confirmed_selection:
                                selected_player = selected_options[position["name"]][0] if direction == "left" else selected_options[position["name"]][1]
                                selected_players.append(selected_player)
                                current_position_index += 1
                                last_selection_time = current_time
                                confirmed_selection = False

                    if current_position_index < len(positions):
                        position = positions[current_position_index]
                        info_position_text = f"Position: {position['name']}"
                        cv2.putText(frame, info_position_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            if current_position_index >= len(positions):
                result_display = create_result_display(selected_players)
                cv2.imshow("Starting Eleven Result", result_display)
                cv2.waitKey(10000)
                break

            cv2.imshow("Starting Eleven Selection", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
