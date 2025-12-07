#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成应用图标
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_application_icon(output_path="icon.ico"):
    """创建应用图标"""
    try:
        # 创建不同尺寸的图标
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        
        # 创建图标
        images = []
        for size in sizes:
            img = Image.new('RGBA', size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # 绘制Windows蓝色背景
            draw.rectangle([(0, 0), size], fill=(0, 120, 215))
            
            # 绘制白色文字"I"
            try:
                font_size = int(size[0] * 0.6)
                font = ImageFont.truetype("arial.ttf", font_size)
            except IOError:
                font = ImageFont.load_default()
            
            text = "I"
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            text_x = (size[0] - text_width) // 2
            text_y = (size[1] - text_height) // 2 - text_bbox[1]
            
            draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)
            
            # 添加到列表
            images.append(img)
        
        # 保存为ICO文件
        images[0].save(
            output_path,
            format="ICO",
            sizes=sizes
        )
        
        print(f"应用图标已创建: {output_path}")
        return True
        
    except Exception as e:
        print(f"创建图标失败: {str(e)}")
        return False


if __name__ == "__main__":
    create_application_icon()