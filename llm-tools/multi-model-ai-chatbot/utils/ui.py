import streamlit as st

MODELS_META = [
    {"key": "gemini",   "label": "Gemini 2.5 Flash", "icon": "✦", "color": "#4285F4", "quad": "Q2"},
    {"key": "openai",   "label": "GPT-4o mini",       "icon": "◈", "color": "#10A37F", "quad": "Q1"},
    {"key": "grok",     "label": "Grok (xAI)",        "icon": "⬡", "color": "#FF6B35", "quad": "Q3"},
    {"key": "deepseek", "label": "DeepSeek Chat",     "icon": "◇", "color": "#7C3AED", "quad": "Q4"},
]

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg:       #09090f;
    --bg2:      #0f1018;
    --bg3:      #14151f;
    --bg4:      #1a1b28;
    --border:   #1e2035;
    --border2:  #2a2c42;
    --txt:      #dde0f0;
    --txt2:     #6e7190;
    --txt3:     #373952;
    --ax:       #252840;
    --ax-glow:  #3a3d68;
}

html, body, .stApp {
    background: var(--bg) !important;
    color: var(--txt) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Kill Streamlit's default top padding and widen the block */
.block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 0.5rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    max-width: 100% !important;
}

/* Remove all default margins Streamlit adds between elements */
.element-container {
    margin-bottom: 0 !important;
}

/* Kill the gap Streamlit puts between column children */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
    gap: 0 !important;
}

div[data-testid="column"] > div {
    gap: 0 !important;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }

/* ── Header ── */
.app-header {
    text-align: center;
    padding: 0.5rem 0 0.4rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 0.4rem;
}
.app-header h1 {
    font-family: 'Space Mono', monospace !important;
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: -1px;
    background: linear-gradient(130deg, #4285F4 0%, #10A37F 33%, #FF6B35 66%, #7C3AED 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
}
.app-header p {
    color: var(--txt3);
    font-size: 0.68rem;
    margin: 0.15rem 0 0;
    letter-spacing: 1px;
    text-transform: uppercase;
    font-family: 'Space Mono', monospace;
}

/* ── Axis label row ── */
.axis-labels-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 0.3rem;
    margin-bottom: 0.2rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: var(--txt3);
    letter-spacing: 0.8px;
}
.axis-label { flex: 1; text-align: center; }
.axis-origin {
    color: var(--ax-glow);
    font-size: 0.9rem;
    padding: 0 0.4rem;
    text-shadow: 0 0 10px var(--ax-glow);
}

/* ── Vertical axis ── */
.axis-v {
    width: 2px;
    height: 100%;
    min-height: 60px;
    background: linear-gradient(180deg,
        transparent 0%, var(--ax) 20%, var(--ax-glow) 50%, var(--ax) 80%, transparent 100%);
    box-shadow: 0 0 8px var(--ax-glow);
    margin: 0 auto;
    border-radius: 1px;
}

/* ── Horizontal axis ── */
.axis-h-wrap { padding: 0; margin: 0; line-height: 0; }
.axis-h {
    height: 2px;
    width: 100%;
    background: linear-gradient(90deg,
        transparent 0%, var(--ax) 10%, var(--ax-glow) 50%, var(--ax) 90%, transparent 100%);
    box-shadow: 0 0 8px var(--ax-glow);
    border-radius: 1px;
}

/* ── Quadrant header — the ONLY chrome per panel ── */
.q-header {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    background: var(--bg3);
    border-bottom: 1px solid var(--border);
    /* border-top or border-bottom set inline per quadrant */
}
.q-icon {
    width: 26px;
    height: 26px;
    border-radius: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    font-weight: 700;
    flex-shrink: 0;
}
.q-titles {
    display: flex;
    flex-direction: column;
    gap: 1px;
    flex: 1;
    min-width: 0;
}
.q-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--txt);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.q-provider {
    font-size: 0.58rem;
    color: var(--txt3);
    letter-spacing: 0.8px;
    text-transform: uppercase;
}
.q-quad-badge {
    font-family: 'Space Mono', monospace;
    font-size: 0.58rem;
    color: var(--txt3);
    letter-spacing: 0.5px;
    flex-shrink: 0;
}
.q-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    flex-shrink: 0;
    animation: qdot 2.4s ease-in-out infinite;
}
@keyframes qdot {
    0%,100% { opacity:1; transform:scale(1); }
    50%      { opacity:0.35; transform:scale(0.7); }
}

