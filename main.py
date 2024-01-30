import streamlit as st
from streamlit_mic_recorder import mic_recorder,speech_to_text
from whisper import WhisperSTT
from openai import OpenAI

st.title('GREENLINK BROMLEY')
##################

openai_api_key=st.secrets["openai"]
client = OpenAI(api_key=openai_api_key)



state=st.session_state
picture = st.camera_input("Take a picture")




st.subheader('Press START to speak, press END when finish ')
st.write('You can speak about a PROBLEM such as flytipping, or an IDEA such as a place for installing solar pannels.')
text=WhisperSTT(openai_api_key=openai_api_key,language='en', start_prompt='🔴 START', stop_prompt='✋ END') # If you don't pass an API key, the function will attempt to load a .env file in the current directory and retrieve it as an environment variable : 'OPENAI_API_KEY'.
if text:
    st.write(text)
    response = client.chat.completions.create(

  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": """
     You are an AI-based data reporting system tailored for the citizens of Bromley. Your primary function is to process and categorize inputs received from users. These inputs will be in the form of text transcriptions, derived from user speech, accompanying photos taken by the users. Each submission will either highlight a problem in the photographed area or propose an innovative idea related to the location in the photo. For instance, a user might report 'extensive fly tipping in the alley behind Oak Street' or suggest 'installing community solar panels on the flat roofs of the High Street buildings.'

Your task involves two critical steps:

Classification: Determine if the submission is reporting a 'Problem' or suggesting an 'Idea.'
Categorization and Description: Assign a relevant category to the submission (like 'Environmental Issues,' 'Urban Development,' 'Community Projects,' etc.) and provide a concise description of the issue or idea.
This information is essential as it will be forwarded to the local council for civic action and data reporting, akin to platforms like FixMyStreet. It could also be utilized by local volunteer groups and community organizations for planning workshops, advocacy initiatives, or other community activities. The data you process will play a significant role in directing attention and resources to pertinent local issues and innovative ideas.

Your output should be formatted as follows:
Problem/Idea | Category | Description

For example:

Problem | Environmental Issues | Extensive fly tipping in the alley behind Oak Street.
Idea | Community Energy Projects | Installing community solar panels on the flat roofs of High Street buildings.
     """
     },
    {"role": "user", "content": f"{text}"},
  ]
)

    st.write("_________________________")
    st.subheader('Your report:')

    c1, c2 = st.columns(2)
    with c1:
        if picture:
            st.image(picture)

    with c2:
        problem, category, content = response.choices[0].message.content.split('|')
        st.write('Problem or Idea: ', problem)
        st.write('Category: ', category)
        st.write('Content: ', content)
        st.write('This has been reported to the council!')
