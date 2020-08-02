class Camera:
    def __init__(self, cam_num):
        self.cam_num = cam_num
        self.cap = None

    def initialize(self):
        self.cap = cv2.VideoCapture(self.cam_num)

    def get_frame(self):
        ret, self.last_frame = self.cap.read()
        return self.last_frame

    def set_brightness(self, value):
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, value)

    def acquire_movie(self, num_frames):
        movie = []
        for _ in range(num_frames):
            movie.append(self.get_frame())
        return movie

    def get_brightness(self):
        return self.cap.get(cv2.CAP_PROP_BRIGHTNESS)

    def __str__(self):
        return 'OpenCV Camera {}'.format(self.cam_num)

    def close_camera(self):
        self.cap.release()


class MovieThread(QThread):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera

    def run(self):
        self.camera.acquire_movie(200)


class StartWindow(QMainWindow):
    def update_image(self):
        frame = self.camera.get_frame()
        self.image_view.setImage(frame.T)

    def start_movie(self):
        self.camera.acquire_movie(1000)

    def __init__(self, camera=None):
        super().__init__()
        self.camera = camera

        self.central_widget = QWidget()
        self.button_frame = QPushButton('Acquire Frame', self.central_widget)
        self.button_movie = QPushButton('Start Movie', self.central_widget)
        self.button_movie.clicked.connect(self.start_movie)
        self.button_frame.clicked.connect(self.update_image)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.button_frame)
        self.layout.addWidget(self.button_movie)
        self.setCentralWidget(self.central_widget)
        self.image_view = ImageView()
        self.layout.addWidget(self.image_view)


camera = Camera(0)
camera.initialize()

app = QApplication([])
start_window = StartWindow(camera)
start_window.show()
app.exit(app.exec_())
