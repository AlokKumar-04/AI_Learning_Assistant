from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from huggingface_hub import InferenceClient
import os
from decouple import config
import logging
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

# Set up logging
logger = logging.getLogger(__name__)

@csrf_exempt
def generate_content(request):
    if request.method == 'POST':
        try:
            logger.info("=" * 50)
            logger.info("REQUEST RECEIVED")
            logger.info("=" * 50)
            
            data = json.loads(request.body)
            topic = data.get('topic', '').strip()
            
            if not topic:
                return JsonResponse({'error': 'Please enter a topic'}, status=400)
            
            if len(topic) > 200:
                return JsonResponse({
                    'error': 'Topic too long. Keep it under 200 characters.'
                }, status=400)
            
            logger.info(f"Topic: {topic}")
            start_time = time.time()
            
            # OPTIMIZATION: Generate all content in parallel with timeout
            with ThreadPoolExecutor(max_workers=5) as executor:
                # Submit all tasks at once
                future_explanation = executor.submit(generate_explanation, topic)
                future_summary = executor.submit(generate_summary, topic)
                future_concepts = executor.submit(generate_key_concepts, topic)
                future_questions = executor.submit(generate_practice_questions, topic)
                future_interview = executor.submit(generate_interview_qa, topic)
                
                # Get results with timeout (45 seconds max)
                try:
                    explanation = future_explanation.result(timeout=45)
                except Exception as e:
                    logger.error(f"Explanation timeout/error: {str(e)}")
                    explanation = f"Content generation timed out. Please try a simpler topic."
                
                try:
                    summary = future_summary.result(timeout=45)
                except Exception as e:
                    logger.error(f"Summary timeout/error: {str(e)}")
                    summary = "Unable to generate summary."
                
                try:
                    key_concepts = future_concepts.result(timeout=45)
                except Exception as e:
                    logger.error(f"Concepts timeout/error: {str(e)}")
                    key_concepts = get_fallback_concepts(topic)
                
                try:
                    practice_questions = future_questions.result(timeout=45)
                except Exception as e:
                    logger.error(f"Questions timeout/error: {str(e)}")
                    practice_questions = get_fallback_questions(topic)
                
                try:
                    interview_qa = future_interview.result(timeout=45)
                except Exception as e:
                    logger.error(f"Interview timeout/error: {str(e)}")
                    interview_qa = get_fallback_interview(topic)
            
            elapsed_time = time.time() - start_time
            logger.info(f"✓ ALL CONTENT GENERATED in {elapsed_time:.2f}s")
            logger.info("=" * 50)
            
            content = {
                'explanation': explanation,
                'summary': summary,
                'key_concepts': key_concepts,
                'practice_questions': practice_questions,
                'interview_qa': interview_qa
            }
            
            return JsonResponse(content)
            
        except Exception as e:
            logger.error(f"Critical error: {str(e)}", exc_info=True)
            return JsonResponse({
                'error': 'An error occurred. Please try again.'
            }, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def call_huggingface_inference(prompt, max_tokens=500, timeout=30):
    """
    Optimized API call with reduced tokens
    Note: timeout parameter is for ThreadPoolExecutor, not API call
    """
    
    api_token = config('HUGGINGFACE_TOKEN', default=None)
    
    if not api_token:
        logger.error("API token not configured")
        return "API configuration error."
    
    try:
        logger.info("→ Calling Hugging Face API...")
        
        client = InferenceClient(token=api_token)
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        # Use only fastest models for speed
        models = [
            "Qwen/Qwen2.5-72B-Instruct",
            "microsoft/Phi-3.5-mini-instruct"
        ]
        
        for model in models:
            try:
                logger.info(f"→ Trying {model}")
                start = time.time()
                
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=max_tokens
                )
                
                elapsed = time.time() - start
                
                if response and response.choices:
                    text = response.choices[0].message.content.strip()
                    if text and len(text) > 10:
                        logger.info(f"✓ Success in {elapsed:.2f}s ({len(text)} chars)")
                        return text
                        
            except Exception as e:
                error_msg = str(e).lower()
                logger.warning(f"Failed with {model}: {str(e)}")
                
                # Don't retry on certain errors
                if "unauthorized" in error_msg or "invalid" in error_msg:
                    return "API authentication error."
                
                continue
        
        return "Unable to generate content. Please try again."
        
    except Exception as e:
        logger.error(f"API error: {str(e)}")
        return "Service temporarily unavailable."


def generate_explanation(topic):
    """Generate concise explanation (OPTIMIZED)"""
    prompt = f"Explain {topic} clearly in 2-3 paragraphs. Cover: what it is, why it matters, and key applications."
    return call_huggingface_inference(prompt, max_tokens=500, timeout=25)


def generate_summary(topic):
    """Generate summary"""
    prompt = f"Write a 2-sentence summary of {topic}."
    return call_huggingface_inference(prompt, max_tokens=150, timeout=20)


