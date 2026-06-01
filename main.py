import tkinter as tk
from PIL import Image, ImageTk
import cv2
import socket


CAMERA_IP   = "192.168.144.108"
CAMERA_PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


class DroneControlUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gimbal Control Station")
        self.root.geometry("1400x800")
        self.root.configure(bg="#121212")
        self.cam_mode = "EO"
        # ==========================
        # Header
        # ==========================
        header = tk.Frame(root, bg="#1e1e1e", height=60)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="DRONE GIMBAL CONTROL STATION",
            font=("Segoe UI", 18, "bold"),
            fg="cyan",
            bg="#1e1e1e"
        )
        title.pack(pady=10)

        # ==========================
        # Main Layout
        # ==========================
        main = tk.Frame(root, bg="#121212")
        main.pack(fill="both", expand=True)

        # ==========================
        # Left Panel
        # ==========================
        left_panel = tk.Frame(main, bg="#1e1e1e", width=250)
        left_panel.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(
            left_panel,
            text="SYSTEM STATUS",
            font=("Segoe UI", 14, "bold"),
            fg="white",
            bg="#1e1e1e"
        ).pack(pady=20)

        self.status = tk.Label(
            left_panel,
            text="● Connected",
            fg="lime",
            bg="#1e1e1e",
            font=("Segoe UI", 12)
        )
        self.status.pack(pady=5)

        self.gimbal = tk.Label(
            left_panel,
            text="Gimbal : Ready",
            fg="white",
            bg="#1e1e1e",
            font=("Segoe UI", 11)
        )
        self.gimbal.pack(pady=5)

        #self.camera = tk.Label(
        #    left_panel,
        #    text="Camera : Online",
        #    fg="white",
        #    bg="#1e1e1e",
        #    font=("Segoe UI", 11)
        #)
        #self.camera.pack(pady=5)

        # ==========================
        # Video Panel
        # ==========================
        center_panel = tk.Frame(main, bg="#121212")
        center_panel.pack(side="left", fill="both", expand=True)

        self.video_label = tk.Label(
            center_panel,
            bg="black",
            bd=3,
            relief="ridge"
        )
        self.video_label.pack(expand=True, padx=10, pady=10)

        # ==========================
        # Right Control Panel
        # ==========================
        right_panel = tk.Frame(main, bg="#1e1e1e", width=300)
        right_panel.pack(side="right", fill="y", padx=10, pady=10)

        tk.Label(
            right_panel,
            text="GIMBAL CONTROL",
            font=("Segoe UI", 14, "bold"),
            fg="white",
            bg="#1e1e1e"
        ).pack(pady=20)

        dpad = tk.Frame(right_panel, bg="#1e1e1e")
        dpad.pack(pady=40)

        btn_style = {
            "font": ("Segoe UI", 22, "bold"),
            "bg": "#00AEEF",
            "fg": "white",
            "activebackground": "#007ACC",
            "width": 3,
            "height": 1,
            "bd": 0
        }

        up = tk.Button(dpad, text="↑", **btn_style, command=self.up)
        up.grid(row=0, column=1, padx=10, pady=10)

        left = tk.Button(dpad, text="←", **btn_style, command=self.left)
        left.grid(row=1, column=0, padx=10, pady=10)

        center = tk.Button(
            dpad,
            text="●",
            bg="#333333",
            fg="lime",
            font=("Segoe UI", 20, "bold"),
            width=3,
            bd=0,
            command=self.center
        )
        center.grid(row=1, column=1)

        right = tk.Button(dpad, text="→", **btn_style, command=self.right)
        right.grid(row=1, column=2, padx=10, pady=10)

        down = tk.Button(dpad, text="↓", **btn_style, command=self.down)
        down.grid(row=2, column=1, padx=10, pady=10)

        # ==========================
        # Zoom Buttons
        # ==========================
        zoom_frame = tk.Frame(right_panel, bg="#1e1e1e")
        zoom_frame.pack(pady=30)

        tk.Button(
            zoom_frame,
            text="Zoom +",
            width=12,
            bg="#28A745",
            fg="white",
            font=("Segoe UI", 11, "bold")
        ).pack(pady=5)

        tk.Button(
            zoom_frame,
            text="Zoom -",
            width=12,
            bg="#DC3545",
            fg="white",
            font=("Segoe UI", 11, "bold")
        ).pack(pady=5)

        # ==========================
        # RTSP Stream
        # ==========================
        DAY_RTSP_URL = "rtspsrc location=rtsp://192.168.144.108:554/stream=1 latency=0 ! decodebin ! videoconvert ! appsink"
        NIGHT_RTSP_URL = "rtspsrc location=rtsp://192.168.144.108:554/stream=2 latency=0 ! decodebin ! videoconvert ! appsink"

        #self.cap = cv2.VideoCapture(DAY_RTSP_URL, cv2.CAP_GSTREAMER)
        #self.cap = cv2.VideoCapture(NIGHT_RTSP_URL, cv2.CAP_GSTREAMER)
        self.cap = cv2.VideoCapture(0)

        self.update_video()


    def build_packet(self, axis: str, speed: int) -> bytes:
        """
        axis  : 'Y' = yaw/pan,  'P' = pitch/tilt
        speed : -127 (left/down) … 0 (stop) … +127 (right/up)
        """
        speed    = speed
        body     = f"#TPUG2wGS{axis}{speed & 0xFF:02X}"
        checksum = sum(ord(c) for c in body) % 256
        return f"{body}{checksum:02X}".encode('ascii')
    
    def send_cmd(self,axis,speed):
        packet = self.build_packet(axis, speed)
        sock.sendto(packet, (CAMERA_IP, CAMERA_PORT))
        print("-----PACKET: ",packet)

    def up(self):
        axis = 'Y'
        self.send_cmd(axis, 50)

    def down(self):
        axis = 'Y'
        self.send_cmd(axis, -50)

    def left(self):
        axis = 'P'
        self.send_cmd(axis,-50)

    def right(self):
        axis = 'P'
        self.send_cmd(axis,50)

    def center(self):
        axis_y, axis_p = 'Y', 'P'
        self.send_cmd(axis_y, 0)
        self.send_cmd(axis_p, 0)

    def update_video(self):
        ret, frame = self.cap.read()

        if ret:
            # Stream is working
            self.status.config(
                text="● Connected",
                fg="lime"
            )

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            img = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(img)

            self.video_label.imgtk = img_tk
            self.video_label.configure(image=img_tk)

        else:
            # No frame received
            self.status.config(
                text="● No Stream",
                fg="red"
            )

        self.root.after(30, self.update_video)


root = tk.Tk()
app = DroneControlUI(root)
root.mainloop()