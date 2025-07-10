AI 学习教练 (AI Learning Coach) 这是一个基于大语言模型（LLM）的个性化学习辅助系统 DEMO。它通过深度诊断评估用户的学习特质，并为用户的特定学习任务生成定制化的学习材料。

项目结构树 /adaptive-learning-assistant |-- backend/ # 后端应用目录 | |-- app/ | | |-- api/ | | | |-- init.py | | | |-- endpoints.py # FastAPI 的所有 API 路由 | | |-- core/ | | | |-- init.py | | | |-- config.py # 应用配置（模型名称、路径等） | | | |-- llm_client.py # 与 Ollama LLM 交互的客户端 | | |-- services/ | | | |-- init.py | | | |-- pdf_generator.py # 从 JSON 生成 PDF 学习资料的服务 | | | |-- profile_manager.py# 管理用户画像的创建与获取 | | | |-- task_manager.py # 管理学习任务的创建与获取 | | |-- prompts/ | | | |-- init.py | | | |-- profile_prompts.py# 用于生成用户画像的 Prompt 模板 | | | |-- task_prompts.py # 用于生成学习资料的 Prompt 模板 | | |-- init.py | | |-- main.py # FastAPI 应用主入口 | |-- data/ # 数据存储目录 (需手动创建) | | |-- user_profiles/ # 存储生成的用户画像 JSON 文件 | | |-- learning_materials/ # 存储生成的学习任务 PDF 和 JSON | |-- .gitignore | |-- requirements.txt # Python 依赖项 | |-- run.py # 启动后端服务的脚本 | |-- frontend/ # 前端应用目录 | |-- index.html # 核心前端文件 (Vue.js 单页面应用) | |-- .gitignore # 全局 .gitignore |-- README.md # 本文件

先决条件 在开始之前，请确保您的系统已经安装了以下软件：
Conda (或 Miniconda): 用于管理Python环境。如果您没有安装，可以从 Anaconda 官网 下载。

Ollama: 用于在本地运行大语言模型。请访问 Ollama 官网 下载并安装。

LaTeX 发行版: 用于从代码生成精美的PDF文件。这是必须的步骤。

Windows: 安装 MiKTeX。在安装过程中，选择“为所有用户安装”并允许“自动安装缺失的软件包”。

macOS: 安装 MacTeX。这是一个较大的安装包，但包含了所有需要的工具。

Linux (Debian/Ubuntu): 运行 sudo apt-get install texlive-full。

下载并运行 Ollama 模型 安装好 Ollama 后，打开您的终端（或命令提示符），运行以下命令来下载并运行我们项目所需的模型（以qwen2:7b为例，您也可以换成qwen3:8b-q8_0或其他模型，但需同步修改 backend/app/core/config.py 中的 OLLAMA_MODEL_NAME）。
ollama run qwen2:7b

当您看到 ">>> Send a message (/? for help)" 的提示时，表示模型已成功在后台运行。您可以关闭这个终端窗口，Ollama服务会继续在后台运行。

创建项目文件 创建一个名为 adaptive-learning-assistant 的主文件夹。
在主文件夹内，根据上面的项目结构树创建所有子文件夹（如 backend, frontend, backend/app, backend/app/api 等）。

将上面代码块中的代码，一一复制并保存到对应的文件中。例如，将后端代码块中的 # backend/run.py 部分保存为 backend/run.py 文件。

配置 Conda 环境并安装依赖 打开终端 (Anaconda Prompt on Windows, or Terminal on macOS/Linux)。
导航到项目根目录 adaptive-learning-assistant。

cd path/to/your/adaptive-learning-assistant

创建新的 Conda 环境: 我们创建一个名为 ai_coach 的新环境，并指定使用 Python 3.10。

conda create --name ai_coach python=3.10 -y

激活 Conda 环境:

conda activate ai_coach

激活后，您会看到终端提示符前面有 (ai_coach) 字样。

安装 Python 依赖: 导航到 backend 目录并使用 pip 安装 requirements.txt 中列出的所有库。

cd backend pip install -r requirements.txt

运行项目 现在，一切准备就绪！
启动后端服务器: 确保您仍处于 backend 目录下，且 (ai_coach) 环境已激活。然后运行 run.py 脚本。

python run.py

如果一切顺利，您会看到类似下面的输出，表示服务器已在 http://127.0.0.1:8000 上运行：

INFO: Started server process [xxxxx] INFO: Waiting for application startup. INFO: Application startup complete. INFO: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)

打开前端页面:

不要关闭正在运行后端服务器的终端。

在您的文件浏览器中，找到 frontend/index.html 文件。

直接用您的网页浏览器（推荐 Chrome 或 Firefox）打开这个 index.html 文件。

现在，您应该可以在浏览器中看到“AI学习教练”的界面了！它会首先检查是否存在用户画像，如果没有，则会引导您完成评估问卷。享受您的个性化学习之旅吧！