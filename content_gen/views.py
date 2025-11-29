from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from huggingface_hub import InferenceClient

@csrf_exempt
def generate_content(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            topic = data.get('topic', '')
            
            if not topic:
                return JsonResponse({'error': 'Topic is required'}, status=400)
            
            explanation = generate_explanation(topic)
            summary = generate_summary(topic)
            key_concepts = generate_key_concepts(topic)
            practice_questions = generate_practice_questions(topic)
            interview_qa = generate_interview_qa(topic)
            
            content = {
                'explanation': explanation,
                'summary': summary,
                'key_concepts': key_concepts,
                'practice_questions': practice_questions,
                'interview_qa': interview_qa
            }
            
            return JsonResponse(content)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def call_huggingface_inference(prompt, max_tokens=800):
    # REPLACE WITH YOUR HUGGING FACE TOKEN
    api_token = "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"
    
    if api_token == "YOUR_HUGGINGFACE_TOKEN_HERE":
        error_msg = "ERROR: Please add your Hugging Face token in views.py"
        return error_msg
    
    try:
        # Initialize InferenceClient with your token
        client = InferenceClient(token=api_token)
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        # Try different free models available
        models = [
            "Qwen/Qwen2.5-72B-Instruct",
            "meta-llama/Llama-3.2-3B-Instruct",
            "microsoft/Phi-3.5-mini-instruct"
        ]
        
        for model in models:
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=max_tokens
                )
                
                text = response.choices[0].message.content.strip()
                return text
                
            except Exception as e:
                continue
        
        # If all models fail, return error
        return "Unable to generate content. Please check your API token or try again later."
        
    except Exception as e:
        error_msg = f"API Error: {str(e)}"
        return error_msg


def generate_explanation(topic):
    prompt = f"""Provide a clear and comprehensive explanation of {topic}.
        Include:
            - What it is
            - Why it's important  
            - How it works
            - Real-world applications
        Write 2-3 paragraphs."""
    
    return call_huggingface_inference(prompt, max_tokens=1000)


def generate_summary(topic):
    prompt = f"Write a concise 3-sentence summary of {topic}."
    return call_huggingface_inference(prompt, max_tokens=300)


def generate_key_concepts(topic):
    prompt = f"""List 5 key concepts about {topic}.

Format as JSON array:
[
  {{"concept": "Concept Name", "description": "Brief description"}},
  {{"concept": "Concept Name", "description": "Brief description"}}
]

Return ONLY the JSON array, nothing else."""
    
    response = call_huggingface_inference(prompt, max_tokens=800)
    
    # Try to parse JSON
    try:
        # Look for JSON array in response
        start = response.find('[')
        end = response.rfind(']') + 1
        if start != -1 and end > start:
            json_str = response[start:end]
            parsed = json.loads(json_str)
            return parsed[:5]
    except Exception as e:
        print(f"   ⚠ JSON parsing failed: {e}")
    # Fallback
    print("   → Using fallback concepts")
    return [
        {"concept": f"{topic} Fundamentals", "description": "Core principles and basic understanding"},
        {"concept": "Key Components", "description": "Main elements and structure"},
        {"concept": "Applications", "description": "Practical uses and real-world examples"},
        {"concept": "Benefits", "description": "Advantages and importance"},
        {"concept": "Best Practices", "description": "Recommended approaches"}
    ]


def generate_practice_questions(topic):
    prompt = f"""Create 5 practice questions about {topic} with answers.

Format as JSON array:
[
  {{"question": "Question text?", "answer": "Answer text"}},
  {{"question": "Question text?", "answer": "Answer text"}}
]

Return ONLY the JSON array, nothing else."""
    
    response = call_huggingface_inference(prompt, max_tokens=1000)
    
    # Try to parse JSON
    try:
        start = response.find('[')
        end = response.rfind(']') + 1
        if start != -1 and end > start:
            json_str = response[start:end]
            parsed = json.loads(json_str)
            print(f"   ✓ Parsed {len(parsed)} questions")
            return parsed[:5]  # Limit to 5
    except Exception as e:
        print(f"JSON parsing failed: {e}")
    
    # Fallback
    print("   → Using fallback questions")
    return [
        {"question": f"What is {topic}?", "answer": f"{topic} is a concept involving key principles and applications."},
        {"question": f"Why is {topic} important?", "answer": "It's important because it provides valuable insights."},
        {"question": f"How does {topic} work?", "answer": "It works through various processes and mechanisms."},
        {"question": "What are the main benefits?", "answer": "Benefits include improved understanding and practical applications."},
        {"question": "What should beginners know?", "answer": "Start with fundamentals and build knowledge gradually."}
    ]


def generate_interview_qa(topic):
    prompt = f"""Create 5 interview questions about {topic} with professional answers.

Format as JSON array:
[
  {{"question": "Interview question?", "answer": "Professional answer"}},
  {{"question": "Interview question?", "answer": "Professional answer"}}
]

Return ONLY the JSON array, nothing else."""
    
    response = call_huggingface_inference(prompt, max_tokens=1000)
    
    # Try to parse JSON
    try:
        start = response.find('[')
        end = response.rfind(']') + 1
        if start != -1 and end > start:
            json_str = response[start:end]
            parsed = json.loads(json_str)
            print(f"   ✓ Parsed {len(parsed)} interview questions")
            return parsed[:5]  
    except Exception as e:
        print(f"   ⚠ JSON parsing failed: {e}")
    
    # Fallback
    print("   → Using fallback interview questions")
    return [
        {"question": f"Can you explain {topic}?", "answer": f"{topic} is an important concept with various applications."},
        {"question": f"What experience do you have with {topic}?", "answer": "I have practical experience applying these principles."},
        {"question": f"How would you implement {topic}?", "answer": "I would analyze requirements and design an appropriate solution."},
        {"question": "What challenges might arise?", "answer": "Common challenges include complexity and integration issues."},
        {"question": "What's the future of this field?", "answer": "The field is evolving with new innovations emerging."}
    ]


def index(request):
    """Render the main page"""
    return render(request, 'index.html')