# A-ASCLL-Art-Converter
这是一个可以把图片转换为字符画的前端工具.

这是我尝试用vibe coding工具的练手项目，我尝试使用ai工具让他更新的更好用。

## 核心功能
- 拖拽/点击上传图片
- 6 种渲染风格：经典ASCII、方块像素、线稿素描、数字矩阵、密集细节、极简线条
- 输出宽度 40~500 可调
- 对比度 0.5~4.0 可调
- 预览字体 0.5~14px 可调
- 反色模式（默认开启，浅字符/深背景）
- 彩色模式（保留原图颜色，Canvas 渲染）
- 导出格式：纯文本 .txt、ANSI 转义码 .ansi、独立 .html


## 技术要点

### 渲染管线
1. drawImage → 缩放到目标尺寸
2. convertToGrayscale → 灰度提取
3. detectEdges（仅线稿风格）→ Sobel 边缘检测
4. applyContrast → 对比度调整
5. 字符映射：灰度 0~255 → 字符集索引
6. 输出：纯文本 / ANSI / Canvas / HTML

### Canvas 彩色渲染（drawToCanvas）
- 使用 measureText 获取设备真实字符宽度（兼容手机）
- 离屏 Canvas 预渲染字符掩码（每个字符只渲染一次）
- fillRect 铺深色背景 → ImageData 叠加彩色字符像素
- 单次 putImageData 输出（高性能）
- CSS width/height 控制显示尺寸（保证布局正确、可滚动）

### ANSI 输出（renderANSI）
- 批量合并同色相邻字符（大幅压缩输出体积）
- 仅在颜色变化时输出 \x1b[38;2;R;G;Bm 转义码
- 适用于 Windows Terminal / iTerm2 / kitty 等真彩色终端

### 国际化（i18n）
- I18N 对象管理中英文字符串
- data-i18n HTML 属性标记需翻译的元素
- applyI18n() 统一更新全界面文字
- 覆盖：按钮、标签、提示栏、Toast、弹窗

### 缩放公式
- 线性映射：displaySize = sliderValue / 4
- 范围：slider 0.5→0.125x, 4→1x, 14→3.5x

## 早期脚本说明
三个 _early.py 脚本是开发探索阶段的产物：
- ascii_art_early.py：生成经典 ASCII（200宽）→ leimu_ascii.txt
- make_ascii_early.py：生成正色/反色/方块三个版本 + 静态HTML查看器
- show_image_early.py：边缘检测 + 高对比度两种风格

这些功能已全部集成到 ascii_converter.html 网页中，
Python 脚本仅保留作为参考，不再维护。


  起初只是想把一张图片转化为字符画，于是诞生了leimu_ascii~

  立刻体验→
# [web体验](https://git.624316.xyz/)


  ( ⌯' '⌯)


