"""Builds dark_mode.svg and light_mode.svg. Run daily by .github/workflows/update.yml to refresh Uptime."""
import calendar
from datetime import date
from xml.sax.saxutils import escape

BIRTH = date(1993, 10, 26)
WIDTH = 60  # characters in the info column

ART = r"""
┌──────────────────────────────────────┐
│ ● ● ●          ~/cesariolins         │
├──────────────────────────────────────┤
│ $ whoami                             │
│ cesario lins                         │
│                                      │
│ $ cat career.txt                     │
│ dentist ──► developer                │
│                                      │
│ $ ls stack/                          │
│ react  next  node  postgres  ai      │
│                                      │
│ $ npm run dev                        │
│ ▲ Ready on http://localhost:3000     │
│                                      │
│ $ █                                  │
└──────────────────────────────────────┘""".split("\n")[1:]

THEMES = {
    "dark_mode.svg": dict(bg="#161b22", fg="#c9d1d9", key="#ffa657", value="#a5d6ff", cc="#616e7f"),
    "light_mode.svg": dict(bg="#f6f8fa", fg="#24292f", key="#953800", value="#0a3069", cc="#c2cfde"),
}


def uptime(born, today):
    # ponytail: day-borrow assumes birth day <= 28 (true for the 26th); use dateutil.relativedelta if that changes
    y, m, d = today.year - born.year, today.month - born.month, today.day - born.day
    if d < 0:
        m -= 1
        prev_year, prev_month = (today.year, today.month - 1) if today.month > 1 else (today.year - 1, 12)
        d += calendar.monthrange(prev_year, prev_month)[1]
    if m < 0:
        y, m = y - 1, m + 12
    return ", ".join(f"{n} {unit}{'s' * (n != 1)}" for n, unit in ((y, "year"), (m, "month"), (d, "day")))


assert uptime(date(1993, 10, 26), date(2026, 11, 4)) == "33 years, 0 months, 9 days"
assert uptime(date(1993, 10, 26), date(2027, 1, 5)) == "33 years, 2 months, 10 days"


def span(text, cls=None):
    return f'<tspan class="{cls}">{escape(text)}</tspan>' if cls else escape(text)


def kv(key, value, width=WIDTH, lead=". "):
    dots = "." * (width - len(lead) - len(key) - len(value) - 3)
    return span(lead, "cc") + span(key, "key") + ":" + span(f" {dots} ", "cc") + span(value, "value")


def title(text, lead="- "):
    return escape(f"{lead}{text} ") + span("-" + "—" * (WIDTH - len(lead) - len(text) - 5) + "-—-", "cc")


BLANK = span(".", "cc")
INFO = [
    title("cesario@lins", lead=""),
    kv("OS", "Windows 11"),
    kv("Uptime", uptime(BIRTH, date.today())),
    kv("Host", "Instituto do Autismo, Univ. da Inclusão"),
    kv("Kernel", "Full Stack Developer"),
    kv("IDE", "VS Code, Claude Code"),
    BLANK,
    kv("Languages.Programming", "JavaScript, TypeScript, SQL"),
    kv("Languages.Computer", "HTML, CSS, SCSS, JSON"),
    kv("Languages.Real", "Portuguese, English"),
    BLANK,
    kv("Stack.Frontend", "React, Next.js, Tailwind"),
    kv("Stack.Backend", "Node.js, Express, REST, Webhooks"),
    kv("Stack.Database", "PostgreSQL, MySQL, Supabase, MongoDB"),
    kv("Stack.AI", "Claude Code, Copilot, MCP, AI Agents"),
    BLANK,
    kv("Career.Before", "Dentist, 8 years (DDS, UFPE)"),
    kv("Career.Switch", "Systems Analysis & Dev, 2025"),
    "",
    title("Contact"),
    kv("Email", "cesario5c@hotmail.com"),
    kv("LinkedIn", "cesariolins"),
    kv("Website", "cesariolins.com.br"),
    "",
    title("Projects"),
    kv("Event.Platform", "3,500+ sign-ups handled"),
    kv("Academic.System", "used by 1,500+ students"),
    kv("AI.Grading", "feedback: days → minutes"),
    kv("WhatsApp.Automation", "no-shows 50% → 30%"),
]

W, H = 1000, 30 + 20 * max(len(ART), len(INFO))
top = max(0, (len(INFO) - len(ART)) // 2)  # centers the art next to the info column
for name, c in THEMES.items():
    art = "\n".join(f'<tspan x="15" y="{30 + 20 * (top + i)}">{escape(line)}</tspan>' for i, line in enumerate(ART))
    info = "\n".join(f'<tspan x="410" y="{30 + 20 * i}">{line}</tspan>' for i, line in enumerate(INFO))
    with open(name, "w", encoding="utf-8") as f:
        f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="{W}px" height="{H}px" font-size="16px">
<style>
@font-face {{ src: local('Consolas'), local('Consolas Bold'); font-family: 'ConsolasFallback'; font-display: swap; size-adjust: 109%; }}
.key {{fill: {c['key']};}} .value {{fill: {c['value']};}} .cc {{fill: {c['cc']};}}
text, tspan {{white-space: pre;}}
</style>
<rect width="{W}px" height="{H}px" fill="{c['bg']}" rx="15"/>
<text fill="{c['fg']}">
{art}
</text>
<text fill="{c['fg']}">
{info}
</text>
</svg>
""")
