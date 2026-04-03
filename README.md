# acfun-video-downloader
AcFun视频流采集工具，自动下载m3u8分片并合并为mp4

# AcFun 视频流采集器

自动下载 AcFun 视频（m3u8 + ts 分片）并合并为 MP4。

## 功能特点

- 输入视频 ID（如 `ac48372480`），自动获取 m3u8 地址
- 下载所有 ts 分片到临时缓存
- 自动调用 ffmpeg 合并为单个 MP4 文件
- 合并后自动清理缓存，节省空间
- 视频文件名自动使用原标题（过滤非法字符）

## 技术栈

- Python 3.x
- requests（网络请求）
- subprocess（调用 ffmpeg）
- ffmpeg（外部工具，需单独安装）

## 安装与使用

### 1. 安装 Python 依赖

```bash
pip install requests

2. 安装 ffmpeg
Windows: 从 ffmpeg.org 下载，解压后将 bin 目录添加到系统 PATH，或在代码中指定 ffmpeg.exe 的绝对路径。

macOS: brew install ffmpeg

Linux: sudo apt install ffmpeg

3. 修改配置
打开脚本，将 ffmpeg_path 变量改为你本地的 ffmpeg 路径：
ffmpeg_path = r'你的ffmpeg路径\bin\ffmpeg.exe'

4. 运行
python
from acfun流媒体视频完整采集 import Acfun

ac = Acfun()
ac.run('ac48372480')   # 替换为你想下载的视频ID


输出
脚本会在 D:/PycharmProjects/demo/文件保存/ 目录（自己改一个指定的路径）下生成 视频标题.mp4。

注意事项
仅限个人学习使用，请勿侵犯版权。

脚本中的 cookies 和 headers 可能会过期，如遇问题可更新为最新的






3. 修改配置
打开脚本，将 ffmpeg_path 变量改为你本地的 ffmpeg 路径：
