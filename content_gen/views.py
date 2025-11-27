from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def index(request):
    return render(request, 'index.html')



def call_hugging_face_api(prompt):
    return 


def generate_explanation(topic):

    prompt = f'''Provide a comprehensive explanation of {topic}
    Include:
        - What it is
        - Why it's important
        - How it works
        - Real-world applications
    Keep it clear and educational.'''
    return call_hugging_face_api(prompt)


def generate_summary(topic):
    return


def generate_key_concepts(topic):
    return


def generate_practice_questions(topic):
    return


def generate_interview_qa(topic):
    return


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