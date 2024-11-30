import os
import subprocess
import argparse
import sys
from tqdm import tqdm
import platform
import shutil
from datetime import datetime

def convert_nef_to_jpg(base_dir, use_magick=True):
    """
    指定されたディレクトリ内のすべてのNEFファイルをJPEGに変換し、
    作成日と修正日を元のNEFファイルと同じに設定します。
    既存のJPEGファイルが存在する場合は上書きされます。
    """
    # ImageMagickのコマンドを設定
    if use_magick:
        imagemagick_cmd = 'magick'
    else:
        imagemagick_cmd = 'convert'
    
    # ExifToolのコマンド
    exiftool_cmd = 'exiftool'
    
    # ベースディレクトリの存在を確認
    if not os.path.isdir(base_dir):
        print(f"Error: 指定されたディレクトリが存在しません: {base_dir}")
        sys.exit(1)
    
    # NEFファイルをリストアップ
    nef_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith('.nef'):
                nef_path = os.path.join(root, file)
                nef_files.append(nef_path)
    
    if not nef_files:
        print("指定されたディレクトリ内にNEFファイルが見つかりませんでした。")
        sys.exit(0)
    
    # 進捗バーを初期化
    for nef_path in tqdm(nef_files, desc="Processing NEF files", unit="file"):
        jpg_path = os.path.splitext(nef_path)[0] + '.jpg'
        
        # JPEGへの変換
        try:
            # mogrifyは指定した形式でファイルを変換し、同名の他形式ファイルを作成します
            subprocess.run([imagemagick_cmd, 'mogrify', '-format', 'jpg', nef_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(f"\nError converting {nef_path}: {e}")
            continue
        
        # Exif情報のコピー
        try:
            # ExifToolを使用してEXIF情報をコピー
            subprocess.run([exiftool_cmd, '-TagsFromFile', nef_path, '-all:all', '-overwrite_original', jpg_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(f"\nError copying EXIF data for {jpg_path}: {e}")
            continue
        
        # ファイルの作成日と修正日をコピー
        try:
            # NEFファイルのタイムスタンプを取得
            stat_info = os.stat(nef_path)
            atime = stat_info.st_atime  # アクセス時刻
            mtime = stat_info.st_mtime  # 修正時刻
            
            # JPEGファイルのタイムスタンプを設定
            os.utime(jpg_path, (atime, mtime))
            
            # macOSの場合、作成日（birth time）も設定
            if platform.system() == 'Darwin':
                # ExifToolを使用してDateTimeOriginalを取得
                result = subprocess.run([exiftool_cmd, '-DateTimeOriginal', '-s', '-s', '-s', nef_path],
                                        stdout=subprocess.PIPE, text=True)
                datetime_original = result.stdout.strip()
                if datetime_original:
                    # DateTimeOriginalを「YYYY:MM:DD HH:MM:SS」から「MM/DD/YYYY HH:MM:SS AM/PM」形式に変換
                    try:
                        dt = datetime.strptime(datetime_original, '%Y:%m:%d %H:%M:%S')
                        formatted_date = dt.strftime('%m/%d/%Y %I:%M:%S %p')
                        # SetFileコマンドで作成日を設定
                        subprocess.run(['SetFile', '-d', formatted_date, jpg_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    except ValueError as ve:
                        print(f"\nError parsing DateTimeOriginal for {jpg_path}: {ve}")
        except subprocess.CalledProcessError as e:
            print(f"\nError setting file times for {jpg_path}: {e}")
            continue
        except Exception as e:
            print(f"\nUnexpected error for {jpg_path}: {e}")
            continue
        
        print(f"Successfully processed: {jpg_path}\n")

def main():
    parser = argparse.ArgumentParser(description="Convert NEF files to JPEG, overwrite existing JPEGs, preserve EXIF data and file timestamps, and display progress.")
    parser.add_argument('directory', help="Base directory to search for NEF files.")
    parser.add_argument('--use-magick', action='store_true', help="Use 'magick' command instead of 'convert'. Required for ImageMagick 7+.")
    
    args = parser.parse_args()
    
    # Check if ImageMagick is installed
    imagemagick_cmd = 'magick' if args.use_magick else 'convert'
    if not shutil.which(imagemagick_cmd):
        print(f"Error: {imagemagick_cmd} コマンドが見つかりません。ImageMagickが正しくインストールされ、PATHに含まれていることを確認してください。")
        sys.exit(1)
    
    # Check if ExifTool is installed
    if not shutil.which('exiftool'):
        print("Error: exiftool コマンドが見つかりません。ExifToolが正しくインストールされ、PATHに含まれていることを確認してください。")
        sys.exit(1)
    
    convert_nef_to_jpg(args.directory, use_magick=args.use_magick)

if __name__ == "__main__":
    main()
