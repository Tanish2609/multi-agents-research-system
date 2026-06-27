import streamlit as st
import time
from pipeline import run_research_pipeline

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---------- fonts ---------- */
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@300;400;500;600&display=swap');

/* ---------- root tokens ---------- */
:root {
    --bg:       #0D0F12;
    --surface:  #151820;
    --border:   #252A34;
    --accent:   #5B7FFF;
    --accent2:  #A78BFA;
    --text:     #E8EAF0;
    --muted:    #6B7280;
    --search:   #1A3A2A;
    --reader:   #1A2840;
    --writer:   #2A1A3A;
    --critic:   #3A2A1A;
    --search-a: #34D399;
    --reader-a: #60A5FA;
    --writer-a: #C084FC;
    --critic-a: #FB923C;
}

/* ---------- global reset ---------- */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] { display: none; }
[data-testid="stSidebar"] { background-color: var(--surface) !important; }
.block-container { padding: 2rem 3rem !important; max-width: 1100px; }

/* ---------- hero ---------- */
.hero {
    text-align: center;
    padding: 3.5rem 1rem 2.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.5rem;
}
.hero-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}
.hero-title {
    font-size: 3rem;
    font-weight: 600;
    letter-spacing: -0.03em;
    line-height: 1.1;
    background: linear-gradient(135deg, var(--text) 40%, var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.75rem;
}
.hero-sub {
    color: var(--muted);
    font-size: 1rem;
    font-weight: 300;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ---------- search box ---------- */
.stTextInput > div > div > input {
    background-color: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(91, 127, 255, 0.15) !important;
}
.stTextInput > div > div > input::placeholder { color: var(--muted) !important; }

/* ---------- button ---------- */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 2rem !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.15s !important;
    width: 100% !important;
}
.stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* ---------- pipeline stage cards ---------- */
.stage-card {
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    border: 1px solid var(--border);
}
.stage-card.search { background: var(--search); border-color: #2D5A44; }
.stage-card.reader { background: var(--reader); border-color: #2D4470; }
.stage-card.writer { background: var(--writer); border-color: #4A2D6A; }
.stage-card.critic { background: var(--critic); border-color: #6A4A2D; }

.stage-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 0.5rem;
}
.stage-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    display: inline-block;
    flex-shrink: 0;
}
.stage-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    font-weight: 600;
}
.stage-card.search .stage-dot  { background: var(--search-a); }
.stage-card.reader .stage-dot  { background: var(--reader-a); }
.stage-card.writer .stage-dot  { background: var(--writer-a); }
.stage-card.critic .stage-dot  { background: var(--critic-a); }
.stage-card.search .stage-label { color: var(--search-a); }
.stage-card.reader .stage-label { color: var(--reader-a); }
.stage-card.writer .stage-label { color: var(--writer-a); }
.stage-card.critic .stage-label { color: var(--critic-a); }

.stage-content {
    color: var(--text);
    font-size: 0.9rem;
    line-height: 1.7;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ---------- progress bar ---------- */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
    border-radius: 99px !important;
}
.stProgress > div > div {
    background: var(--border) !important;
    border-radius: 99px !important;
    height: 4px !important;
}

/* ---------- status text ---------- */
.status-line {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    color: var(--muted);
    text-align: center;
    padding: 0.4rem 0;
}

/* ---------- divider ---------- */
.section-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 2rem 0;
}

/* ---------- result section title ---------- */
.result-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 1.25rem;
}

/* ---------- error ---------- */
.stAlert { border-radius: 10px !important; }

/* ---------- expander ---------- */
details > summary {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.1em !important;
    color: var(--muted) !important;
    cursor: pointer;
}
[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}

/* ---------- hide streamlit branding ---------- */
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-label">Multi-Agent System</div>
    <div class="hero-title">Research Intelligence</div>
    <div class="hero-sub">Four specialized agents work in sequence — searching, scraping, writing, and critiquing — to produce a polished research report on any topic.</div>
</div>
""", unsafe_allow_html=True)


# ── Pipeline stage metadata ───────────────────────────────────────────────────
STAGES = [
    {
        "key":    "search_results",
        "cls":    "search",
        "icon":   "🔍",
        "label":  "Search Agent",
        "desc":   "Querying the web for recent, reliable sources",
        "status": "Searching the web…",
    },
    {
        "key":    "scraped_content",
        "cls":    "reader",
        "icon":   "📄",
        "label":  "Reader Agent",
        "desc":   "Scraping top URLs for deeper content",
        "status": "Scraping top URLs…",
    },
    {
        "key":    "report",
        "cls":    "writer",
        "icon":   "✍️",
        "label":  "Writer",
        "desc":   "Drafting a structured research report",
        "status": "Drafting the report…",
    },
    {
        "key":    "feedback",
        "cls":    "critic",
        "icon":   "🧠",
        "label":  "Critic",
        "desc":   "Reviewing and scoring the report",
        "status": "Reviewing the report…",
    },
]


# ── Input row ─────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1], gap="small")

with col_input:
    topic = st.text_input(
        label="topic",
        placeholder="e.g.  Quantum computing breakthroughs in 2025",
        label_visibility="collapsed",
    )

with col_btn:
    run = st.button("Run →", use_container_width=True)


# ── Session state ─────────────────────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None
if "running" not in st.session_state:
    st.session_state.running = False


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.result = None
        st.session_state.running = True

        st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
        st.markdown('<div class="result-title">Pipeline Progress</div>', unsafe_allow_html=True)

        progress_bar = st.progress(0)
        status_placeholder = st.empty()
        stage_placeholders = [st.empty() for _ in STAGES]

        try:
            # We intercept each stage by running them one by one via the same
            # functions used in pipeline.py — re-using the imported chains/agents.
            from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

            state = {}
            total = len(STAGES)

            def render_stage(idx, content, done=False):
                s = STAGES[idx]
                spinner = "" if done else " <span style='color:var(--muted)'>…</span>"
                stage_placeholders[idx].markdown(f"""
