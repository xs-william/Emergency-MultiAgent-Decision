# ==========================================
# Module: Multimodal Input Parser
# File: planner/multimodal_input.py
# ==========================================
# 🧩 模块功能：
#   - 接收用户的文本 / 图像 / 音频多模态输入；
#   - 自动检测并转换多种音频格式（mp3, wav, flac, m4a, ogg）；
#   - 统一编码为 Base64，输出标准 JSON；
#   - 可扩展至 video / sensor 等模态。
# ==========================================

from typing import Optional, Dict, Any
from pathlib import Path
import base64
import json
import os
import numpy as np
from PIL import Image
import io
from datetime import datetime
from pydub import AudioSegment  # 🎧 用于多格式音频解析


class MultiModalInput:
    """多模态输入封装类：统一管理文本 / 图像 / 音频等模态"""

    def __init__(self,
                 text: Optional[str] = None,
                 image_input: Optional[Any] = None,
                 audio_input: Optional[Any] = None):
        self.text = text.strip() if text else ""
        self.image_input = image_input
        self.audio_input = audio_input

    # -------------------------
    # 文本模态解析
    # -------------------------
    def parse_text(self) -> Dict[str, Any]:
        """文本输入解析"""
        return {"text_valid": bool(self.text), "text_content": self.text or ""}

    # -------------------------
    # 图像模态解析
    # -------------------------
    def parse_image(self) -> Dict[str, Any]:
        """图像输入解析：支持路径 / dict / numpy 数组"""
        try:
            # ✅ 只判断 None，不直接对 numpy 做布尔判断
            if self.image_input is None:
                return {"image_valid": False, "image_base64": ""}

            # 1️⃣ Gradio dict 格式
            if isinstance(self.image_input, dict) and "data" in self.image_input:
                img_data = self.image_input["data"]
                if isinstance(img_data, np.ndarray):  # numpy数组
                    img = Image.fromarray(img_data.astype("uint8"))
                    buf = io.BytesIO()
                    img.save(buf, format="PNG")
                    encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
                elif isinstance(img_data, (bytes, bytearray)):
                    encoded = base64.b64encode(img_data).decode("utf-8")
                else:
                    return {"image_valid": False, "image_base64": ""}
                name = self.image_input.get("name", "uploaded_image")

            # 2️⃣ numpy.ndarray 格式
            elif isinstance(self.image_input, np.ndarray):
                img = Image.fromarray(self.image_input.astype("uint8"))
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
                name = "array_image.png"

            # 3️⃣ 文件路径格式
            elif isinstance(self.image_input, (str, Path)) and Path(self.image_input).exists():
                with open(self.image_input, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode("utf-8")
                name = Path(self.image_input).name

            else:
                return {"image_valid": False, "image_base64": ""}

            print(f"[✅ ImageParse] Parsed: {name}")
            return {
                "image_valid": True,
                "image_name": name,
                "image_base64": encoded
            }

        except Exception as e:
            print(f"[⚠️ ImageParse] Error: {e}")
            return {"image_valid": False, "image_base64": ""}

    def parse_audio(self):
        """
        ✅ 最简工程版音频解析：
        - 支持 mp3 / wav / flac / m4a / ogg；
        - Gradio 自动生成临时文件路径；
        - 后端只需读取并 base64 编码；
        - 不依赖 soundfile / pydub；
        - 稳定且通用。
        """
        log_dir = Path("output/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / "audio_parse.log"

        def log(msg):
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{ts}] {msg}")
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"[{ts}] {msg}\n")

        # 检查文件有效性
        if not self.audio_input or not Path(self.audio_input).exists():
            log("❌ No valid audio file found.")
            return {"audio_valid": False, "audio_base64": ""}

        try:
            with open(self.audio_input, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")

            log(f"✅ Audio parsed successfully: {Path(self.audio_input).name}")
            return {
                "audio_valid": True,
                "audio_name": Path(self.audio_input).name,
                "audio_base64": encoded
            }

        except Exception as e:
            log(f"⚠️ Audio parse failed: {e}")
            return {"audio_valid": False, "audio_base64": ""}





    # -------------------------
    # 输出统一结构
    # -------------------------
    def to_dict(self) -> Dict[str, Any]:
        """输出标准化输入结构"""
        parsed = {
            "text": self.parse_text(),
            "image": self.parse_image(),
            "audio": self.parse_audio()
        }
        parsed["input_summary"] = self._summarize(parsed)
        self._log_input(parsed)
        return parsed

    @staticmethod
    def _summarize(parsed: Dict[str, Any]) -> str:
        """生成输入概览"""
        parts = []
        if parsed["text"]["text_valid"]:
            parts.append("Text ✓")
        if parsed["image"]["image_valid"]:
            parts.append("Image ✓")
        if parsed["audio"]["audio_valid"]:
            parts.append("Audio ✓")
        return " | ".join(parts) if parts else "No valid input"

    @staticmethod
    def _log_input(parsed: Dict[str, Any]):
        """保存输入结构日志"""
        os.makedirs("output/logs", exist_ok=True)
        with open("output/logs/last_input.json", "w", encoding="utf-8") as f:
            json.dump(parsed, f, ensure_ascii=False, indent=2)


# -------------------------
# 🔧 快捷函数接口
# -------------------------
def parse_multimodal_input(
    text: Optional[str],
    image: Any,
    audio: Any
) -> Dict[str, Any]:
    """兼容 Gradio 的统一输入解析函数"""
    instance = MultiModalInput(
        text=text,
        image_input=image,
        audio_input=audio
    )
    return instance.to_dict()
