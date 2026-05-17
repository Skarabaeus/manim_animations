from manim import *


class SensorSizeComparison(Scene):
    def construct(self):
        # --- Dimensions (scaled: 1 unit = 4mm) ---
        SCALE = 0.15
        ff_w, ff_h = 36 * SCALE, 24 * SCALE
        mft_w, mft_h = 17.3 * SCALE, 13 * SCALE

        # --- Full Frame sensor ---
        ff_rect = Rectangle(width=ff_w, height=ff_h, color=BLUE)
        ff_rect.set_fill(BLUE, opacity=0.25)
        ff_label = Text("Full Frame", font_size=48, color=BLUE).scale(0.5).next_to(ff_rect, UP, buff=0.2)
        ff_dim = Text("36 × 24 mm", font_size=36, color=BLUE_B).scale(0.5).next_to(ff_rect, DOWN, buff=0.2)

        # --- MFT sensor (same center) ---
        mft_rect = Rectangle(width=mft_w, height=mft_h, color=RED)
        mft_rect.set_fill(RED, opacity=0.35)
        mft_label = Text("Micro Four Thirds", font_size=48, color=RED).scale(0.5).next_to(ff_rect, UP, buff=0.2)
        mft_dim = Text("17.3 × 13 mm", font_size=36, color=RED_B).scale(0.5).next_to(mft_rect, DOWN, buff=0.2)

        # --- Crop factor annotation ---
        crop_text = Text("2× Crop Factor", font_size=44, color=YELLOW).scale(0.5)
        crop_text.to_edge(DOWN, buff=0.5)

        # Corner brackets to highlight the MFT area inside FF
        corner_color = RED_C
        corner_len = 0.25
        half_w, half_h = mft_w / 2, mft_h / 2
        corners = VGroup(*[
            VGroup(
                Line(ORIGIN, dx * corner_len * RIGHT, color=corner_color, stroke_width=3),
                Line(ORIGIN, dy * corner_len * UP,   color=corner_color, stroke_width=3),
            ).shift(dx * half_w * RIGHT + dy * half_h * UP)
            for dx, dy in [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        ])

        # ── Animation sequence ──────────────────────────────────────────────

        # 1. Draw Full Frame
        self.play(Create(ff_rect), Write(ff_label))
        self.play(FadeIn(ff_dim))
        self.wait(0.8)

        # 2. Overlay MFT rect (fade in label swap)
        self.play(
            FadeOut(ff_label),
            FadeOut(ff_dim),
            FadeIn(mft_rect),
            run_time=0.6,
        )
        self.play(Write(mft_label), FadeIn(mft_dim))
        self.wait(0.8)

        # 3. Show both labels separated vertically
        ff_label_static = Text("Full Frame (36×24)", font_size=40, color=BLUE).scale(0.5).move_to(ff_rect).shift(UP * 1.6)
        mft_label_static = Text("MFT (17.3×13)", font_size=40, color=RED).scale(0.5).move_to(ff_rect).shift(UP * 1.2)
        self.play(
            FadeOut(mft_label),
            FadeOut(mft_dim),
            FadeIn(ff_label_static),
            FadeIn(mft_label_static),
        )
        self.wait(0.5)

        # 4. Draw corner brackets to emphasise MFT boundary inside FF
        self.play(Create(corners))
        self.wait(0.5)

        # 5. Show crop factor callout
        self.play(Write(crop_text))
        self.wait(1.5)

        # 6. Pulse the MFT rect to emphasise it is the smaller sensor
        self.play(mft_rect.animate.set_fill(RED, opacity=0.6), run_time=0.4)
        self.play(mft_rect.animate.set_fill(RED, opacity=0.35), run_time=0.4)
        self.wait(1)
