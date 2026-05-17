from manim import *
import numpy as np


class DepthOfFieldZone(Scene):
    def construct(self):
        # ─── Layout constants ───────────────────────────────────────────
        meter_unit = 1.0
        axis_y = -2.2
        camera_y = -1.6

        # ─── Camera ─────────────────────────────────────────────────────
        body = RoundedRectangle(width=1.0, height=0.7, corner_radius=0.08,
                                color=GRAY_B, fill_opacity=1.0, stroke_width=2)
        body.move_to([-5.5, camera_y, 0])
        vf = Rectangle(width=0.35, height=0.13, color=GRAY_C, fill_opacity=1.0, stroke_width=1)
        vf.move_to([body.get_x(), body.get_top()[1] + 0.065, 0])
        lens_outer = Rectangle(width=0.32, height=0.5, color=GRAY_C, fill_opacity=1.0, stroke_width=1)
        lens_outer.next_to(body, RIGHT, buff=-0.05)
        lens_glass = Circle(radius=0.17, color=BLUE_E, fill_opacity=0.9,
                            stroke_width=1.5, stroke_color=GRAY_B)
        lens_glass.move_to(lens_outer.get_right() + LEFT * 0.06)
        camera = VGroup(vf, body, lens_outer, lens_glass)
        camera_fnum = Text("f/2.8", font_size=32, color=YELLOW).scale(0.5).next_to(body, LEFT, buff=0.15)

        # ─── Distance axis ──────────────────────────────────────────────
        axis_start_x = lens_glass.get_center()[0] + 0.25
        axis_end_x = axis_start_x + 6.5
        axis = Arrow([axis_start_x, axis_y, 0], [axis_end_x, axis_y, 0],
                     color=GRAY_B, buff=0, stroke_width=2.5,
                     max_tip_length_to_length_ratio=0.04)

        marker_lines = VGroup()
        marker_labels = VGroup()
        for d in [1, 2, 3, 4, 5, 6]:
            x = axis_start_x + d * meter_unit
            tick = Line([x, axis_y - 0.08, 0], [x, axis_y + 0.08, 0],
                        color=GRAY_B, stroke_width=2)
            lbl = Text(f"{d}m", font_size=26, color=GRAY_B).scale(0.5).next_to(tick, DOWN, buff=0.07)
            marker_lines.add(tick)
            marker_labels.add(lbl)

        # ─── Scene objects ──────────────────────────────────────────────
        def make_tree(color, size):
            trunk = Rectangle(width=size * 0.18, height=size * 0.45, color=GRAY,
                              fill_opacity=1.0, stroke_width=1)
            foliage = Triangle(color=color, fill_opacity=1.0, stroke_width=1).scale(size * 0.8)
            foliage.next_to(trunk, UP, buff=-size * 0.1)
            return VGroup(trunk, foliage)

        def make_person(color, size):
            head = Circle(radius=size * 0.22, color=color, fill_opacity=1.0, stroke_width=1.5)
            torso = Rectangle(width=size * 0.5, height=size * 0.8, color=color,
                              fill_opacity=1.0, stroke_width=1.5)
            torso.next_to(head, DOWN, buff=0.02)
            return VGroup(head, torso)

        # (distance_m, object)
        object_specs = [
            (1.5, make_tree(GREEN_D, 0.7)),
            (2.5, Circle(radius=0.22, color=PURPLE_A, fill_opacity=0.95, stroke_width=2)),
            (3.0, make_person(YELLOW_D, 0.8)),
            (3.5, Circle(radius=0.22, color=TEAL_A, fill_opacity=0.95, stroke_width=2)),
            (4.5, make_tree(GREEN_E, 0.6)),
        ]
        scene_objects = VGroup()
        object_distances = []
        for d, obj in object_specs:
            x = axis_start_x + d * meter_unit
            obj.move_to([x, axis_y + obj.height / 2 + 0.05, 0])
            scene_objects.add(obj)
            object_distances.append(d)

        # ─── Focus plane line ───────────────────────────────────────────
        focus_d = 3.0
        focus_x = axis_start_x + focus_d * meter_unit
        focus_line = DashedLine([focus_x, axis_y - 0.15, 0], [focus_x, 2.0, 0],
                                color=YELLOW_B, dash_length=0.08, stroke_width=2)
        focus_label = Text("focus (3m)", font_size=26, color=YELLOW_B).scale(0.5).move_to([focus_x, 2.25, 0])

        # ─── DoF bands ──────────────────────────────────────────────────
        band_height = 3.2
        band_bottom = axis_y + 0.05
        band_y_center = band_bottom + band_height / 2

        def band_rect(near, far):
            width = (far - near) * meter_unit
            x_center = axis_start_x + (near + far) / 2 * meter_unit
            r = Rectangle(width=width, height=band_height,
                          color=GREEN_B, fill_opacity=0.25,
                          stroke_color=GREEN_C, stroke_width=2)
            r.move_to([x_center, band_y_center, 0])
            return r

        ff_near, ff_far = 2.75, 3.25
        mft_near, mft_far = 2.5, 3.5

        ff_band = band_rect(ff_near, ff_far)
        mft_band = band_rect(mft_near, mft_far)

        # DoF width labels (placed inside the band, near top)
        ff_dof_label = Text("DoF ≈ 0.5 m", font_size=36, color=GREEN_C).scale(0.5)
        ff_dof_label.move_to([axis_start_x + 3.0, 1.5, 0])
        mft_dof_label = Text("DoF ≈ 1.0 m   (2× wider)", font_size=36, color=GREEN_C).scale(0.5)
        mft_dof_label.move_to([axis_start_x + 3.0, 1.5, 0])

        # ─── Headers ────────────────────────────────────────────────────
        title = Text("Depth of Field — same f/2.8, same framing",
                     font_size=48).scale(0.5).to_edge(UP, buff=0.2)
        mode_ff = Text("Full Frame", font_size=44, color=BLUE).scale(0.5).next_to(title, DOWN, buff=0.15)
        mode_mft = Text("Micro Four Thirds", font_size=44, color=RED).scale(0.5).next_to(title, DOWN, buff=0.15)

        # ─── Animations ─────────────────────────────────────────────────

        # 1. Title
        self.play(Write(title))

        # 2. Camera
        self.play(FadeIn(camera), FadeIn(camera_fnum))

        # 3. Distance axis + markers
        self.play(GrowArrow(axis))
        self.play(LaggedStartMap(Create, marker_lines, lag_ratio=0.08),
                  LaggedStartMap(FadeIn, marker_labels, lag_ratio=0.08), run_time=0.9)

        # 4. Scene objects
        self.play(LaggedStartMap(FadeIn, scene_objects, lag_ratio=0.12))
        self.wait(0.4)

        # 5. Focus plane line
        self.play(Create(focus_line), FadeIn(focus_label))
        self.wait(0.4)

        # 6. Enter FF mode + show FF DoF band
        self.play(FadeIn(mode_ff))
        self.play(FadeIn(ff_band), FadeIn(ff_dof_label))

        # 7. Blur objects outside FF band
        blur_anims = []
        for obj, d in zip(scene_objects, object_distances):
            if not (ff_near <= d <= ff_far):
                blur_anims.append(obj.animate.set_opacity(0.3))
        self.play(*blur_anims, run_time=0.8)
        self.wait(2.0)

        # 8. FF → MFT: band expands, more objects come into focus
        sharpen_anims = []
        for obj, d in zip(scene_objects, object_distances):
            if (mft_near <= d <= mft_far) and not (ff_near <= d <= ff_far):
                sharpen_anims.append(obj.animate.set_opacity(1.0))

        self.play(
            Transform(mode_ff, mode_mft),
            Transform(ff_band, mft_band),
            Transform(ff_dof_label, mft_dof_label),
            *sharpen_anims,
            run_time=1.8,
        )
        self.wait(2.5)

        # 9. Summary
        summary = Text("Same f/2.8 · equivalent framing → MFT DoF ≈ 2× FF",
                       font_size=40, color=GREEN_B).scale(0.5).to_edge(DOWN, buff=0.4)
        self.play(Write(summary))
        self.wait(3)
