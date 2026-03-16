from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from datetime import datetime

OUT = "output/pdf/snake_game_project_documentation.pdf"


def wrap_text(text, font_name, font_size, max_width):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        t = w if not cur else f"{cur} {w}"
        if stringWidth(t, font_name, font_size) <= max_width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_section(c, x, y, width, title, bullets, heading_size=9.2, body_size=7.6):
    c.setFont("Helvetica-Bold", heading_size)
    c.drawString(x, y, title)
    y -= 10
    c.setFont("Helvetica", body_size)

    for b in bullets:
        lines = wrap_text(b, "Helvetica", body_size, width - 8)
        if not lines:
            continue
        c.drawString(x + 1, y, u"- " + lines[0])
        y -= 8
        for line in lines[1:]:
            c.drawString(x + 8, y, line)
            y -= 8
        y -= 2
    return y


def build(path):
    c = canvas.Canvas(path, pagesize=A4)
    w, h = A4
    margin = 13 * mm
    content_w = w - (2 * margin)

    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(1)
    c.rect(margin - 4, margin - 4, content_w + 8, h - 2 * margin + 8)

    header_y = h - margin - 12

    c.setFont("Helvetica-Bold", 15)
    c.drawString(margin, header_y, "SNAKE GAME | TECHNICAL + PROJECT DOCUMENTATION")
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margin, header_y - 14, "Artifact: CyberChipppyyy Snake | Runtime: Browser | Language: Vanilla JS | Rendering: Canvas 2D")
    c.setFont("Helvetica", 7.4)
    c.drawString(margin, header_y - 25, f"Generated {datetime.now().strftime('%Y-%m-%d %H:%M')} | Scope reviewed: full repository (1 file, 302 LOC)")
    c.line(margin, header_y - 31, w - margin, header_y - 31)

    gap = 7 * mm
    col_w = (content_w - gap) / 2
    lx = margin
    rx = margin + col_w + gap
    ly = header_y - 43
    ry = header_y - 43

    ly = draw_section(c, lx, ly, col_w, "1) PROJECT SUMMARY", [
        "A self-contained Snake implementation delivered as a single HTML file. No package manager, build pipeline, server process, or external media dependencies are required.",
        "Core objective: retain classic movement/collision mechanics while applying a cyber-neon presentation and synthesized interaction feedback.",
        "Execution model: static page load, immediate gameplay loop startup, keyboard-driven control path, canvas-based redraw on each frame."
    ])

    ly = draw_section(c, lx, ly, col_w, "2) FILE + CODE MAP", [
        "`index.html` owns all layers: semantic shell (HUD/canvas/help), CSS theming, stateful game engine, drawing pipeline, audio primitives, and event binding.",
        "State primitives: `snake`, `direction`, `nextDirection`, `food`, `score`, `tickMs`, `lastTick`, `running`, and lazy `audioCtx`.",
        "Gameplay constants: `cells=32`, `BASE_SPEED=140ms`, `SPEED_STEP=7ms/point`, `MIN_SPEED=45ms`."
    ])

    ly = draw_section(c, lx, ly, col_w, "3) GAME ENGINE DETAILS", [
        "Board geometry: 640x640 canvas partitioned into 32x32 grid cells. Entity coordinates are integer cell indices for deterministic movement and collision checks.",
        "Update cycle: `requestAnimationFrame` loop executes `update()` once elapsed wall-clock >= `tickMs`; render path runs every animation frame.",
        "Collision policy: terminal on boundary overflow or any head-to-body intersection; on terminal state `running=false` and failure UI/sound are triggered.",
        "Growth policy: head insertion each step, tail removal unless food consumed; this preserves expected body propagation behavior."
    ])

    ly = draw_section(c, lx, ly, col_w, "4) INPUT + UX BEHAVIOR", [
        "Supported controls: Arrow keys and WASD for directional intent, Space for hard restart, pointer/tap to initialize audio and restart after fail.",
        "Input safety: direct 180-degree reversals are rejected to prevent invalid self-collision exploits.",
        "HUD behavior: score is displayed in top header and updated on every successful food capture."
    ])

    ry = draw_section(c, rx, ry, col_w, "5) RENDERING + VISUAL SYSTEM", [
        "Theme implementation combines layered radial/linear gradients, glow shadows, and high-contrast typography for a cyber aesthetic.",
        "Snake rendering: bright green segments with stronger head luminosity to maintain directional readability at high speeds.",
        "Food rendering: enlarged purple pixel block with randomized inset/shadow and alpha modulation to produce a flicker effect.",
        "Grid rendering: low-opacity lattice lines keep positional context without overpowering gameplay objects."
    ])

    ry = draw_section(c, rx, ry, col_w, "6) AUDIO SYSTEM", [
        "Audio backend: WebAudio API with oscillator + gain envelope synthesis; no static files are bundled.",
        "Event-linked cues: start boot chirp, directional click, reward tone pair, and descending failure pattern.",
        "Compatibility strategy: `ensureAudio()` lazily creates/resumes context to satisfy autoplay restrictions in modern browsers."
    ])

    ry = draw_section(c, rx, ry, col_w, "7) SCORING + DIFFICULTY SCALING", [
        "Score increments by 1 per food pickup and is reflected immediately in HUD text content.",
        "Difficulty increases every point: loop interval decreases by 7ms after each score event until hard floor (45ms) is reached.",
        "This creates linear acceleration early game and capped speed ceiling late game for playability."
    ])

    ry = draw_section(c, rx, ry, col_w, "8) QUALITY STATUS + NEXT ITERATIONS", [
        "Current quality strengths: deterministic rules, responsive layout, clear controls, robust restart flow, and coherent visual/audio feedback.",
        "Known constraints: no automated tests, no persistent high score, no swipe gestures, no in-game pause/settings surface.",
        "Recommended roadmap: persistence via localStorage, touch gesture interpreter, difficulty presets, and optional accessibility palette mode."
    ])

    c.setLineWidth(0.6)
    c.line(margin, margin + 12, w - margin, margin + 12)
    c.setFont("Helvetica-Bold", 7.4)
    c.drawString(margin, margin + 3, "Document profile: monochrome single-page technical brief with implementation and maintenance coverage")

    c.showPage()
    c.save()


if __name__ == "__main__":
    build(OUT)
    print(OUT)

