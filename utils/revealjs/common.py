import os
import subprocess
import logging

logger = logging.getLogger(__name__)


def git_clone(repo_url, target_directory):
    cwd = os.getcwd()
    # 切换到目标目录
    os.chdir(target_directory)

    # 执行git clone命令
    try:
        subprocess.run(["git", "clone", repo_url], check=True)
        logger.error("Git clone completed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Git clone failed with return code {e.returncode}: {e.output}")
    finally:
        os.chdir(cwd)


def clone_revealjs():
    # Git仓库的URL
    repo_url = "https://github.com/hakimel/reveal.js.git"
    # 目标目录路径
    target_directory = os.path.join(os.getcwd(), "./utils/revealjs/reveal_src")
    # 确保目标目录存在
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    git_clone(repo_url, target_directory)