/* ── User message bubble ── */
.q-user-msg {
    display: flex;
    justify-content: flex-end;
    padding: 8px 10px 4px;
    margin: 0;
}
.q-user-bubble {
    background: #131d2e;
    border: 1px solid #1d3050;
    border-radius: 8px 8px 2px 8px;
    padding: 6px 10px;
    max-width: 90%;
    font-size: 0.82rem;
    line-height: 1.45;
    color: #b8c8e0;
    word-break: break-word;
}

/* ── Response area — tight top margin ── */
.q-response {
    padding: 4px 10px 0;
    margin: 0;
}

/* Override Streamlit paragraph margins inside quadrants */
.stMarkdown p {
    font-size: 0.85rem !important;
    line-height: 1.6 !important;
    color: var(--txt) !important;
    margin: 0.2rem 0 0.2rem !important;
}
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.88rem !important;
    color: var(--txt) !important;
    margin: 0.4rem 0 0.15rem !important;
}
.stMarkdown ul, .stMarkdown ol {
    font-size: 0.83rem !important;
    padding-left: 1.1rem !important;
    margin: 0.2rem 0 !important;
}
.stMarkdown li { margin: 0.1rem 0 !important; }

/* ── Turn divider ── */
hr.q-divider {
    border: none !important;
    border-top: 1px dashed var(--border2) !important;
    margin: 0.5rem 10px !important;
    opacity: 0.4;
}

/* ── Empty hint — compact, no large padding ── */
.q-empty-hint {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 12px;
}
.q-empty-text {
    font-size: 0.68rem;
    color: var(--txt3);
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.5px;
}

/* ── Caption / meta ── */
[data-testid="stCaptionContainer"], .stCaption {
    color: var(--txt3) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.62rem !important;
    padding: 0 10px 4px !important;
    margin: 0 !important;
}

/* ── Code ── */
code {
    background: #0d0f1a !important;
    border: 1px solid var(--border2) !important;
    border-radius: 3px !important;
    padding: 1px 4px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.78em !important;
    color: #4ade80 !important;
}
pre code { padding: 0 !important; border: none !important; color: inherit !important; }
pre {
    background: #060810 !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    padding: 0.6rem !important;
    font-size: 0.76rem !important;
    margin: 0.3rem 10px !important;
}

/* ── Input ── */
.input-spacer { height: 0.4rem; }
.stChatInput {
    border: 1px solid var(--border2) !important;
    border-radius: 8px !important;
    background: var(--bg3) !important;
}
.stChatInput textarea {
    background: transparent !important;
    color: var(--txt) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: #4285F4 !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] label {
    color: var(--txt2) !important;
    font-size: 0.78rem !important;
}
.sidebar-logo {
    font-family: 'Space Mono', monospace;
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--txt);
    padding: 0.6rem 0 0.15rem;
}
.sidebar-sub {
    color: var(--txt3);
    font-size: 0.65rem;
    margin-bottom: 0.9rem;
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.5px;
}
.sidebar-section {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: var(--txt3);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 0.8rem 0 0.3rem;
    border-top: 1px solid var(--border);
    margin-top: 0.3rem;
}
.q-model-card {
    display: flex;
    align-items: center;
    gap: 8px;
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 5px;
    padding: 6px 9px;
    margin: 3px 0;
}
.q-model-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
.q-model-name { font-size: 0.77rem; color: var(--txt); font-weight: 500; flex: 1; }
.q-model-quad { font-family: 'Space Mono', monospace; font-size: 0.58rem; color: var(--txt3); }
.stat-pill {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 2px 8px;
    font-size: 0.65rem;
    color: var(--txt3);
    font-family: 'Space Mono', monospace;
}
.stButton > button {
    background: var(--bg3) !important;
    color: var(--txt) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 5px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    border-color: #4285F4 !important;
    color: #4285F4 !important;
    box-shadow: 0 0 10px #4285F420 !important;
}

