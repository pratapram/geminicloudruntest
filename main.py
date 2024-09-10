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


from flask import Flask, render_template, jsonify
app = Flask(__name__)

import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting, FinishReason
import vertexai.generative_models as generative_models
from vertexai.preview.prompts import Prompt


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


def generate():
  vertexai.init(project="yourprojectname", location="us-central1")
  variables = [
    {
    },
  ]
  prompt = Prompt(
    prompt_data=["""What is the capital of New york state?"""],
    model_name="gemini-1.5-flash-001",
    variables=variables,
    generation_config=generation_config,
    safety_settings=safety_settings,
  )
  # Generate content using the assembled prompt. Change the index if you want
  # to use a different set in the variable value list.
  response = prompt.generate_content(
      contents=prompt.assemble_contents(**prompt.variables[0]),
      stream=False,
  )
  #print (response.text)
  #dir(response)
  return (response.text)

#generate()



@app.route('/')
def index():
    text = generate()

    return text


if __name__ == "__main__":
    app.run(debug=True)

