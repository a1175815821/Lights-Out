import tkinter as tk
from tkinter import ttk
import random
import time
import pygame
import pyttsx3
from tkinter import messagebox
import os
import sys
import pygame
import pyttsx3

def resource_path(relative_path):
    """获取资源文件的路径，适用于打包后的 .exe 文件"""
    try:
        # 如果是 PyInstaller 打包后的程序，资源文件放在临时文件夹中
        base_path = sys._MEIPASS
    except Exception:
        # 非 PyInstaller 创建的环境，使用当前工作目录
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class LightsOutGame:
    def __init__(self, root):
        self.root = root
        self.step_count = 0
        self.score = 0
        self.start_time = None  # 初始化计时器
        self.mode = "fixed"  # 默认固定模式
        self.size = 4  # 默认4x4网格
        self.buttons = []  # 存储按钮
        self.setup_ui()
        self.init_audio()

    def init_audio(self):
        """初始化音效和背景音乐"""
        try:
            pygame.mixer.init()
            print(pygame.mixer.get_init())  # 输出音频初始化信息

            # 获取资源文件的路径
            click_sound_path = resource_path("click_sound.mp3")
            background_music_path = resource_path("background_music.mp3")

            # 加载音效和背景音乐
            self.click_sound = pygame.mixer.Sound(click_sound_path)
            pygame.mixer.music.load(background_music_path)
            pygame.mixer.music.set_volume(1.0)  # 设置背景音乐音量
            pygame.mixer.music.play(-1)  # 循环播放背景音乐

            # 初始化语音引擎
            self.engine = pyttsx3.init()
            print("音效和语音引擎初始化成功")

        except Exception as e:
            print(f"音效或语音引擎初始化失败: {e}")

    def play_click_sound(self):
        """播放点击音效"""
        try:
            self.click_sound.play()
        except Exception as e:
            print(f"播放音效失败: {e}")

    # 其他游戏逻辑代码保持不变



