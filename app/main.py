import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

# --- App Styling --- (Integrated Fun Styles)
def set_page_config():
    st.set_page_config(layout="wide", page_title="AutoPitch: Cold Email Generator", page_icon="📧")
    st.markdown(
        """
        <style>
            body {
                background-color: #0d0d0d;
                color: #f2f2f2;
                cursor: url('https://cdn-icons-png.flaticon.com/512/60/60992.png'), auto;
            }
            .main {
                background-color: #0d0d0d;
                padding: 2rem;
            }

            .app-header {
                margin-bottom: 2rem;
            }

            .app-header h1 {
                font-size: 3.5rem;
                font-weight: 800;
                color: #ffffff;
                margin-bottom: 0.5rem;
                letter-spacing: -1px;
                background: linear-gradient(to right, #4c8bf5, #8c52ff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: fadeIn 2s ease-out;
            }

            .app-header h3 {
                font-size: 1.7rem;
                font-weight: 500;
                color: #bbbbbb;
                margin-top: 0;
                margin-bottom: 0.8rem;
                animation: fadeIn 2.5s ease-out;
            }

            .app-header p {
                font-size: 1rem;
                color: #aaaaaa;
                margin-bottom: 2.5rem;
                line-height: 1.6;
                max-width: 700px;
                animation: fadeIn 3s ease-out;
            }

            .stTextInput>div>div>input {
                font-size: 16px;
                padding: 0.5rem;
                background-color: #1a1a1a;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 4px;
                transition: background-color 0.3s ease;
            }

            .stTextInput>div>div>input:focus {
                background-color: #333;
                border-color: #4c8bf5;
            }

            .stButton>button {
                background-color: #000000;
                color: white;
                font-size: 16px;
                padding: 0.6rem 1.2rem;
                border-radius: 8px;
                border: none;
                transition: background-color 0.3s ease, transform 0.2s;
            }

            .stButton>button:hover {
                background-color: #22222;
                transform: scale(1.1);
                box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.3);
            }

            .stButton>button:active {
                transform: scale(1);
            }

            .email-box {
                background-color: #1a1a1a;
                border-left: 5px solid #4c8bf5;
                padding: 1rem;
                margin-bottom: 1.5rem;
                border-radius: 6px;
                font-family: monospace;
                color: #f2f2f2;
                animation: fadeIn 1.5s ease-out;
            }

            .email-box a {
                color: #66ccff !important;
                text-decoration: underline;
            }

            @keyframes fadeIn {
                0% { opacity: 0; }
                100% { opacity: 1; }
            }
        </style>
        """, unsafe_allow_html=True
    )


# --- Fun: Confetti Animation ---
def trigger_confetti():
    st.markdown(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.4.0/dist/confetti.browser.min.js"></script>
        <script>
            function fireConfetti() {
                var myCanvas = document.createElement('canvas');
                document.body.appendChild(myCanvas);
                var myConfetti = confetti.create(myCanvas, {
                    resize: true,
                    useWorker: true
                });
                myConfetti({ particleCount: 300, spread: 70, origin: { x: 0.5, y: 0.5 } });
            }
            fireConfetti();
        </script>
        """, unsafe_allow_html=True
    )


# --- App Functionality ---
def create_streamlit_app(llm, portfolio, clean_text):
    st.markdown("""
        <div class="app-header">
            <h1>AutoPitch</h1>
            <h3>Cold Mail Generator</h3>
            <p>Craft customized cold emails by simply pasting a job URL. Let AI do the outreach!</p>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        url_input = st.text_input("🔗 Enter a Job URL:",
                                  value="https://www.amazon.jobs/en/jobs/2959878/system-development-engineer-ii-realm-hyd")
        submit_button = st.button("🚀 Generate Cold Email")

    if submit_button:
        trigger_confetti()  # Trigger confetti on button click
        try:
            with st.spinner("⏳ Processing..."):
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)

                if not jobs:
                    st.warning("No job information extracted from the URL.")
                    return

                for idx, job in enumerate(jobs):
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)

                    with st.container():
                        st.markdown(f"#### 📩 Email {idx + 1}")
                        st.markdown(f'<div class="email-box">{email}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ An Error Occurred: {e}")


# --- App Execution ---
if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    set_page_config()
    create_streamlit_app(chain, portfolio, clean_text)
