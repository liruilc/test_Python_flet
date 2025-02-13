import flet as ft 
import cv2
import base64
import threading
import time 

class CameraApp(ft.Column):  # ✅ 使用 Column 代替 UserControl
    def __init__(self, page: ft.Page):
        super().__init__(expand=True)
        self.page = page
        self.thread_running = True  # ✅ 避免未定义变量
        self.page.window.width = 900
        self.page.window.prevent_close = True
        self.page.window.on_event = self.window_event
        
        # 读取默认图片
        try:
            path = base64.b64encode(open("camara.png", "rb").read()).decode("utf-8")
        except FileNotFoundError:
            print("⚠️ 警告: 找不到 camara.png，使用空白图像")
            path = ""

        self.video1 = ft.Image(src_base64=path, expand=True)
        self.video2 = ft.Image(src_base64=path, expand=True)

        # 相机界面
        self.cameras = ft.Column(
            expand=True,
            controls=[
                ft.Container(expand=True, border_radius=10, content=self.video1),
                ft.Container(expand=True, border_radius=10, content=self.video2),
            ],
        )

        # 信息栏
        self.info_text = ft.Column(
            expand=True,
            controls=[
                ft.Container(expand=True, border_radius=10, bgcolor="blue"),
                ft.Container(expand=True, border_radius=10, bgcolor="blue"),
            ],
        )

        self.controls = [ft.Row(expand=True, controls=[self.cameras, self.info_text])]
        self.page.update()  # ✅ 确保 UI 刷新

        # 启动线程
        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            print("⚠️ 错误: 无法连接到摄像头")
        else:
            self.threading = threading.Thread(target=self.update_frame_camera)
            self.threading.start()

    def update_frame_camera(self):
        """实时更新摄像头画面"""
        while self.thread_running:
            ret, frame = self.capture.read()
            if ret:
                _, buffer = cv2.imencode(".png", frame)
                self.frame = base64.b64encode(buffer).decode("utf-8")
                self.video1.src_base64 = self.frame
                self.video2.src_base64 = self.frame
                self.page.update()  # ✅ 确保 UI 刷新
            else:
                print("⚠️ 错误: 读取摄像头失败")
            time.sleep(0.03)

    def window_event(self, e):
        if e.data == "close":
            self.page.overlay.append(ft.AlertDialog(
                modal=True,
                title=ft.Text("请确认"),
                content=ft.Text("是否关闭应用？"),
                actions=[
                    ft.ElevatedButton("是", on_click=self.yes_click),
                    ft.OutlinedButton("否", on_click=self.no_click),
                ],
            ))
            self.page.update()

    def yes_click(self, e):
        self.thread_running = False
        if self.threading.is_alive():
            self.threading.join()
        self.capture.release()
        self.page.window_close()

    def no_click(self, e):
        self.page.update()

# 启动 Flet 应用
ft.app(target=lambda page: page.add(CameraApp(page)))  # ✅ 正确添加组件
