from dotenv import load_dotenv
import os 
import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, function_tool
from pathlib import Path
import webbrowser
from urllib.parse import quote_plus
import streamlit as st

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    st.error("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")
    st.stop()

# ==================== PHYSICS-FOCUSED TOOL FUNCTIONS ====================

@function_tool
def create_physics_notes(topic: str, content: str) -> str:
    """Create a physics notes file for a specific topic."""
    filename = f"Physics_Notes_{topic.replace(' ', '_')}.txt"
    path = Path.home() / "Desktop" / filename
    
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"📚 PHYSICS NOTES - {topic.upper()}\n")
            f.write("=" * 50 + "\n\n")
            f.write(content)
            f.write(f"\n\n📝 Created by Physics Mentor\n")
        return f"✅ Physics notes for '{topic}' saved to Desktop as {filename}"
    except Exception as e:
        return f"❌ Error creating physics notes: {str(e)}"

@function_tool
def save_physics_solution(problem_title: str, solution: str) -> str:
    """Save a physics problem solution to a file."""
    filename = f"Physics_Solution_{problem_title.replace(' ', '_')}.txt"
    path = Path.home() / "Desktop" / filename
    
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"🎯 PHYSICS PROBLEM SOLUTION\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Problem: {problem_title}\n\n")
            f.write(solution)
            f.write(f"\n\n✅ Solved by Physics Mentor\n")
        return f"✅ Solution for '{problem_title}' saved to Desktop as {filename}"
    except Exception as e:
        return f"❌ Error saving solution: {str(e)}"

@function_tool
def search_physics_videos(topic: str) -> str:
    """Search YouTube for physics educational videos on a specific topic."""
    try:
        encoded_query = quote_plus(f"physics {topic} tutorial explanation")
        youtube_url = f"https://www.youtube.com/results?search_query={encoded_query}"
        webbrowser.open(youtube_url)
        return f"🎥 Opened YouTube search for physics videos on: '{topic}'"
    except Exception as e:
        return f"❌ Error searching physics videos: {str(e)}"

@function_tool
def search_physics_resources(topic: str) -> str:
    """Search Google for physics educational resources on a specific topic."""
    try:
        encoded_query = quote_plus(f"physics {topic} explanation examples problems")
        search_url = f"https://www.google.com/search?q={encoded_query}"
        webbrowser.open(search_url)
        return f"🔍 Opened Google search for physics resources on: '{topic}'"
    except Exception as e:
        return f"❌ Error searching physics resources: {str(e)}"

@function_tool
def open_physics_websites(site_type: str) -> str:
    """Open popular physics educational websites."""
    physics_sites = {
        'khan_academy': 'https://www.khanacademy.org/science/physics',
        'physics_classroom': 'https://www.physicsclassroom.com/',
        'hyperphysics': 'http://hyperphysics.phy-astr.gsu.edu/hbase/hframe.html',
        'physics_world': 'https://physicsworld.com/',
        'mit_physics': 'https://web.mit.edu/physics/',
        'feynman_lectures': 'https://www.feynmanlectures.caltech.edu/',
        'physics_forums': 'https://www.physicsforums.com/',
        'wolfram_physics': 'https://www.wolframalpha.com/examples/science-and-technology/physics',
        'nist': 'https://www.nist.gov/pml/physics-laboratory',
        'physics_today': 'https://physicstoday.scitation.org/'
    }
    
    site_key = site_type.lower().replace(' ', '_')
    
    if site_key in physics_sites:
        try:
            webbrowser.open(physics_sites[site_key])
            return f"🌐 Opened {site_type}: {physics_sites[site_key]}"
        except Exception as e:
            return f"❌ Error opening {site_type}: {str(e)}"
    else:
        available_sites = ', '.join([key.replace('_', ' ').title() for key in physics_sites.keys()])
        return f"⚠️ '{site_type}' not found. Available physics sites: {available_sites}"

