from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChatHistory, KnowledgeBase
from .forms import ChatHistoryForm
from .utils import get_gemini_response, convert_markdown_to_html

# @login_required  # Ensure the user is logged in
# def chatbot_view(request):
#     if request.method == 'POST':
#         form = ChatHistoryForm(request.POST)
#         if form.is_valid():
#             user_message = form.cleaned_data['user_message']
#             bot_response = convert_markdown_to_html(get_gemini_response(user_message))
            
#             # Save the chat history
#             chat_history = form.save(commit=False)
#             chat_history.user = request.user  # Associate the current user with the chat
#             chat_history.bot_response = bot_response
#             chat_history.save()

#             return render(request, 'chatbot/chat.html', {
#                 'form': form,
#                 'bot_response': bot_response,
#                 'user_message': user_message,
#                 'chat_history': ChatHistory.objects.filter(user=request.user).order_by('-timestamp')
#             })
#     else:
#         form = ChatHistoryForm()

#     # Display the form and the conversation history
#     return render(request, 'chatbot/chat.html', {
#         'form': form,
#         'chat_history': ChatHistory.objects.filter(user=request.user).order_by('-timestamp')
#     })

@login_required  # Ensure the user is logged in
def chatbot_view(request):
    if request.method == 'POST':
        form = ChatHistoryForm(request.POST)
        if form.is_valid():
            user_message = form.cleaned_data['user_message']
            
            
            # Check if the query is in the knowledge base
            kb_entry = KnowledgeBase.objects.filter(query=user_message).first()
            
            if kb_entry:
                bot_response = kb_entry.response
            else:
                # If not found, call the Gemini API
                bot_response = convert_markdown_to_html(get_gemini_response(user_message))
            
            # Save the new query and response to the knowledge base
            existing_entry = KnowledgeBase.objects.filter(query__iexact=user_message).first()
            if not existing_entry:
                KnowledgeBase.objects.create(query=user_message, response=bot_response)

         # Save the chat history
            chat_history = form.save(commit=False)
            chat_history.user = request.user  # Associate the current user with the chat
            chat_history.bot_response = bot_response
            chat_history.save()

            return render(request, 'chatbot/chat.html', {
                'form': form,
                'bot_response': bot_response,
                'user_message': user_message,
                'chat_history': ChatHistory.objects.filter(user=request.user).order_by('-timestamp')
            })
    else:
        form = ChatHistoryForm()

    # Display the form and the conversation history
    return render(request, 'chatbot/chat.html', {
        'form': form,
        'chat_history': ChatHistory.objects.filter(user=request.user).order_by('-timestamp')
    })