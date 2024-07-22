import streamlit as st
from openai import OpenAI

#Connect Model LLM
@st.cache_resource
def Connect_Model():
	return OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
client = Connect_Model()

# Store LLM generated responses
if "messages" not in st.session_state.keys():
	st.session_state.messages = [
		{"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."}
	]

# Display chat messages
def Display():
	for message in st.session_state.messages:
		if message["role"] != "system":
			with st.chat_message(message["role"]):
				st.write(message["content"])
Display()

# Function for generating LLM response
def Generate_llm_response():
	response = client.chat.completions.create(
		model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
		messages=st.session_state.messages,
		temperature=0.7,
		stream=True,

	)

	return response

# if st.session_state.messages[-1]["role"] == "user":
# 	message = {"role": "assistant", "content": ""}
# 	response = Generate_llm_response()
	
# 	with st.chat_message("assistant"):
# 		st.write(response)

prompt = st.chat_input("?")
if prompt:
	with st.chat_message("user"):
		st.write(prompt)
	message = {"role": "user", "content": prompt}
	st.session_state.messages.append(message)

	response = Generate_llm_response()
	with st.chat_message("assistant"):
		st.write(response)

	message = {"role": "assistant", "content": ""}
	for chunk in response:
		if chunk.choices[0].delta.content:
			message["content"] += chunk.choices[0].delta.content
	st.session_state.messages.append(message)
			

st.write(st.session_state.messages)