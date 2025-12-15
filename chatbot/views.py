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