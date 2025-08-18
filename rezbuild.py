#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import shutil
import subprocess
import tarfile

def run_cmd(cmd, cwd=None):
    print(f"[RUN] {cmd}")
    subprocess.run(cmd, cwd=cwd, shell=True, check=True)

def clean_build_dir(build_path):
    if os.path.isdir(build_path):
        print(f"🧹 Cleaning build dir (preserve build.rxt): {build_path}")
        for item in os.listdir(build_path):
            if item.endswith(".rxt"):
                continue
            path = os.path.join(build_path, item)
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    else:
        os.makedirs(build_path, exist_ok=True)

def clean_install_dir(install_path):
    if os.path.isdir(install_path):
        print(f"🧹 Removing install dir: {install_path}")
        shutil.rmtree(install_path)

def copy_package_py(source_path, install_path):
    src = os.path.join(source_path, "package.py")
    dst = os.path.join(install_path, "package.py")
    if os.path.isfile(src):
        print(f"📄 Copying package.py → {dst}")
        shutil.copy(src, dst)

def write_build_marker(build_path):
    marker = os.path.join(build_path, "build.rxt")
    with open(marker, "a"):
        pass
    print(f"📝 Touching build marker: {marker}")

def write_variant_file(build_path):
    variant = os.path.join(build_path, "variant.json")
    print(f"📄 Writing variant.json → {variant}")
    with open(variant, "w") as f:
        f.write("{}\n")

def extract_tarball(tar_path, dest):
    print(f"📦 Extracting {tar_path} → {dest}")
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(dest)

def build(source_path, build_path, install_path, targets):
    version       = os.environ.get("REZ_BUILD_PROJECT_VERSION", "20.9.0")
    tarball       = os.path.join(source_path, "source", f"node-v{version}.tar.gz")
    fixed_install = f"/core/Linux/APPZ/packages/nodejs/{version}"
    extract_dir   = os.path.join(build_path, f"node-v{version}")

    print(f"📦 Tarball:    {tarball}")
    print(f"🏗️  Build dir: {build_path}")
    print(f"📂 Install dir: {fixed_install}")

    # install-only 모드
    if "install" in targets:
        if not os.path.isdir(extract_dir):
            # full build 없이 바로 설치 시 소스 추출 + 빌드
            clean_build_dir(build_path)
            os.makedirs(build_path, exist_ok=True)
            extract_tarball(tarball, build_path)
            os.chdir(extract_dir)
            run_cmd(f"./configure --prefix={fixed_install}")
            run_cmd("make -j$(nproc)")
        clean_install_dir(fixed_install)
        os.chdir(extract_dir)
        run_cmd("make install")
        copy_package_py(source_path, fixed_install)
        write_variant_file(build_path)
        print("✅ nodejs install complete.")
        return

    # full build
    clean_build_dir(build_path)
    clean_install_dir(fixed_install)
    os.makedirs(build_path, exist_ok=True)

    extract_tarball(tarball, build_path)
    os.chdir(extract_dir)
    run_cmd(f"./configure --prefix={fixed_install}")
    run_cmd("make -j$(nproc)")

    write_build_marker(build_path)
    write_variant_file(build_path)
    print("✅ nodejs build complete.")

if __name__ == "__main__":
    build(
        source_path  = os.environ["REZ_BUILD_SOURCE_PATH"],
        build_path   = os.environ["REZ_BUILD_PATH"],
        install_path = os.environ["REZ_BUILD_INSTALL_PATH"],
        targets      = sys.argv[1:]
    )