@function_tool
def create_formula_sheet(exam_type: str) -> str:
    """Create a formula sheet for specific physics exams."""
    filename = f"Physics_Formulas_{exam_type.upper()}.txt"
    path = Path.home() / "Desktop" / filename
    
    formula_content = {
        'MDCAT': """
🎯 MDCAT PHYSICS FORMULAS

📐 MECHANICS:
• v = u + at
• s = ut + ½at²
• v² = u² + 2as
• F = ma
• p = mv (momentum)
• KE = ½mv²
• PE = mgh

⚡ ELECTRICITY:
• V = IR (Ohm's Law)
• P = VI = I²R = V²/R
• Q = It
• C = Q/V (Capacitance)

🌊 WAVES:
• v = fλ
• f = 1/T
• n = sin i / sin r

🔥 THERMODYNAMICS:
• PV = nRT
• Q = mcΔT
• η = W/Q × 100%
        """,
        'NEET': """
🎯 NEET PHYSICS FORMULAS

📐 MECHANICS:
• v = u + at
• s = ut + ½at²
• F = ma
• τ = Iα (Torque)
• L = Iω (Angular momentum)
• g = GM/R²

⚡ ELECTRICITY & MAGNETISM:
• F = qE
• B = μ₀I/2πr
• ε = -dΦ/dt (Faraday's Law)
• F = qvB sin θ

🌊 OPTICS:
• 1/f = 1/u + 1/v
• m = v/u = h'/h
• μ = c/v

☢️ MODERN PHYSICS:
• E = hf
• λ = h/p (de Broglie)
• E = mc²
        """,
        'JEE': """
🎯 JEE PHYSICS FORMULAS

📐 MECHANICS:
• v = u + at
• F = dp/dt
• τ = r × F
• I = Σmr²
• ω = v/r
• α = a/r

⚡ ELECTRICITY & MAGNETISM:
• ∮E⃗·dA⃗ = Q/ε₀ (Gauss Law)
• ∮B⃗·dl⃗ = μ₀I (Ampere's Law)
• ε = -dΦ/dt
• F⃗ = q(E⃗ + v⃗ × B⃗)

🌊 WAVES & OSCILLATIONS:
• x = A sin(ωt + φ)
• T = 2π√(l/g)
• v = √(T/μ)
• I ∝ A²

☢️ MODERN PHYSICS:
• E = hf = hc/λ
• p = h/λ
• ΔE = Δmc²
• R = 1.097 × 10⁷ m⁻¹
        """
    }
    
    try:
        content = formula_content.get(exam_type.upper(), "Formula sheet for general physics topics")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ {exam_type.upper()} physics formula sheet created on Desktop as {filename}"
    except Exception as e:
        return f"❌ Error creating formula sheet: {str(e)}"

# ==================== AGENT INITIALIZATION ====================

@st.cache_resource
def initialize_agent():
    """Initialize the Physics Mentor agent once and cache it"""
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )

    agent = Agent(
        name="Physics Mentor",
        instructions="""
You are a highly experienced, professional Physics teacher with deep command over both foundational and advanced topics in Physics. 

You specialize in helping students prepare for competitive exams like MDCAT, NEET, JEE, and JEE Advanced, as well as intermediate-level (1st-year and 2nd-year) Physics.

-- Don't answer on the other subject question from physics and simply response that you are trained to answer and discussed about physics subject and will not answer about different topics of any other subjects

🧠 Teaching Style:
- Friendly, engaging, and easy to understand
- Step-by-step solutions with clear logic
- Break down complex problems into simple steps
- Use real-world analogies where helpful
- Tailor explanations based on exam level and context

📚 Response Structure & Formatting Guidelines:

1. **Use Unicode math symbols** instead of LaTeX:
   - ∫ for integration, ∂ for partial derivative
   - ≈ (approximately), ≤ (less than or equal), ≥ (greater than or equal)
   - ∞ (infinity), π (pi), θ (theta), α, β, γ (Greek letters)
   - Subscripts like v₀, a₁, F₂ and superscripts like x², t³

2. **Represent fractions** as:
   - Simple division: dv/dt
   - Unicode fractions (½, ¼, ¾) when appropriate
   - Or (numerator)/(denominator) if needed

3. **Structure all numerical solutions like this:**
   - 🎯 **Given:** (List all known values clearly)
   - 📘 **Step 1:** (State the formula or principle used)
   - 🧮 **Step 2:** (Plug in values and perform calculations)
   - ⏱️ **Step 3:** (Final calculation step)
   - ✅ **Final Answer:** (Clearly box the answer with units)

4. **Visual clarity:**
   - Use bullet points for lists
   - Add blank lines between sections for readability
   - Keep symbols and math expressions clean and easy to scan

5. **Use emojis** thoughtfully to make steps more visually engaging:
   - 🎯 for known values
   - 📘 for concept/formula steps
   - 🧮 for calculations
   - ⏱️ for timing or computation focus
   - ✅ for the final answer
   - ❌ for common mistakes (if explaining an error)

🚫 Avoid:
- Complex LaTeX
- Overloaded formulas without explanation
- Jumping steps or skipping reasoning

🎓 Your goal is to make every answer feel like a personalized tutoring session, ensuring the student not only gets the correct result but understands how and why.

Stay strictly focused on Physics, and keep answers aligned to the student's exam level and learning goals.

When students ask you to save notes, solutions, or create formula sheets, use the appropriate tools to help them organize their study materials.
""",
        tools=[create_physics_notes, save_physics_solution, search_physics_videos, 
               search_physics_resources, open_physics_websites, create_formula_sheet]
    )
    
    return agent, config

