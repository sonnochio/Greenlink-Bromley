from streamlit_mic_recorder import mic_recorder,speech_to_text
from whisper import WhisperSTT
from openai import OpenAI
import streamlit as st
from streamlit_js_eval import get_geolocation
from storage import upload_image, create_data_point,initialize_firebase, create_feedback
import datetime

initialize_firebase()

st.write("Please sync location and allow the app to access your current location!")
if st.checkbox("Sync location"):
    try:
        loc = get_geolocation()
        lat=loc['coords']['latitude']
        lon=loc['coords']['longitude']
        data={"lat": {
            "0": lat,
        },
        "lon": {
            "0": lon,
        },}
    except:
        st.write('Loading...')

st.title('GREENLINK BROMLEY')
##################

openai_api_key=st.secrets["openai"]




client = OpenAI(api_key=openai_api_key)



state=st.session_state
picture = st.camera_input("Take a picture")
now = datetime.datetime.now()



s1, s2 = st.columns(2)
with s1:
    st.subheader('Press START to speak, press END when finish. Wait for your report to generate. ')
with s2:
    st.write('You can speak about a PROBLEM such as flytipping, or an IDEA such as a place for installing solar pannels. Try to keep it short.')
    st.write('If you need help with sighting, switch on below')
    sighting_req = st.toggle('Sighting guide')
if sighting_req:
    st.write("""

Aim to cover these areas when reporting a sighting of an endangeroued speicies.
- Species identification
- Quantity observed
- Behavior observed
- Habitat type
- Weather conditions
- Life stage (e.g., adult, juvenile, larva)
- Physical condition (e.g., healthy, injured)
- Sex (if determinable)
- Presence of young
- Flowering condition (for plants)
- Interaction with other species""")
text=WhisperSTT(openai_api_key=openai_api_key,language='en', start_prompt='🔴 START', stop_prompt='✋ END') # If you don't pass an API key, the function will attempt to load a .env file in the current directory and retrieve it as an environment variable : 'OPENAI_API_KEY'.
if text:
    st.write('Your transcription:')
    st.write(text)
    response = client.chat.completions.create(

  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": """
You are an AI-based data reporting system tailored for the citizens of Bromley. Your primary function is to process and categorize inputs received from users. These inputs will be in the form of text transcriptions, derived from user speech, accompanying photos taken by the users. Each submission will either highlight a problem in the photographed area or propose an innovative idea related to the location in the photo or report an endangered species found in the uk. For instance, a user might report 'extensive fly tipping in the alley behind Oak Street' or suggest 'installing community solar panels on the flat roofs of the High Street buildings or report a sighting of the endangered species ‘Crawfish’

Your task involves two critical steps:

Classification: Determine if the submission is reporting a 'Problem' or suggesting an 'Idea’, or ‘sighting’
Categorization and Description: Assign a relevant category to the submission (like 'Environmental Issues,' 'Urban Development,' 'Community Projects,' etc.) and provide a concise description of the issue or idea.
This information is essential as it will be forwarded to the local council for civic action and data reporting, akin to platforms like FixMyStreet. It could also be utilized by local volunteer groups and community organizations for planning workshops, advocacy initiatives, or other community activities. The data you process will play a significant role in directing attention and resources to pertinent local issues and innovative ideas.

Your output should be formatted as follows:
Problem/Idea/sighting | Category | Description

For example:

Problem | Environmental Issues | Extensive fly tipping in the alley behind Oak Street.
Idea | Community Energy Projects | Installing community solar panels on the flat roofs of High Street buildings.
Problem | Environmental Issues | Extensive fly tipping in the alley behind Oak Street.
Sighting | Endangered Species | Spotted one of the endangered species , ‘Crawfish’.
     """
     },
    {"role": "user", "content": f"{text}"},
  ]
)

    st.write("_________________________")
    st.subheader('Your report:')
    try:
        st.map(data=data)
    except:
        st.write()
    c1, c2 = st.columns(2)
    with c1:
        if picture:
            st.image(picture)
            image_url=upload_image(picture, f'upload/{now}.jpg')

    with c2:
        try:
     
        
            problem, category, content = response.choices[0].message.content.split('|')
            st.write(now)
            st.write('Type: ', problem)
            st.write('Category: ', category)
            st.write('Content: ', content)
            create_data_point(image_url=image_url, geolocation=data, summarization=content, raw=text, type=problem, category=category ,time=now)

            st.write("✅Your report has been documented")
        except:
            st.write("An error has occured, Please try again")


st.write('If you have any feedback during test, please press the feedback button below and speak.')
feedback=WhisperSTT(openai_api_key=openai_api_key,language='en', start_prompt='🔴 START FEEDBACK', stop_prompt='✋ END FEEDBACK')
if feedback:
    create_feedback(feedback=feedback)
    st.write("Feedback collected. Thank you so much")