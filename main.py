import os
import time
import subprocess
import polars as pl

build_count = 10
project_dir = os.path.join(os.environ["HOME"], "work/KmmGithubSearch")
commits = ["main", "b92a835c"]
pre_build_command = """
./gradlew clean && cd iosApp && bundle exec fastlane clean
"""
build_command = """
cd iosApp && bundle exec fastlane debug_build
"""


def run_command(command: str):
    subprocess.run(command, shell=True, check=True)


build_times = {}
original_dir = os.getcwd()
os.chdir(project_dir)
for commit in commits:
    build_times[commit] = []
    for i in range(build_count + 1):
        run_command(f"git checkout {commit}")
        run_command(pre_build_command)
        start_time = time.time()
        run_command(build_command)
        end_time = time.time()
        build_time = end_time - start_time
        if i >= 1:
            build_times[commit].append(build_time)

df = pl.DataFrame(build_times)
os.chdir(original_dir)
df.write_excel("build_time.xlsx")
