#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图标处理模块 - 封装图标转换和处理功能
"""

import os
from PIL import Image, ImageDraw
from config import TARGET_SIZES


def process_icon(input_path, output_dir):
    """处理图标为系统格式"""
    try:
        # 输出文件路径
        output_ico = os.path.join(output_dir, 'boot_icon.ico')
        output_png = os.path.join(output_dir, 'boot_icon.png')
        
        # 打开并处理图片
        with Image.open(input_path) as img:
            # 验证图片有效性
            img.verify()
            
            # 重新打开图片
            img = Image.open(input_path)
            
            # 检查图片尺寸
            if img.size[0] < 128 or img.size[1] < 128:
                raise ValueError("图片尺寸过小。建议使用至少256x256像素的图片")
            
            # 转换为RGBA
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # 处理不同尺寸的图标
            processed_images = []
            for size in TARGET_SIZES:
                rounded_icon = create_rounded_icon(img, size)
                processed_images.append(rounded_icon)
            
            # 保存为PNG（用于预览）
            processed_images[0].save(output_png, 'PNG')
            
            # 保存为ICO（多尺寸）
            processed_images[0].save(
                output_ico, 
                'ICO', 
                sizes=[(size[0], size[1]) for size in TARGET_SIZES]
            )
        
        return output_ico, output_png
        
    except FileNotFoundError:
        raise FileNotFoundError(f"图片文件不存在: {input_path}")
    except ValueError as e:
        raise ValueError(f"图片格式错误: {str(e)}")
    except PermissionError:
        raise PermissionError(f"无法写入文件到: {output_dir}。请检查权限设置")
    except Exception as e:
        raise Exception(f"处理图标时出错: {str(e)}")


def create_rounded_icon(image, size):
    """创建圆形图标"""
    try:
        # 调整尺寸
        resized = image.resize(size, Image.Resampling.LANCZOS)
        
        # 创建圆形蒙版
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse([(0, 0), size], fill=255)
        
        # 应用圆形
        rounded = Image.new('RGBA', size)
        rounded.paste(resized, mask=mask)
        
        return rounded
        
    except Exception as e:
        raise Exception(f"创建圆形图标失败: {str(e)}")


def create_preview_icon(image_path, size=(100, 100)):
    """创建预览图标"""
    try:
        with Image.open(image_path) as img:
            # 转换为RGBA
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # 创建圆形图标
            rounded = create_rounded_icon(img, size)
            
            return rounded
            
    except Exception as e:
        raise Exception(f"创建预览图标失败: {str(e)}")


def check_image_validity(image_path):
    """检查图片有效性"""
    try:
        with Image.open(image_path) as img:
            # 检查是否为有效的图片
            img.verify()
            return True
    except Exception as e:
        return False


def get_image_info(image_path):
    """获取图片信息"""
    try:
        with Image.open(image_path) as img:
            return {
                "size": img.size,
                "format": img.format,
                "mode": img.mode,
                "width": img.width,
                "height": img.height
            }
    except Exception as e:
        raise Exception(f"获取图片信息失败: {str(e)}")
