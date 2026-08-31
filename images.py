import os
import re
import shutil

# Paths
posts_dir = r"E:\zeblog\zeblog\content\post" 
attachments_dir = r"E:\HuaweiMoveData\Users\Administrator\Documents\Obsidian Vault\attachments"
static_images_dir = r"E:\zeblog\zeblog\static\images"

# 确保目标目录存在
os.makedirs(static_images_dir, exist_ok=True)

total_copied = 0
total_files = 0

for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        total_files += 1
        
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
        
        print(f"\n处理文件: {filename}")
        
        # 匹配 Obsidian 格式，捕获图片名和宽度参数
        # ![[图片名.png|宽度]] 或 ![[图片名.png]]
        images = re.findall(r'!\[\[([^\]|]+)(?:\|([^\]]*))?\]\]', content)
        
        if images:
            print(f"找到 {len(images)} 张图片")
            for img, width in images:
                print(f"  - {img} (宽度: {width if width else '默认'})")
        else:
            print("未找到图片")
            continue
        
        for image, width_param in images:
            # 处理 URL 编码
            image_url = image.replace(' ', '%20')
            
            # 根据是否有宽度参数生成不同的格式
            if width_param and width_param.isdigit():
                # 有宽度参数：使用 figure shortcode 并指定宽度
                markdown_image = f'\n{{{{< figure src="/images/{image_url}" alt="{image}" width="{width_param}" >}}}}\n'
            else:
                # 无宽度参数：使用标准 Markdown 格式（如果 unsafe=true）或 figure shortcode
                # 方式1: 标准 Markdown（需要 unsafe=true）
                # markdown_image = f"\n![{image}](/images/{image_url})\n"
                
                # 方式2: figure shortcode（不需要 unsafe）
                markdown_image = f'\n{{{{< figure src="/images/{image_url}" alt="{image}" >}}}}\n'
            
            # 替换原格式
            pattern = r'!\[\[(' + re.escape(image) + r')(?:\|[^\]]*)?\]\]'
            content = re.sub(pattern, markdown_image, content)
            
            # 复制图片文件
            image_source = os.path.join(attachments_dir, image)
            if os.path.exists(image_source):
                dest_path = os.path.join(static_images_dir, image)
                shutil.copy(image_source, dest_path)
                total_copied += 1
                if width_param:
                    print(f"  ✓ 复制: {image} (宽度: {width_param}px)")
                else:
                    print(f"  ✓ 复制: {image} (原始尺寸)")
            else:
                print(f"  ✗ 文件不存在: {image_source}")
        
        # 清理多余的空行
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # 写回文件
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

print(f"\n{'='*50}")
print(f"处理完成！")
print(f"处理文件数: {total_files}")
print(f"复制图片数: {total_copied}")
print(f"图片目录: {static_images_dir}")