def generate_key_concepts(topic):
    """Generate key concepts (OPTIMIZED)"""
    prompt = f"""List 5 key concepts about {topic}.

Return as JSON array:
[
  {{"concept": "First Concept", "description": "Brief explanation of this concept"}},
  {{"concept": "Second Concept", "description": "Brief explanation of this concept"}}
]

IMPORTANT: Return ONLY the JSON array, no other text."""
    
    response = call_huggingface_inference(prompt, max_tokens=500, timeout=25)
    
    logger.info(f"Concepts raw response: {response[:200]}")  # Debug log
    
    try:
        start = response.find('[')
        end = response.rfind(']') + 1
        if start != -1 and end > start:
            json_str = response[start:end]
            logger.info(f"Extracted JSON: {json_str[:100]}")  # Debug log
            
            parsed = json.loads(json_str)
            if isinstance(parsed, list) and len(parsed) > 0:
                logger.info(f"✓ Parsed {len(parsed)} concepts")
                return parsed[:5]
        
        logger.warning("Could not find valid JSON in response")
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
    except Exception as e:
        logger.error(f"Parse error: {str(e)}")
    
    logger.info("Using fallback concepts")
    return get_fallback_concepts(topic)


def generate_practice_questions(topic):
    """Generate practice questions (OPTIMIZED)"""
    prompt = f"""Create 5 practice questions about {topic}.

Return as JSON array:
[
  {{"question": "What is the main concept?", "answer": "Brief answer here"}},
  {{"question": "How does it work?", "answer": "Brief answer here"}}
]

IMPORTANT: Return ONLY the JSON array, no other text."""
    
    response = call_huggingface_inference(prompt, max_tokens=600, timeout=25)
    
    logger.info(f"Practice Q raw response: {response[:200]}")  # Debug log
    
    try:
        # Try to find and extract JSON array
        start = response.find('[')
        end = response.rfind(']') + 1
        
        if start != -1 and end > start:
            json_str = response[start:end]
            logger.info(f"Extracted JSON: {json_str[:100]}")  # Debug log
            
            parsed = json.loads(json_str)
            
            if isinstance(parsed, list) and len(parsed) > 0:
                logger.info(f"✓ Parsed {len(parsed)} questions")
                return parsed[:5]
        
        logger.warning("Could not find valid JSON in response")
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
    except Exception as e:
        logger.error(f"Parse error: {str(e)}")
    
    logger.info("Using fallback questions")
    return get_fallback_questions(topic)


def generate_interview_qa(topic):
    """Generate interview Q&A (OPTIMIZED)"""
    prompt = f"""Create 5 interview questions about {topic}.

Return as JSON array:
[
  {{"question": "Can you explain this concept?", "answer": "Professional answer here"}},
  {{"question": "What's your experience?", "answer": "Professional answer here"}}
]

IMPORTANT: Return ONLY the JSON array, no other text."""
    
    response = call_huggingface_inference(prompt, max_tokens=600, timeout=25)
    
    logger.info(f"Interview Q raw response: {response[:200]}")  # Debug log
    
    try:
        # Try to find and extract JSON array
        start = response.find('[')
        end = response.rfind(']') + 1
        
        if start != -1 and end > start:
            json_str = response[start:end]
            logger.info(f"Extracted JSON: {json_str[:100]}")  # Debug log
            
            parsed = json.loads(json_str)
            
            if isinstance(parsed, list) and len(parsed) > 0:
                logger.info(f"✓ Parsed {len(parsed)} interview questions")
                return parsed[:5]
        
        logger.warning("Could not find valid JSON in response")
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
    except Exception as e:
        logger.error(f"Parse error: {str(e)}")
    
    logger.info("Using fallback interview questions")
    return get_fallback_interview(topic)


# Fallback functions
def get_fallback_concepts(topic):
    return [
        {"concept": f"{topic} Basics", "description": "Fundamental understanding"},
        {"concept": "Key Principles", "description": "Core concepts and ideas"},
        {"concept": "Applications", "description": "Real-world uses"},
        {"concept": "Benefits", "description": "Advantages and importance"},
        {"concept": "Best Practices", "description": "Recommended approaches"}
    ]


def get_fallback_questions(topic):
    return [
        {"question": f"What is {topic}?", "answer": f"{topic} is an important concept."},
        {"question": f"Why is {topic} important?", "answer": "It provides valuable insights."},
        {"question": f"How does {topic} work?", "answer": "Through various mechanisms."},
        {"question": "What are the benefits?", "answer": "Multiple practical benefits."},
        {"question": "What should I know?", "answer": "Start with fundamentals."}
    ]


def get_fallback_interview(topic):
    return [
        {"question": f"Explain {topic}", "answer": f"{topic} is a key concept."},
        {"question": f"Your experience with {topic}?", "answer": "Practical experience."},
        {"question": "How would you use it?", "answer": "By applying principles."},
        {"question": "What challenges exist?", "answer": "Various challenges."},
        {"question": "Future of this field?", "answer": "Rapidly evolving."}
    ]


def index(request):
    """Render the main page"""
    return render(request, 'index.html')