/* Sidebar mini-map grid */
.mini-map {
    display: grid;
    grid-template-columns: 1fr 2px 1fr;
    grid-template-rows: auto 2px auto;
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 5px;
    overflow: hidden;
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
}
.mm-cell {
    padding: 7px 9px;
    background: var(--bg2);
}
.mm-ax-v { background: linear-gradient(180deg, var(--ax), var(--ax-glow), var(--ax)); }
.mm-ax-h { background: linear-gradient(90deg, var(--ax), var(--ax-glow), var(--ax)); height: 2px; }
.mm-name { font-weight: 700; margin-bottom: 2px; }
.mm-pos  { font-size: 0.52rem; color: var(--txt3); }
</style>
"""


def apply_custom_css():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_header():
    st.markdown("""
    <div class="app-header">
        <h1>⊕ MultiMind AI</h1>
        <p>XY · Gemini · GPT · Grok · DeepSeek</p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">⊕ MultiMind AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-sub">XY quadrant · 4-model parallel</div>', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-section">Quadrant Map</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="mini-map">
            <div class="mm-cell" style="border-right:1px solid #1e2035;border-bottom:1px solid #1e2035;">
                <div class="mm-name" style="color:#4285F4;">✦ Gemini</div>
                <div class="mm-pos">Q2 · top-left</div>
            </div>
            <div class="mm-ax-v" style="border-bottom:1px solid #1e2035;"></div>
            <div class="mm-cell" style="border-left:1px solid #1e2035;border-bottom:1px solid #1e2035;">
                <div class="mm-name" style="color:#10A37F;">◈ GPT</div>
                <div class="mm-pos">Q1 · top-right</div>
            </div>
            <div class="mm-ax-h"></div>
            <div style="background:#3a3d68;box-shadow:0 0 6px #3a3d68;"></div>
            <div class="mm-ax-h"></div>
            <div class="mm-cell" style="border-right:1px solid #1e2035;border-top:1px solid #1e2035;">
                <div class="mm-name" style="color:#FF6B35;">⬡ Grok</div>
                <div class="mm-pos">Q3 · bottom-left</div>
            </div>
            <div class="mm-ax-v" style="border-top:1px solid #1e2035;"></div>
            <div class="mm-cell" style="border-left:1px solid #1e2035;border-top:1px solid #1e2035;">
                <div class="mm-name" style="color:#7C3AED;">◇ DeepSeek</div>
                <div class="mm-pos">Q4 · bottom-right</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sidebar-section">Active Models</div>', unsafe_allow_html=True)
        for m in MODELS_META:
            st.markdown(f"""
            <div class="q-model-card">
                <span class="q-model-dot" style="background:{m['color']};box-shadow:0 0 5px {m['color']}88;"></span>
                <span class="q-model-name">{m['icon']} {m['label']}</span>
                <span class="q-model-quad">{m['quad']}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="sidebar-section">Actions</div>', unsafe_allow_html=True)
        clear = st.button("🗑 Clear all quadrants", use_container_width=True)

        turns = st.session_state.get("turns", [])
        if turns:
            n = len(turns)
            st.markdown(f"""
            <div style="margin-top:0.6rem;">
                <span class="stat-pill">⊕ {n} turn{"s" if n!=1 else ""} · {n*4} responses</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div style="position:fixed;bottom:0.6rem;font-size:0.58rem;color:#1a1c2e;
                    font-family:'Space Mono',monospace;">MultiMind AI · XY</div>
        """, unsafe_allow_html=True)

    return clear