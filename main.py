import streamlit as st
from services.auth.login_wall import render_login
from services.state.session_defaults import initial_session_defaults
from services.config.workout_config import EXERCISE_OPTIONS
from services.ui.style_loader import load_styles
from services.persistence.exercise_repository import init_db
from streamlit_webrtc import webrtc_streamer,WebRtcMode
from services.vision.exercise_video_processor import VideoProcessorClass
load_styles()
def main():
    init_db()
    st.set_page_config(page_icon="💪",page_title="AI real-time GYM Coach",initial_sidebar_state="expanded",layout="centered")
    if not render_login():
        return
    initial_session_defaults()
    workout_started=st.session_state.get("workout_started",False)
    with st.sidebar:
        st.title("AI Coach")
        if st.session_state.username:
            st.caption(f"login as {st.session_state.username}")
        st.divider()
        st.subheader("Workout Plan")
        if not workout_started:
            st.selectbox("Exercise",options=EXERCISE_OPTIONS,key="plan_exercise")
            st.number_input("Sets",min_value=0,max_value=50,key="paln_sets",step=1)
            st.number_input("Reps per Set",min_value=0,max_value=50,key="paln_reps",step=1)
            st.divider()
            if st.button("Start Session",width="stretch",key="start_Session"):
                st.session_state['workout_started']=True
                st.rerun()
        else:
            exercise=st.session_state.get("plan_exercise")
            sets=st.session_state.get("plan_sets")
            reps=st.session_state.get("plan_reps")
            if st.button("End Session",key="end_session_button",width="stretch"):
                st.session_state['workout_started']=False
                st.rerun()
        if workout_started:
                st.divider()
                total_reps=st.session_state.get("reps")
                exercise=st.session_state.get("plan_exercise")
                current_set_reps=st.session_state.get("current_set_reps")
                reps_per_set=st.session_state.get("paln_reps")
                sets_completed=st.session_state.get("sets_completed")
                target_sets=st.session_state.get("plan_sets")
        
                st.subheader("Progress")  
                st.metric("Total Reps",f"{total_reps}")   
                st.metric("Current Set Reps",f"{current_set_reps}/{reps_per_set}")   
                st.metric("sets completed",f"{sets_completed}/{target_sets}")   
                st.divider()
                if exercise == "Squats":
                    st.subheader("Squat Metrics")
                    st.metric("Knee Angle", f"{st.session_state.knee_angle}°")
                    st.metric("Back Angle", f"{st.session_state.back_angle}°")
                    st.metric("Depth Status", st.session_state.depth_status)

                elif exercise == "Push-ups":
                    st.subheader("Push-up Metrics")
                    st.metric("Elbow Angle", f"{st.session_state.elbow_angle}°")
                    st.metric("Body Alignment", st.session_state.body_alignment)
                    st.metric("Hip Position", st.session_state.hip_status)

                elif exercise == "Biceps Curls (Dumbbell)":
                    st.subheader("Curl Metrics")
                    st.metric("Elbow Angle", f"{st.session_state.elbow_angle}°")
                    st.metric("Shoulder Stability", st.session_state.shoulder_status)
                    st.metric("Swing Detection", st.session_state.swing_status)

                elif exercise == "Shoulder Press":
                    st.subheader("Shoulder Press Metrics")
                    st.metric("Elbow Angle", f"{st.session_state.elbow_angle}°")
                    st.metric("Arm Extension", st.session_state.extension_status)
                    st.metric("Back Arch", st.session_state.back_arch_status)

                elif exercise == "Lunges":
                    st.subheader("Lunge Metrics")
                    st.metric("Front Knee Angle", f"{st.session_state.front_knee_angle}°")
                    st.metric("Torso Angle", f"{st.session_state.torso_angle}°")
                    st.metric("Balance Status", st.session_state.balance_status)
    st.title("AI GYM COACH")
    st.markdown("#### Real-time pose detection with proactive AI voice coaching")
    if not workout_started:
        st.html("""
<style>
    .workout-container {
        width: 680px;
        max-width: 90%;
        margin: 90px auto 0 auto;
        padding: 45px 40px;
        text-align: center;

        background: #171922;
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 20px;

        box-shadow: 0 20px 50px rgba(0,0,0,0.25);

        font-family: Arial, sans-serif;
    }

    .pointer {
        font-size: 46px;
        margin-bottom: 22px;
    }

    .title {
        margin: 0;
        color: white;
        font-size: 32px;
        font-weight: 800;
        letter-spacing: -0.8px;
    }

    .description {
        margin-top: 16px;
        color: #90929d;
        font-size: 15px;
        line-height: 1.7;
    }

    .description strong {
        color: white;
        font-weight: 600;
    }
</style>

<div class="workout-container">

    <div class="pointer">👈</div>

    <h1 class="title">
        Set your workout plan
    </h1>

    <p class="description">
        Choose your exercise sets and reps in the sidebar,
        <br>
        then click <strong>Start Workout</strong>
        to activate the camera and AI coach.
    </p>

</div>
""")
    else:
        context=webrtc_streamer(key="exercise",mode=WebRtcMode.SENDRECV,video_processor_factory=VideoProcessorClass,rtc_configuration={
        "iceServers": [
            {"urls": ["stun:stun.l.google.com:19302"]}
        ]
    },media_stream_constraints={"video":True,"audio":False},async_processing=True)
     

if __name__=="__main__":
    main()