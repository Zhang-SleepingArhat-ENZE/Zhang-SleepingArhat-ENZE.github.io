# import os
# import re
# import shutil
 
# # Paths (using raw strings to handle Windows backslashes correctly)
# posts_dir = r"E:\zeblog\zeblog\content\post" 
# attachments_dir = r"E:\HuaweiMoveData\Users\Administrator\Documents\Obsidian Vault\attachments"
# static_images_dir = r"E:\zeblog\zeblog\static\images"

# # Step 1: Process each markdown file in the posts directory
# for filename in os.listdir(posts_dir):
#     if filename.endswith(".md"):
#         filepath = os.path.join(posts_dir, filename)
        
#         with open(filepath, "r", encoding="utf-8") as file:
#             content = file.read()
        
#         # Step 2: Find all image links in the format ![Image Description](/images/Pasted%20image%20...%20.png)
#         images = re.findall(r'\[\[([^]]*\.png)\]\]', content)
        
#         # Step 3: Replace image links and ensure URLs are correctly formatted
#         for image in images:
#             # Prepare the Markdown-compatible link with %20 replacing spaces
#             markdown_image = f"![Image Description](/images/{image.replace(' ', '%20')})"
#             content = content.replace(f"[[{image}]]", markdown_image)
            
#             # Step 4: Copy the image to the Hugo static/images directory if it exists
#             image_source = os.path.join(attachments_dir, image)
#             if os.path.exists(image_source):
#                 shutil.copy(image_source, static_images_dir)

#         # Step 5: Write the updated content back to the markdown file
#         with open(filepath, "w", encoding="utf-8") as file:
#             file.write(content)

# print("Markdown files processed and images copied successfully.")

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
        
        # 匹配 Obsidian 格式
        images = re.findall(r'!\[\[([^\]|]+)(?:\|[^\]]*)?\]\]', content)
        
        if images:
            print(f"找到 {len(images)} 张图片: {images}")
        else:
            print("未找到图片")
            continue
        
        for image in images:
            image_url = image.replace(' ', '%20')
            
            # ===== 选择一种格式 =====
            
            # 方式A: 使用 figure shortcode（推荐，最可靠）
            markdown_image = f'\n{{{{< figure src="/images/{image_url}" alt="{image}" >}}}}\n'
            
            # 方式B: 使用 HTML img 标签
            # markdown_image = f'\n<img src="/images/{image_url}" alt="{image}">\n'
            
            # 方式C: 使用带样式的 HTML（可控制大小）
            # markdown_image = f'\n<img src="/images/{image_url}" alt="{image}" style="max-width:100%; height:auto;">\n'
            
            # 方式D: 标准 Markdown（需要 unsafe=true）
            # markdown_image = f"![{image}](/images/{image_url})"
            # =========================
            
            pattern = r'!\[\[(' + re.escape(image) + r')(?:\|[^\]]*)?\]\]'
            content = re.sub(pattern, markdown_image, content)
            
            # 复制图片
            image_source = os.path.join(attachments_dir, image)
            if os.path.exists(image_source):
                dest_path = os.path.join(static_images_dir, image)
                shutil.copy(image_source, dest_path)
                total_copied += 1
                print(f"  ✓ 复制: {image}")
            else:
                print(f"  ✗ 文件不存在: {image_source}")
        
        # 清理多余空行
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

print(f"\n{'='*50}")
print(f"处理完成！")
print(f"处理文件数: {total_files}")
print(f"复制图片数: {total_copied}")
print(f"图片目录: {static_images_dir}")