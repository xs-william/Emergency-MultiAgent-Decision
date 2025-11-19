# ==========================================
# Module: SAM2 Preprocessor
# File: executor/sam2_preprocessor.py
# ==========================================
# 🧩 功能概述：
#   - 集成 SAM2 模型进行图像分割预处理；
#   - 将全图像输入转换为分割掩码输出；
# ==========================================

import torch
from sam2.sam2_image_predictor import SAM2ImagePredictor
import matplotlib.pyplot as plt


class SAM2Preprocessor:
    """SAM2 图像分割预处理器"""

    def __init__(self):
        self.predictor = SAM2ImagePredictor.from_pretrained("facebook/sam2-hiera-large")

    def preprocess_image(self, image) -> dict:
        """
        使用 SAM2 对图像进行分割预处理
        :param image_path: 输入图像路径
        :param prompts: 分割提示信息（如点、框等）
        :return: 分割结果
        """
        with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16):
            self.predictor.set_image(image)
            masks, scores, logits = self.predictor.predict(
                point_coords=None,
                point_labels=None,
                box=None,
                multimask_output=True,
            )
        return {"masks": masks, "scores": scores, "logits": logits}


def sam2_image_preprocess(image) -> dict:
    """对全图像进行 SAM2 预处理，返回分割掩码等结果"""
    preprocessor = SAM2Preprocessor()
    return preprocessor.preprocess_image(image)


if __name__ == '__main__':
    # 测试用例
    from PIL import Image
    image_path = "test/example1/image1.png"
    image = Image.open(image_path).convert("RGB")

    sam2_result = sam2_image_preprocess(image)
    print(sam2_result)
    # 可视化结果，分区展示
    masks = sam2_result["masks"]
    for i, mask in enumerate(masks):
        plt.subplot(1, len(masks), i + 1)
        plt.imshow(mask, cmap='gray')
        plt.axis('off')
    plt.show()
