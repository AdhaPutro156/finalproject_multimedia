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
