# HTML Previewer

一个支持中英文界面切换的桌面HTML预览与导出小工具，基于 PyQt6 开发。

## 功能特色

- 左侧输入/粘贴HTML代码，右侧实时预览网页效果
- 支持保存HTML源码、导出网页为PDF
- 支持拖拽HTML文件直接打开
- 支持中英文界面自动切换和手动切换
- 可自定义保存路径
- "关于我"菜单含作者信息与免责声明

## 使用方法

1. 安装依赖（推荐用虚拟环境）：
   ```bash
   pip install -r requirements.txt
   ```
2. 运行程序：
   ```bash
   python app.py
   ```
3. 打包为exe（可选）：
   ```bash
   pip install pyinstaller
   pyinstaller --noconsole --onefile app.py
   ```
   打包后在 `dist/app.exe`，可直接运行。

## 目录结构

- `app.py`         主程序
- `requirements.txt` 依赖列表
- `README.md`      项目说明
- `.gitignore`     Git忽略配置

## 免责声明

个人爱好开发，随便使用，电脑炸了自负！
小工具由 Lanlic Yuen (1Plab CE) V 1.0  
有问题可联系：lanlic@hotmail.com  
未必回，但未必不看。 