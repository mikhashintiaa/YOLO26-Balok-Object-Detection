from pathlib import Path
import shutil
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "README_ASSETS"
OUT.mkdir(exist_ok=True)

CLASSES = [
    "balok_hijautua",
    "balok_hitam",
    "balok_merahmuda",
    "papan_balok",
]

def copy_if_exists(src, dst_name):
    src = Path(src)
    if src.exists():
        dst = OUT / dst_name
        shutil.copy2(src, dst)
        print(f"[OK] {dst}")
        return dst
    print(f"[SKIP] Tidak ditemukan: {src}")
    return None

def find_test_dir():
    candidates = [
        ROOT / "hasil_praktik" / "TEST_E1",
        ROOT / "runs" / "detect" / "hasil_praktik" / "TEST_E1",
    ]
    for p in candidates:
        if p.exists():
            return p
    return None

def pick_one(folder, class_name):
    exts = {".jpg", ".jpeg", ".png", ".webp"}
    files = [p for p in sorted(folder.iterdir())
             if p.is_file() and p.suffix.lower() in exts and class_name in p.stem]
    return files[0] if files else None

def make_montage(paths, labels, output, title):
    valid = [(p, l) for p, l in zip(paths, labels) if p and Path(p).exists()]
    if not valid:
        print(f"[SKIP] Tidak ada gambar untuk {output}")
        return
    thumb_w, thumb_h = 520, 390
    header_h = 60
    cell_h = thumb_h + 45
    cols = 2
    rows = (len(valid) + cols - 1) // cols
    canvas = Image.new("RGB", (cols * thumb_w, header_h + rows * cell_h), "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((20, 20), title, fill="black")
    for i, (p, label) in enumerate(valid):
        img = Image.open(p).convert("RGB")
        img.thumbnail((thumb_w - 20, thumb_h - 20))
        bg = Image.new("RGB", (thumb_w, thumb_h), "white")
        x = (thumb_w - img.width) // 2
        y = (thumb_h - img.height) // 2
        bg.paste(img, (x, y))
        r, c = divmod(i, cols)
        px, py = c * thumb_w, header_h + r * cell_h
        canvas.paste(bg, (px, py))
        draw.text((px + 12, py + thumb_h + 10), label, fill="black")
    canvas.save(OUT / output, quality=95)
    print(f"[OK] {OUT / output}")

cek_visual = ROOT / "dataset_yolo" / "cek_visual"
if cek_visual.exists():
    ann_paths = [pick_one(cek_visual, c) for c in CLASSES]
    make_montage(
        ann_paths, CLASSES,
        "01_contoh_anotasi_4kelas.jpg",
        "Contoh anotasi bounding box dataset"
    )
else:
    print("[SKIP] dataset_yolo/cek_visual tidak ditemukan")

copy_if_exists(ROOT / "hasil_praktik" / "E1_pretrained" / "results.png", "02_E1_results.png")
copy_if_exists(ROOT / "hasil_praktik" / "E2_scratch" / "results.png", "03_E2_results.png")
copy_if_exists(ROOT / "hasil_praktik" / "E3_tuning" / "results.png", "04_E3_results.png")

experiments = ["E1 Pretrained", "E2 Scratch", "E3 Tuning"]
map50 = [0.995, 0.952, 0.995]
map5095 = [0.976, 0.634, 0.969]

x = range(len(experiments))
width = 0.36
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar([i - width/2 for i in x], map50, width, label="mAP50")
ax.bar([i + width/2 for i in x], map5095, width, label="mAP50-95")
ax.set_xticks(list(x))
ax.set_xticklabels(experiments)
ax.set_ylim(0, 1.05)
ax.set_ylabel("Nilai")
ax.set_title("Perbandingan Akurasi E1, E2, dan E3")
ax.legend()
ax.grid(axis="y", alpha=0.25)
for i, v in enumerate(map50):
    ax.text(i - width/2, v + 0.015, f"{v:.3f}", ha="center", fontsize=9)
for i, v in enumerate(map5095):
    ax.text(i + width/2, v + 0.015, f"{v:.3f}", ha="center", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "05_perbandingan_akurasi_E1_E2_E3.png", dpi=180)
plt.close(fig)
print(f"[OK] {OUT / '05_perbandingan_akurasi_E1_E2_E3.png'}")

inference_ms = [20.9, 21.9, 60.8]
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(experiments, inference_ms)
ax.set_ylabel("Inference time (ms/gambar)")
ax.set_title("Perbandingan Waktu Inferensi")
ax.grid(axis="y", alpha=0.25)
for b, v in zip(bars, inference_ms):
    ax.text(b.get_x() + b.get_width()/2, v + 1, f"{v:.1f} ms", ha="center", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "06_perbandingan_inference_time.png", dpi=180)
plt.close(fig)
print(f"[OK] {OUT / '06_perbandingan_inference_time.png'}")

test_dir = find_test_dir()
if test_dir:
    test_paths = [pick_one(test_dir, c) for c in CLASSES]
    make_montage(
        test_paths, CLASSES,
        "07_hasil_test_4kelas.jpg",
        "Contoh hasil deteksi model terbaik (E1)"
    )
else:
    print("[SKIP] Folder TEST_E1 tidak ditemukan")

e1 = ROOT / "hasil_praktik" / "E1_pretrained"
copy_if_exists(e1 / "PR_curve.png", "08_PR_curve_E1.png")
copy_if_exists(e1 / "F1_curve.png", "09_F1_curve_E1.png")

print("\nSELESAI.")
print(f"Semua aset README ada di: {OUT}")
