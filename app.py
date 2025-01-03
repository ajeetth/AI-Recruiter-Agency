import streamlit as st
import asyncio
import os
from datetime import datetime
from pathlib import Path
from streamlit_option_menu import option_menu


# configure streamlit page
st.set_page_config(
    page_title="AI  Recruiter Agency",
    page_icon= "🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# custom css

st.markdown(
    """
    <style>
    .stProgress .st-bo {
            background-color: #00a0dc;
        }
        .success-text {
            color: #00c853;
        }
        .warning-text {
            color: #ffd700;
        }
        .error-text {
            color: #ff5252;
        }
        .st-emotion-cache-1v0mbdj.e115fcil1 {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 20px;
        }
    </style>""",
    unsafe_allow_html=True,
)

async def process_resume(file_path:str)->dict:
    """Process resume through the AI recruitment pipeline."""
    pass

def save_uploaded_file(uploaded_file)->str:
    """Save uploaded file and return path"""
    try:
        # creates uploads directory if it doesn't exist
        save_dir = Path("uploads")
        save_dir.mkdir(exist_ok=True)

        # Generate unique file name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = save_dir / f"resume_{timestamp}_{uploaded_file.name}"

        # Save file to disk
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        return str(file_path)
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
        raise e

def main():
    # sidebar navigation
    with st.sidebar:
        st.image(
            "https://img.icons8.com/resume",
            width=50
        )
        st.title("AI Recruiter Agency")
        selected = option_menu(
            menu_title="Navigation",
            options=["Upload resume", "About"],
            menu_icon="cast",
            default_index=0
        )
        if selected == "Upload resume":
            st.header("📄Resume Analysis")
            st.write("Upload A resume to get AI powered insights")

            uploaded_file = st.file_uploader(
                "Choose a PDF resume file",
                type=["pdf"],
                help="Upload a PDF resume file to analyze"
            )
            if uploaded_file:
                try:
                    with st.spinner("Saving uploaded file ..."):
                        resume_path = save_uploaded_file(uploaded_file)
                    st.info("Resume uploaded successfully! Processing ...")

                    # create place holder for progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    # process resume
                    try:
                        status_text.info("Analyzing resume ...")
                        progress_bar.progress(50)

                        result = asyncio.run(process_resume(resume_path))

                        if result["status"] == "completed":
                            progress_bar.progress(100)
                            status_text.success("Analysis complete!")

                            # Dkisplay the tabs
                            tab1, tab2, tab3, tab4 = st.tabs(
                                [
                                    "📊 Analysis",
                                    "💼 Job Matches",
                                    "🎯 Screening",
                                    "💡 Recommendations"
                                ]
                            )
                            with tab1:
                                st.subheader("Skills Analysis")
                                st.write(result["analysis results"]["skills analysis"])
                                st.metric(
                                    "confident score",
                                    f"{result['analysis results']['confidence score']}:.0 %"
                                )
                            with tab2:
                                st.subheader("Matched Positions")
                                if not result["job matches"]["matched_jobs"]:
                                    st.warning("No matched positions found.")

                                seen_titles = (
                                    set()
                                ) # keep track of seen titles to avoid duplicates 
                                for job in result["job matches"]["matched_jobs"]:
                                    if job["title"] in seen_titles:
                                        continue
                                    seen_titles.add(job["title"])

                                    with st.container():
                                        col1, col2, col3 = st.columns([2, 1, 1])
                                        with col1:
                                            st.write(f"**{job["title"]}**")
                                        with col2:
                                            st.write(
                                                f"Match: {job.get('match_score', 'N/A')}"
                                            )
                                        with col3:
                                            st.write(f"📍 {job.get('location', 'N/A')}")
                                    st.divider()

                            with tab3:
                                st.subheader("Screening Results")
                                st.metric(
                                    "Screening Score",
                                    f"{result['screening results']['screening_score']} %"
                                )
                                st.write(result["screening results"]["screening_report"])

                            with tab4:
                                st.subheader("FinalRecommendations")
                                st.info(
                                    result["recommendations"]["final_recommendations"],
                                    icon="💡"
                                )
                            
                            # save Results
                            output_dir = Path("results")
                            output_dir.mkdir(exist_ok=True)
                            output_file = (
                                output_dir 
                                / f"{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
                            )

                            with open(output_file, "w") as f:
                                f.write(str(result))

                            st.success(f"Results saved to {output_file}")

                        else:
                            st.error(
                                f"Process failed at stage {result['current_stage']}\n"
                                f"Erorr: {result.get('error', 'Unknown error')}"
                            )

                    except Exception as e:
                        st.error(f"Error processing resume: str({e})")

                    finally:
                        try:
                            os.remove(resume_path)
                        except Exception as e:
                            st.error(f"Error removing temporary file: str({e})")       

                except Exception as e:
                    st.error(f"Error saving uploaded file: str({e})")

        elif selected == "About":
            st.header("About AI Recruiter Agency")
            st.write(
                """
                Welcome to AI Recruiter Agency, a cutting-edge recruitment analysis system powered by:
        
                - **Ollama (llama3.2)**: Advanced language model for natural language processing
                - **Swarm Framework**: Coordinated AI agents for specialized tasks
                - **Streamlit**: Modern web interface for easy interaction
        
                Our system uses specialized AI agents to:
                1. 📄 Extract information from resumes
                2. 🔍 Analyze candidate profiles
                3. 🎯 Match with suitable positions
                4. 👥 Screen candidates
                5. 💡 Provide detailed recommendations
        
                Upload a resume to experience AI-powered recruitment analysis!
                """
            )


if __name__ == "__main__":
    main()