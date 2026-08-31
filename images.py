import os
import re
import shutil

# Paths
posts_dir = r"E:\zeblog\zeblog\content\post" 
attachments_dir = r"E:\HuaweiMoveData\Users\Administrator\Documents\Obsidian Vault\attachments"
static_images_dir = r"E:\zeblog\zeblog\static\images"

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
        
        # 第一步：找出所有连续的图片（同一段落中）
        # 匹配连续的 ![[图片.png|宽度]] 格式
        image_pattern = r'!\[\[([^\]|]+)(?:\|([^\]]*))?\]\]'
        
        # 找出所有图片及其位置
        images = re.findall(image_pattern, content)
        
        if images:
            print(f"找到 {len(images)} 张图片")
        else:
            print("未找到图片")
            continue
        
        # 第二步：处理图片组（将连续图片组合成一行）
        # 按段落分割内容
        paragraphs = content.split('\n\n')
        new_paragraphs = []
        
        for para in paragraphs:
            # 检查这个段落是否包含多张图片
            para_images = re.findall(image_pattern, para)
            
            if len(para_images) > 1:
                # 多张图片在同一段落 -> 组合成一行
                print(f"  发现 {len(para_images)} 张连续图片，组合成一行")
                
                # 构建水平排列的 HTML
                images_html = []
                for image, width in para_images:
                    image_url = image.replace(' ', '%20')
                    if width and width.isdigit():
                        # 使用 figure shortcode 并指定宽度
                        img_tag = f'{{{{< figure src="/images/{image_url}" alt="{image}" width="{width}" class="inline-image" >}}}}'
                    else:
                        img_tag = f'{{{{< figure src="/images/{image_url}" alt="{image}" class="inline-image" >}}}}'
                    images_html.append(img_tag)
                    
                    # 复制图片
                    image_source = os.path.join(attachments_dir, image)
                    if os.path.exists(image_source):
                        dest_path = os.path.join(static_images_dir, image)
                        shutil.copy(image_source, dest_path)
                        total_copied += 1
                        print(f"    ✓ 复制: {image}")
                
                # 包装在 flex 容器中
                combined = f'\n<div style="display:flex; gap:10px; justify-content:center; flex-wrap:wrap;">\n'
                combined += '\n'.join(images_html)
                combined += '\n</div>\n'
                
                new_paragraphs.append(combined)
            else:
                # 单张图片或没有图片，单独处理
                for image, width in para_images:
                    image_url = image.replace(' ', '%20')
                    if width and width.isdigit():
                        img_tag = f'{{{{< figure src="/images/{image_url}" alt="{image}" width="{width}" >}}}}'
                    else:
                        img_tag = f'{{{{< figure src="/images/{image_url}" alt="{image}" >}}}}'
                    
                    # 替换
                    pattern = r'!\[\[(' + re.escape(image) + r')(?:\|[^\]]*)?\]\]'
                    para = re.sub(pattern, img_tag, para)
                    
                    # 复制图片
                    image_source = os.path.join(attachments_dir, image)
                    if os.path.exists(image_source):
                        dest_path = os.path.join(static_images_dir, image)
                        shutil.copy(image_source, dest_path)
                        total_copied += 1
                        print(f"  ✓ 复制: {image}")
                
                new_paragraphs.append(para)
        
        # 重新组合内容
        content = '\n\n'.join(new_paragraphs)
        
        # 写回文件
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

print(f"\n{'='*50}")
print(f"处理完成！")
print(f"处理文件数: {total_files}")
print(f"复制图片数: {total_copied}")