<div class="stage-card {s['cls']}">
    <div class="stage-header">
        <span class="stage-dot"></span>
        <span class="stage-label">{s['icon']} {s['label']}</span>
    </div>
    <div class="stage-content">{content}{'' if done else spinner}</div>
</div>
""", unsafe_allow_html=True)

            # ── Stage 0: Search ───────────────────────────────────────────────
            status_placeholder.markdown(
                f'<div class="status-line">⚡ {STAGES[0]["status"]}</div>',
                unsafe_allow_html=True,
            )
            render_stage(0, "Querying the web for relevant, up-to-date sources…")
            progress_bar.progress(5)

            search_agent = build_search_agent()
            search_result = search_agent.invoke({
                "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
            })
            state["search_results"] = search_result["messages"][-1].content

            render_stage(0, state["search_results"], done=True)
            progress_bar.progress(25)

            # ── Stage 1: Reader ───────────────────────────────────────────────
            status_placeholder.markdown(
                f'<div class="status-line">⚡ {STAGES[1]["status"]}</div>',
                unsafe_allow_html=True,
            )
            render_stage(1, "Picking the most relevant URL and scraping for deeper content…")
            progress_bar.progress(30)

            reader_agent = build_reader_agent()
            read_result = reader_agent.invoke({
                "messages": [(
                    "user",
                    f"Based on the following search results about {topic}, "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{state['search_results'][:800]}"
                )]
            })
            state["scraped_content"] = read_result["messages"][-1].content

            render_stage(1, state["scraped_content"], done=True)
            progress_bar.progress(50)

            # ── Stage 2: Writer ───────────────────────────────────────────────
            status_placeholder.markdown(
                f'<div class="status-line">⚡ {STAGES[2]["status"]}</div>',
                unsafe_allow_html=True,
            )
            render_stage(2, "Synthesising search results and scraped content into a structured report…")
            progress_bar.progress(55)

            combined = (
                f"Search results:\n{state['search_results']}\n\n"
                f"Detailed scraped content:\n{state['scraped_content']}"
            )
            state["report"] = writer_chain.invoke({"topic": topic, "research": combined})

            render_stage(2, state["report"], done=True)
            progress_bar.progress(75)

            # ── Stage 3: Critic ───────────────────────────────────────────────
            status_placeholder.markdown(
                f'<div class="status-line">⚡ {STAGES[3]["status"]}</div>',
                unsafe_allow_html=True,
            )
            render_stage(3, "Critically reviewing the report for accuracy, depth, and clarity…")
            progress_bar.progress(80)

            state["feedback"] = critic_chain.invoke({"report": state["report"]})

            render_stage(3, state["feedback"], done=True)
            progress_bar.progress(100)

            status_placeholder.markdown(
                '<div class="status-line" style="color: var(--search-a)">✓ Pipeline complete</div>',
                unsafe_allow_html=True,
            )

            st.session_state.result = state

        except Exception as e:
            st.error(f"Pipeline error: {e}")

        st.session_state.running = False


# ── Show previous result (after rerun) ───────────────────────────────────────
elif st.session_state.result:
    state = st.session_state.result

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    st.markdown('<div class="result-title">Last Research Run</div>', unsafe_allow_html=True)

    for s in STAGES:
        content = state.get(s["key"], "")
        st.markdown(f"""
<div class="stage-card {s['cls']}">
    <div class="stage-header">
        <span class="stage-dot"></span>
        <span class="stage-label">{s['icon']} {s['label']}</span>
    </div>
    <div class="stage-content">{content}</div>
</div>
""", unsafe_allow_html=True)


# ── Pipeline diagram (always visible) ────────────────────────────────────────
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

with st.expander("HOW THE PIPELINE WORKS"):
    st.markdown("""
<div style="font-family:'IBM Plex Mono',monospace; font-size:0.8rem; color:#6B7280; line-height:2;">

  🔍  <span style="color:#34D399">Search Agent</span>
       Queries the web and returns relevant, recent results for your topic.
       ↓
  📄  <span style="color:#60A5FA">Reader Agent</span>
       Picks the most useful URL from the results and scrapes full page content.
       ↓
  ✍️  <span style="color:#C084FC">Writer</span>
       Combines search + scraped data and drafts a structured research report.
       ↓
  🧠  <span style="color:#FB923C">Critic</span>
       Reviews the draft for accuracy, depth, gaps, and overall quality.

</div>
""", unsafe_allow_html=True)