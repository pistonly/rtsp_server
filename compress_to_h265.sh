#!/bin/bash

# 定义输出文件名
output_file="output.h265"

# 定义输入图片文件夹
input_dir="tmp"

# 清空已有的输出文件
> "$output_file"

# 遍历所有jpg文件
for img in "$input_dir"/*.jpg; do
    # 打印当前处理的图片名称
    echo "正在处理: $img"
    
    # 使用FFmpeg将每个jpg文件转换为h265编码并追加到输出文件中
    ffmpeg -y -i "$img" -c:v libx265 -profile:v main10 -pix_fmt yuvj420p -colorspace bt709 -vf "scale=3840:2160" -r 25 -f hevc - | cat >> "$output_file"
done

echo "所有图片已压缩并合并为 $output_file"
