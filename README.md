# Manim Animations

Photography/optics explainer animations built with [Manim Community Edition](https://www.manim.community/) v0.20.1.

## Scenes

| File | Scene class | Description |
|------|-------------|-------------|
| `light_cone_aperture.py` | `LightConeAperture` | Light cone, aperture, and why same f-stop = same intensity per mm² across sensor sizes |
| `sensor_comparison.py` | `SensorSizeComparison` | Full Frame vs MFT sensor size comparison |
| `depth_of_field.py` | `DepthOfFieldZone` | Depth of field zone visualization |

## Rendering

### Quick preview (low quality — fast iteration)

```bash
manim -pql <file>.py <SceneName>
```

480p, 15 fps. Use this while developing — renders in seconds.

### Standard quality (720p)

```bash
manim -pqm <file>.py <SceneName>
```

720p, 30 fps. Good middle ground for checking layout and motion.

### Full HD (1080p) — recommended for final export

```bash
manim -pqh <file>.py <SceneName>
```

1080p, 60 fps. Use this for the final render you'll actually share.

### Production / 2K

```bash
manim -pqp <file>.py <SceneName>
```

1440p, 60 fps. Noticeably slower; worth it if you plan to pan/zoom in a video editor.

### 4K

```bash
manim -pqk <file>.py <SceneName>
```

2160p, 60 fps. Slow. Only needed if the final delivery target is 4K.

### Render without auto-opening the preview

Drop the `-p` flag from any command above:

```bash
manim -qh <file>.py <SceneName>
```

### Quality flag reference

| Flag | Resolution | FPS |
|------|-----------|-----|
| `-ql` | 480p | 15 |
| `-qm` | 720p | 30 |
| `-qh` | 1080p | 60 |
| `-qp` | 1440p (2K) | 60 |
| `-qk` | 2160p (4K) | 60 |

Output lands in `media/videos/<file>/<resolution>/`.
