"""STEP 8-7B: 10 progressive voting charts -> FHD MP4 (no audio).

Run in AIJ-P1 project root:
    python -m pip install imageio imageio-ffmpeg pillow numpy
    python step8_make_counting_video.py

The script never inserts future results ahead of their stage.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import imageio.v2 as imageio
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
CHARTS = ROOT / "video" / "charts"
OUTPUT = ROOT / "video" / "clips" / "hanbit_counting_10steps.mp4"


def make_video(seconds_per_step: float, fps: int, fade_seconds: float) -> None:
    files = [CHARTS / f"vote_share_step_{step:02d}.png" for step in range(1, 11)]
    missing = [str(path) for path in files if not path.is_file()]
    if missing:
        raise FileNotFoundError("그래프 PNG 파일이 없습니다:\n" + "\n".join(missing))

    images: list[np.ndarray] = []
    for file in files:
        with Image.open(file) as img:
            if img.size != (1920, 1080):
                raise ValueError(f"{file.name}: 1920×1080이 아닌 {img.size}입니다")
            images.append(np.asarray(img.convert("RGB")))

    frames_per_step = round(seconds_per_step * fps)
    fade_frames = round(fade_seconds * fps)
    if frames_per_step < 1 or fade_frames >= frames_per_step:
        raise ValueError("단계 표시 시간은 전환 효과보다 길어야 합니다.")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    print(f"입력: PNG {len(images)}개 (1920x1080)")
    print(f"출력: {OUTPUT}")
    print(f"설정: {fps}fps, 단계당 {seconds_per_step}초, 전환 {fade_seconds}초")

    # Each step occupies a fixed slot, with the fade at the end of the slot.
    # The final frame remains the verified step 10 result.
    with imageio.get_writer(
        OUTPUT, fps=fps, codec="libx264", quality=7,
        pixelformat="yuv420p", macro_block_size=1,
        ffmpeg_log_level="error",
    ) as writer:
        for idx, frame in enumerate(images):
            hold_frames = frames_per_step if idx == 9 else frames_per_step - fade_frames
            for _ in range(hold_frames):
                writer.append_data(frame)
            if idx < 9:
                next_frame = images[idx + 1]
                for k in range(1, fade_frames + 1):
                    alpha = k / fade_frames
                    blended = Image.blend(
                        Image.fromarray(frame), Image.fromarray(next_frame), alpha
                    )
                    writer.append_data(np.asarray(blended))
            print(f"완료: {idx+1:02d}/10단계")

    print(f"완료: {OUTPUT.name} / 예상 길이 {frames_per_step*10/fps:.1f}초")
    print("참고: 음성 없는 개표 그래픽 클립입니다. 앵커 MP3는 편집 단계에서 결합합니다.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="한빛시 10단계 개표 그래픽 MP4")
    parser.add_argument("--seconds-per-step", type=float, default=3.0)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--fade-seconds", type=float, default=0.4)
    args = parser.parse_args()
    make_video(args.seconds_per_step, args.fps, args.fade_seconds)
