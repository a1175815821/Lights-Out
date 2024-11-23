from cx_Freeze import setup, Executable
import sys

# 如果你使用的是特定的 Python 版本，请在 sys.argv 中传递 --build-exe
build_exe_options = {
    "packages": ["pygame", "pyttsx3"],
    "include_files": ["background_music.mp3", "click_sound.mp3"],  # 需要包含的音频文件
    "excludes": ["tkinter"]  # 如果你不使用 tkinter，可以排除
}

setup(
    name="LightsOutGame",
    version="1.0",
    description="关灯游戏",
    options={"build_exe": build_exe_options},
    executables=[Executable("game.py", base=None)]  # 这里指定你的脚本
)