def extract_response_text(result):
    """Extract clean text from RunResult"""
    try:
        result_str = str(result)
        
        if "Final output (str):" in result_str:
            parts = result_str.split("Final output (str):")
            if len(parts) > 1:
                content = parts[1].strip()
                lines = content.split('\n')
                clean_lines = []
                for line in lines:
                    if line.startswith('- ') and ('new item' in line or 'raw response' in line):
                        break
                    clean_lines.append(line)
                return '\n'.join(clean_lines).strip()
        
        return result_str
    except Exception as e:
        return str(result)

# ==================== ASYNC RUNNER FUNCTION ====================

async def run_agent_async(agent, user_input, config):
    """Run the agent asynchronously"""
    try:
        response = await Runner.run(
            agent,
            input=user_input,
            run_config=config
        )
        return extract_response_text(response)
    except Exception as e:
        return f"❌ Error running agent: {str(e)}"

def run_agent_sync(agent, user_input, config):
    """Synchronous wrapper for the async agent runner"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(run_agent_async(agent, user_input, config))
            return result
        finally:
            loop.close()
    except Exception as e:
        return f"❌ Error in sync wrapper: {str(e)}"

# ==================== STREAMLIT UI ====================

st.set_page_config(
    page_title="Physics Mentor AI",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 Physics Mentor - Your AI Physics Teacher")
st.markdown("*Specialized in MDCAT, NEET, JEE preparation and intermediate Physics*")

# Initialize agent
agent, config = initialize_agent()

# Sidebar with physics-specific instructions
with st.sidebar:
    st.header("📚 Physics Mentor Guide")
    st.markdown("""
    ### 🎯 What I Can Help With:
    - **Problem Solving**: Step-by-step solutions with clear explanations
    - **Concept Clarification**: Breaking down complex physics topics
    - **Exam Preparation**: MDCAT, NEET, JEE, JEE Advanced
    - **Formula Sheets**: Create organized formula collections
    - **Study Resources**: Find physics videos and materials
    
    ### 📝 Study Tools:
    - Save physics notes and solutions to files
    - Create exam-specific formula sheets
    - Search for educational videos and resources
    - Access top physics learning websites
    
    ### 🎓 Exam Focus Areas:
    - **MDCAT**: Medical entrance preparation
    - **NEET**: National medical entrance
    - **JEE/JEE Advanced**: Engineering entrance
    - **Intermediate**: 1st & 2nd year physics
    
    ### 💡 Example Questions:
    - "Solve this kinematics problem step by step"
    - "Explain Newton's laws with examples"
    - "Create a formula sheet for NEET"
    - "Find videos about electromagnetic induction"
    - "Save these notes about thermodynamics"
    """)
    
    st.markdown("---")
    st.markdown("**🌐 Physics Resources:**")
    st.markdown("Khan Academy, Physics Classroom, HyperPhysics, Feynman Lectures, Physics Forums, Wolfram Physics")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me any physics question..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("🧠 Thinking through the physics..."):
            try:
                clean_response = run_agent_sync(agent, prompt, config)
                st.markdown(clean_response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": clean_response})
                
            except Exception as e:
                error_message = f"❌ Error: {str(e)}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})

# Clear chat button
st.markdown("---")
if st.button("🗑️ Clear Chat", type="secondary"):
    st.session_state.messages = []
    st.rerun()

# Physics-specific footer
st.markdown("---")
st.markdown("**🧠 Physics Learning Tips:**")
st.markdown("- Always start with understanding the concept before solving problems")
st.markdown("- Practice numerical problems regularly for exam preparation")
st.markdown("- Use the formula sheets and save important solutions for revision")
st.markdown("- Ask for step-by-step explanations when you're stuck")
st.markdown("- Focus on understanding the 'why' behind each formula")

# Debug section
with st.expander("🔧 Debug Info"):
    st.write(f"Desktop path: {Path.home() / 'Desktop'}")
    st.write(f"Current working directory: {os.getcwd()}")
    st.write(f"API Key present: {bool(gemini_api_key)}")
    st.write("Physics Mentor Agent: ✅ Active")