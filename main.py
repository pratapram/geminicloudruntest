# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import chainlit as cl
import base64
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting, Part
import asyncio

vertexai.init(project="yourprojectname", location="us-central1")
model = GenerativeModel(
    "gemini-1.5-flash-001",
    system_instruction=["""you are a nyc expert"""]
    )

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
]

@cl.on_message
async def main(msg: cl.Message):
    print("The user sent: ", msg.content)

    response = cl.Message(content = "")


    stream = await model.generate_content_async(
          [msg.content],
          generation_config=generation_config,
          safety_settings=safety_settings,
          stream = True
    )
    #print (stream)
    async for chunk in stream:
        #print (chunk)
        if 'candidates' in chunk.to_dict().keys():
            if 'content' in chunk.candidates[0].to_dict().keys():
                token = chunk.text
                await response.stream_token(token)
    await response.update()


 

# if __name__ == "__main__":
#     from chainlit.cli import run_chainlit
#     run_chainlit(__file__)

