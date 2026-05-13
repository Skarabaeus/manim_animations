from manim import *
import numpy as np


class LightConeAperture(Scene):
    def construct(self):
        # === Layout ===
        LENS_X = -4.0
        SENSOR_X = 3.0

        # Sensor visual heights (proportional FF:MFT = 24:13)
        ff_h = 2.0
        mft_h = ff_h * (13 / 24)

        # === Title ===
        title = Text("Same f/2.8 → Same intensity per mm²",
                     font_size=26, color=WHITE).to_edge(UP, buff=0.3)

        # === Lens (side view = vertical ellipse) ===
        lens = Ellipse(width=0.4, height=2.4, color=BLUE_C,
                       fill_opacity=0.4, stroke_width=2)
        lens.move_to([LENS_X, 0, 0])

        ap_top = lens.get_top()
        ap_bot = lens.get_bottom()
        lens_half_h = (ap_top[1] - ap_bot[1]) / 2

        f_label = Text("f/2.8", font_size=22, color=YELLOW).next_to(lens, DOWN, buff=0.25)
        lens_label = Text("lens", font_size=14, color=BLUE_B).next_to(lens, UP, buff=0.15)

        # Aperture brace
        ap_brace = Brace(lens, direction=LEFT, buff=0.05)
        ap_brace_label = Text("aperture", font_size=12, color=BLUE_B).next_to(
            ap_brace, LEFT, buff=0.05)

        # === Sensor plane (reference line) ===
        sensor_plane = DashedLine(
            np.array([SENSOR_X, 2.3, 0]),
            np.array([SENSOR_X, -2.3, 0]),
            color=GRAY, dash_length=0.1, stroke_opacity=0.5
        )
        sp_label = Text("sensor plane", font_size=12, color=GRAY_B).next_to(
            sensor_plane.get_top(), UP, buff=0.1)

        # === Light cone (aperture → image area at sensor plane) ===
        image_h = ff_h * 1.05
        cone_top_pt = np.array([SENSOR_X, image_h / 2, 0])
        cone_bot_pt = np.array([SENSOR_X, -image_h / 2, 0])

        cone = Polygon(
            ap_top, ap_bot, cone_bot_pt, cone_top_pt,
            color=YELLOW, fill_opacity=0.2,
            stroke_width=2, stroke_color=YELLOW_B
        )

        # Top/bottom rays as separate emphasised lines
        ray_top = Line(ap_top, cone_top_pt, color=YELLOW_B, stroke_width=2)
        ray_bot = Line(ap_bot, cone_bot_pt, color=YELLOW_B, stroke_width=2)

        # === Photon dots (uniform density inside cone) ===
        photon_dots = VGroup()
        rng = np.random.default_rng(42)
        n_dots = 100
        for _ in range(n_dots):
            t = rng.uniform(0.08, 1.0)
            x = LENS_X + t * (SENSOR_X - LENS_X)
            y_bound = (1 - t) * lens_half_h + t * (image_h / 2)
            y = rng.uniform(-y_bound * 0.97, y_bound * 0.97)
            dot = Dot([x, y, 0], radius=0.022, color=YELLOW_A, fill_opacity=0.85)
            photon_dots.add(dot)

        # === Sensors ===
        ff_sensor = Rectangle(width=0.2, height=ff_h, color=BLUE,
                              fill_opacity=0.9, stroke_width=2)
        ff_sensor.move_to([SENSOR_X, 0, 0])
        ff_text = VGroup(
            Text("Full Frame", font_size=18, color=BLUE),
            Text("864 mm²", font_size=14, color=BLUE_B),
        ).arrange(DOWN, buff=0.1).next_to(ff_sensor, RIGHT, buff=0.3)

        mft_sensor = Rectangle(width=0.2, height=mft_h, color=RED,
                               fill_opacity=0.9, stroke_width=2)
        mft_sensor.move_to([SENSOR_X, 0, 0])
        mft_text = VGroup(
            Text("MFT", font_size=18, color=RED),
            Text("225 mm²", font_size=14, color=RED_B),
        ).arrange(DOWN, buff=0.1).next_to(mft_sensor, RIGHT, buff=0.3)

        # === Bottom annotation slot ===
        bottom_note_position = lambda mob: mob.to_edge(DOWN, buff=0.5)

        # ── Animations ────────────────────────────────────────────────────

        # 1. Title
        self.play(Write(title))

        # 2. Lens + labels
        self.play(Create(lens), FadeIn(f_label), FadeIn(lens_label))
        self.play(FadeIn(ap_brace), FadeIn(ap_brace_label))

        # 3. Sensor plane
        self.play(Create(sensor_plane), FadeIn(sp_label))
        self.wait(0.3)

        # 4. Light cone — draw rays first, then fill
        self.play(Create(ray_top), Create(ray_bot), run_time=0.8)
        self.play(FadeIn(cone), run_time=0.6)

        # 5. Photon dots fade in to show uniform illumination
        self.play(LaggedStartMap(FadeIn, photon_dots, lag_ratio=0.008, run_time=1.5))
        self.wait(0.3)

        # 6. FF sensor enters the focal plane
        self.play(GrowFromCenter(ff_sensor), FadeIn(ff_text))

        note = Text("FF captures the full cone — wide area at f/2.8 intensity",
                    font_size=18, color=BLUE_A)
        bottom_note_position(note)
        self.play(FadeIn(note))
        self.wait(2)

        # 7. Swap FF → MFT
        note2 = Text("Swap to MFT — same lens, same f/2.8, smaller sensor",
                     font_size=18, color=ORANGE)
        bottom_note_position(note2)
        self.play(Transform(note, note2))

        self.play(
            Transform(ff_sensor, mft_sensor),
            FadeOut(ff_text),
        )
        self.play(FadeIn(mft_text))
        self.wait(0.6)

        # 8. Emphasise: cone unchanged → intensity per mm² unchanged
        note3 = Text("Cone unchanged → same intensity per mm² → same exposure",
                     font_size=18, color=GREEN_B)
        bottom_note_position(note3)
        self.play(Transform(note, note3))

        # Pulse cone
        self.play(cone.animate.set_fill(YELLOW, opacity=0.4), run_time=0.4)
        self.play(cone.animate.set_fill(YELLOW, opacity=0.2), run_time=0.4)
        self.wait(1.0)

        # 9. Highlight that MFT misses the outer rays (less total light)
        # Dim photons above and below the MFT sensor's vertical extent
        outside_photons = VGroup(*[
            d for d in photon_dots
            if abs(d.get_center()[1]) > mft_h / 2 * (
                (d.get_center()[0] - LENS_X) / (SENSOR_X - LENS_X)
            ) + lens_half_h * (1 - (d.get_center()[0] - LENS_X) / (SENSOR_X - LENS_X)) * 0  # only filter by sensor band
        ])
        # Simpler filter: photons whose y exceeds MFT half-height (at any x near the sensor)
        outside_photons = VGroup(*[
            d for d in photon_dots if abs(d.get_center()[1]) > mft_h / 2
        ])
        self.play(outside_photons.animate.set_fill(GRAY, opacity=0.25), run_time=0.8)

        note4 = Text("Same lux per mm²   ·   MFT total light ≈ ¼ of FF (smaller area)",
                     font_size=18, color=WHITE)
        bottom_note_position(note4)
        self.play(Transform(note, note4))
        self.wait(2.5)
