# pycaps2.py
import subprocess
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Add captions using PyCaps")
    parser.add_argument("--input", type=str, required=True, help="Path to the video file (e.g. output/broll_no_caps11.mp4)")
    parser.add_argument("--template", type=str, default="templates/centered", help="PyCaps template folder")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: File not found → {input_path}")
        return

    output_path = input_path.with_name(f"{input_path.stem}_captioned.mp4")

    print(f"Adding captions...")
    print(f"   Input: {input_path}")
    print(f"   Template: {args.template}")
    print(f"   Output: {output_path}")

    result = subprocess.run([
        "pycaps", "render",
        "--input", str(input_path),
        "--template", args.template,
        "--output", str(output_path)
    ], capture_output=True, text=True)

    if result.returncode == 0:
        print("CAPTIONS ADDED SUCCESSFULLY!")
        print(f"Final video → {output_path}")
        print(f"OUTPUT_PATH={output_path}")  # Optional: for master script
    else:
        print("PyCaps failed:")
        print(result.stderr)

if __name__ == "__main__":
    main()