class LightsOutGame:
    def __init__(self, root):
        self.root = root
        self.step_count = 0
        self.score = 0
        self.start_time = None  # 初始化计时器
        self.mode = "fixed"  # 默认固定模式
        self.size = 4  # 默认4x4网格
        self.buttons = []  # 存储按钮
        self.setup_ui()
        self.init_audio()

    def setup_ui(self):
        """设置游戏的用户界面"""
        self.root.title("关灯游戏")
        self.root.geometry("600x600")
        self.root.config(bg="#333333")

        # 创建分数和计时器显示
        self.step_label = tk.Label(self.root, text="步数: 0", bg="#333333", fg="white")
        self.step_label.pack()

        self.timer_label = tk.Label(self.root, text="时间: 0s", bg="#333333", fg="white")
        self.timer_label.pack()

        # 难度选择
        difficulty_label = tk.Label(self.root, text="选择难度:", bg="#333333", fg="white")
        difficulty_label.pack()

        self.difficulty_combobox = ttk.Combobox(self.root, values=[("3x3", 3), ("4x4", 4), ("5x5", 5)],
                                                state="readonly")
        self.difficulty_combobox.set("4x4")
        self.difficulty_combobox.pack(pady=10)
        self.difficulty_combobox.bind("<<ComboboxSelected>>", self.change_difficulty)

        # 模式选择
        mode_label = tk.Label(self.root, text="选择模式:", bg="#333333", fg="white")
        mode_label.pack()

        self.mode_combobox = ttk.Combobox(self.root, values=["固定模式", "随机模式"], state="readonly")
        self.mode_combobox.set("固定模式")
        self.mode_combobox.pack(pady=10)
        self.mode_combobox.bind("<<ComboboxSelected>>", self.change_mode)

        # 重置按钮
        reset_button = tk.Button(self.root, text="重置游戏", command=self.reset_game, bg="#FF4500", fg="white")
        reset_button.pack(pady=10)

        # 初始化按钮网格
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.init_grid()

    def init_audio(self):
        """初始化音效和背景音乐"""
        try:
            pygame.mixer.init()
            print(pygame.mixer.get_init())  # 输出音频初始化信息

            # 加载音效和背景音乐
            self.click_sound = pygame.mixer.Sound("click_sound.mp3")
            pygame.mixer.music.load("background_music.mp3")
            pygame.mixer.music.set_volume(1.0)  # 设置背景音乐音量
            pygame.mixer.music.play(-1)  # 循环播放背景音乐

            # 初始化语音引擎
            self.engine = pyttsx3.init()
            print("音效和语音引擎初始化成功")

        except Exception as e:
            print(f"音效或语音引擎初始化失败: {e}")

    def init_grid(self):
        """初始化按钮网格"""
        # 清空之前的按钮
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.buttons = []
        for i in range(self.size):  # 设置为新的网格大小
            row = []
            for j in range(self.size):
                button = tk.Button(self.grid_frame, width=5, height=2, bg="#1E90FF",  # 蓝色按钮
                                   command=lambda i=i, j=j: self.toggle_lights(i, j))
                button.grid(row=i, column=j, sticky="nsew")
                row.append(button)
            self.buttons.append(row)

        # 自适应按钮大小
        for i in range(self.size):
            self.grid_frame.grid_columnconfigure(i, weight=1)
            self.grid_frame.grid_rowconfigure(i, weight=1)

        # 应用模式
        self.apply_mode()

    def reset_game(self):
        """重置游戏状态"""
        print("游戏重置")
        self.step_count = 0
        self.score = 0
        if self.start_time is None:  # 如果计时器尚未启动，则启动计时器
            self.start_time = time.time()
        self.update_labels()

        # 重新初始化按钮状态
        self.init_grid()

    def toggle_lights(self, i, j):
        """切换灯光状态"""
        print(f"点击灯光: ({i}, {j})")
        # 播放点击音效
        try:
            self.click_sound.play()
        except Exception as e:
            print(f"播放音效失败: {e}")

        # 点击按钮时切换它本身以及周围按钮的颜色
        self.toggle_button(i, j)  # 切换当前按钮
        if i > 0: self.toggle_button(i - 1, j)  # 上方按钮
        if i < self.size - 1: self.toggle_button(i + 1, j)  # 下方按钮
        if j > 0: self.toggle_button(i, j - 1)  # 左方按钮
        if j < self.size - 1: self.toggle_button(i, j + 1)  # 右方按钮

        self.step_count += 1
        self.update_labels()

        # 判断是否完成游戏，如果所有灯光熄灭则弹出成功提示
        if self.check_win():
            self.show_success_popup()

    def toggle_button(self, i, j):
        """切换按钮颜色"""
        current_color = self.buttons[i][j].cget("bg")
        new_color = "#1E90FF" if current_color == "#333333" else "#333333"  # 切换颜色
        self.buttons[i][j].config(bg=new_color)

    def apply_mode(self):
        """根据选择的模式应用初始灯光状态"""
        for i in range(self.size):
            for j in range(self.size):
                if self.mode == "random":
                    # 随机选择亮或灭
                    current_color = "#1E90FF" if random.choice([True, False]) else "#333333"
                elif self.mode == "fixed":
                    # 固定模式：所有按钮初始状态为亮
                    current_color = "#1E90FF"
                self.buttons[i][j].config(bg=current_color)

    def update_labels(self):
        """更新计时器和步数"""
        # 计算时间
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            minutes, seconds = divmod(elapsed_time, 60)
            timer_text = f"{int(minutes)}:{int(seconds):02d}"
            self.timer_label.config(text=f"时间: {timer_text}")

        # 更新步数
        self.step_label.config(text=f"步数: {self.step_count}")

        # 每1000毫秒（1秒）更新一次计时器
        self.root.after(1000, self.update_labels)

    def change_difficulty(self, event):
        """更改难度"""
        selected_size = int(self.difficulty_combobox.get().split('x')[0])
        print(f"选择难度: {selected_size}x{selected_size}")
        self.size = selected_size
        self.reset_game()

    def change_mode(self, event):
        """更改游戏模式"""
        # 根据事件内容确定新的模式
        new_mode = "random" if event.widget.get() == "随机模式" else "fixed"

        # 只有在模式发生变化时才更新
        if new_mode != self.mode:
            print(f"更改模式到 {new_mode}")
            self.mode = new_mode  # 只需将模式设置为新模式

            # 应用新模式
            self.apply_mode()

    def check_win(self):
        """检查是否完成游戏"""
        for i in range(self.size):
            for j in range(self.size):
                # 如果任何按钮的颜色不是暗色，则游戏没有完成
                if self.buttons[i][j].cget("bg") != "#333333":
                    return False
        return True

    def show_success_popup(self):
        """显示成功弹窗"""
        elapsed_time = time.time() - self.start_time
        minutes, seconds = divmod(elapsed_time, 60)
        timer_text = f"{int(minutes)}:{int(seconds):02d}"

        # 弹出成功窗口，显示步数和时间
        messagebox.showinfo("成功", f"恭喜你完成了游戏！\n\n步数: {self.step_count}\n时间: {timer_text}")


# 启动游戏主循环
if __name__ == "__main__":
    root = tk.Tk()
    game = LightsOutGame(root)
    root.mainloop()
