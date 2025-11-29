from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
# Create your views here.

def index(request):
    return render(request, 'index.html')


def call_huggingface_api(prompt, max_retries=2):
    models = [
        "mistralai/Mistral-7B-Instruct-v0.2",  
        "microsoft/Phi-3-mini-4k-instruct",    
        "meta-llama/Meta-Llama-3-8B-Instruct",  
    ]
    
    # Get your FREE API token from: https://huggingface.co/settings/tokens
    api_token = "YOUR_HUGGINGFACE_TOKEN_HERE"  # Replace with your token
    
    for model in models:
        try:
            url = f"https://api-inference.huggingface.co/models/{model}"
            headers = {
                "Authorization": f"Bearer {api_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 1000,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "return_full_text": False
                }
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', '').strip()
                elif isinstance(result, dict):
                    return result.get('generated_text', '').strip()
            continue
            
        except Exception as e:
            print(f"Error with model {model}: {str(e)}")
            continue
    
    return f"Unable to generate content at the moment. Please try again later."



def parse_concepts_from_text(request):
    pass


def parse_qa_from_text(request):
    pass


def generate_explanation(topic):

    prompt = f'''Provide a comprehensive explanation of {topic}
    Include:
        - What it is
        - Why it's important
        - How it works
        - Real-world applications
    Keep it clear and educational.'''
    return call_huggingface_api(prompt)


def generate_summary(topic):
    prompt = f'''Provide a concise summary of {topic} in 3-4 sentences. 
    Focus on the most important points that someone should know.'''
    return call_huggingface_api


def generate_key_concepts(topic):
    prompt = f'''List 5-7 key concepts related to {topic}.
    For each concept, provide the name and a brief description.
    Format your response EXACTLY as a JSON array like this:
    [
        {{"concept": "Concept Name 1", "description": "Brief description here"}},
        {{"concept": "Concept Name 2", "description": "Brief description here"}}
    ]
    Return ONLY the JSON array, no other text.'''
    response = call_huggingface_api(prompt)
    try:
        # Try to extract JSON from response
        start = response.find('[')
        end = response.rfind(']') + 1
        if start != -1 and end > start:
            json_str = response[start:end]
            return json.loads(json_str)
        else:
            # Fallback parsing
            return parse_concepts_from_text(response, topic)
    except:
        return parse_concepts_from_text(response, topic)


def generate_practice_questions(topic):
    prompt = f"""Create 5 practice questions about {topic} with answers.
    Include a mix of difficulty levels.
    Format your response EXACTLY as a JSON array like this:
    [
        {{"question": "What is...", "answer": "The answer is..."}},
        {{"question": "How does...", "answer": "It works by..."}}
    ]
    Return ONLY the JSON array, no other text."""
    
    response = call_huggingface_api(prompt)
    try:
        start = response.find('[')
        end = response.rfind(']') + 1
        if start != -1 and end > start:
            json_str = response[start:end]
            return json.loads(json_str)
        else:
            return parse_qa_from_text(response)
    except:
        return parse_qa_from_text(response)


def generate_interview_qa(topic):
    prompt = f"""Create 5 common interview questions about {topic} with detailed professional answers.
    Make them realistic interview-style questions.
    Format your response EXACTLY as a JSON array like this:
    [
        {{"question": "Can you explain...", "answer": "A professional answer would be..."}},
        {{"question": "What are the benefits of...", "answer": "The main benefits include..."}}
    ]
    Return ONLY the JSON array, no other text."""
    
    response = call_huggingface_api(prompt)
    try:
        start = response.find('[')
        end = response.rfind(']') + 1
        if start != -1 and end > start:
            json_str = response[start:end]
            return json.loads(json_str)
        else:
            return parse_qa_from_text(response)
    except:
        return parse_qa_from_text(response)


@csrf_exempt
def generate_content(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            topic = data.get('topic', '')

            if not topic:
                return JsonResponse({'error':'Topic is required'}, status=400)
            
            content = {
                'explanation': generate_explanation(topic),
                'summary': generate_explanation(topic),
                'key_concepts': generate_key_concepts(topic),
                'practice_questions': generate_practice_questions(topic),
                'interview_qa': generate_interview_qa
            }
            return JsonResponse(content)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
    return JsonResponse({'error': 'Invalid request method'}, status=405)