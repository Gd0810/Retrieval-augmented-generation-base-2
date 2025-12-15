from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from .models import KnowledgeBase
from .services import get_ai_response

def get_relevant_data(user_question):
    words = [word.lower() for word in user_question.split() if len(word) > 1]
    query = Q()
    for word in words:
        query |= Q(content__icontains=word)
    results = KnowledgeBase.objects.filter(query)[:5]
    question_words = set(words)
    ranked_results = []
    for entry in results:
        content_words = set(entry.content.lower().split())
        match_count = len(question_words.intersection(content_words))
        if match_count > 0:
            ranked_results.append((entry, match_count))
    ranked_results.sort(key=lambda x: x[1], reverse=True)
    top_results = [entry for entry, _ in ranked_results[:1]]  # Top 1 only
    retrieved = "\n".join([entry.content for entry in top_results]) or "No relevant data found."
    print("Retrieved Data:", retrieved)
    return retrieved

def chatbot_view(request):
    if request.method == "GET":
        user_question = request.GET.get("question")
        if not user_question:
            return JsonResponse({"error": "No question provided"}, status=400)
        
        # Define common greetings and their responses
        greetings = {
    "hi": "Hello! How can I assist you today?",
    "hello": "Hi there! What's on your mind?",
    "hey": "Hey! Nice to hear from you! What’s up?",
    "howdy": "Howdy! Ready to help—what’s on your plate?",
    "greetings": "Greetings! How can I make your day even better?",
    "yo": "Yo! What's good?",
    "hiya": "Hiya! Great to see you—how can I help?",
    "how are you": "I'm doing great, thanks for asking! How about you?",
    "how's it going": "All good here! How’s it going with you?",
    "how's today": "Today’s going well, thanks! How can I help you?",
    "how you doing": "Doing awesome, thanks! What's up with you?",
    "what's up": "Not much, just here to help! What's up with you?",
    "what's good": "All good here! What’s good with you?",
    "good morning": "Good morning! Hope your day’s off to a great start!",
    "good afternoon": "Good afternoon! How’s your day going so far?",
    "good evening": "Good evening! Ready to dive into something fun?",
    "good day": "Good day to you too! What’s on your mind?",
    "how's your day": "My day’s great, thanks for asking! How’s yours?",
    "how's everything": "Everything’s awesome here! How’s it with you?",
    "what's new": "Nothing new with me, but I’m curious—what’s new with you?",
    "how's it hanging": "Hanging in there! How about you?",
    "sup": "Sup! What’s cooking?",
    "how's life": "Life’s good in the digital world! How’s yours?",
    "hi there": "Hey there! What can I do for you today?",
    "hello there": "Hello! Nice to hear from you—what’s up?",
    "hey you": "Hey you! What’s the vibe today?",
    "how are things": "Things are great here! How are they with you?",
    "what’s happening": "Not much, just chilling! What’s happening with you?",
    "how’s your mood": "My mood’s as bright as ever! How’s yours?",
    "hope you’re well": "Thanks, I’m doing great! Hope you’re well too!",
    "nice to see you": "Nice to see you too! What’s on your mind?"
}
        
        # Check if the user input is a greeting
        user_question_lower = user_question.lower().strip()
        for greeting, response in greetings.items():
            if user_question_lower.startswith(greeting):
                return JsonResponse({"answer": response})
        
        # Proceed with RAG for user data-related questions
        retrieved_data = get_relevant_data(user_question)
        answer = get_ai_response(user_question, retrieved_data)
        return JsonResponse({"answer": answer or "No answer generated."})  # Fallback for empty responses

def chat_page_view(request):
    return render(request, 'chat.html')