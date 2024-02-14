import os
import time
import subprocess

build_count = 3
project_dir = os.path.join(os.environ["HOME"], "work/KmmGithubSearch")
commits = ["main"]  # ["main", "b92a835c4fdb35fbf4f77e86559bd2d50f334cc0"]
pre_build_command = """
./gradlew clean && cd iosApp && bundle exec fastlane clean
"""
build_command = """
cd iosApp && bundle exec fastlane debug_build
"""


def run_command(command: str):
    subprocess.run(command, shell=True, check=True)


build_times = []

os.chdir(project_dir)
for commit in commits:
    build_times.append([])
    for i in range(build_count + 1):
        run_command(f"git checkout {commit}")
        run_command(pre_build_command)
        start_time = time.time()
        run_command(build_command)
        end_time = time.time()
        build_time = end_time - start_time
        if i >= 1:
            build_times[-1].append(build_time)

print(build_times)
