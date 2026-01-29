from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Message

@login_required
def inbox_view(request):
    """
    Finds all unique users the current user has messaged with.
    """
    user = request.user
    
    # Get all messages where the user is sender OR receiver
    messages = Message.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).order_by('-created_at')

    # Filter for unique conversation partners
    conversations = []
    seen_users = set()

    for msg in messages:
        # Determine who the "other" person is
        if msg.sender == user:
            partner = msg.receiver
        else:
            partner = msg.sender
            
        if partner not in seen_users:
            conversations.append({
                'partner': partner,
                'last_message': msg
            })
            seen_users.add(partner)

    return render(request, 'inbox.html', {'conversations': conversations})

@login_required
def chat_view(request, user_id):
    """
    Shows chat history with a specific user and allows sending messages.
    """
    other_user = get_object_or_404(User, id=user_id)
    current_user = request.user

    # Handle Sending a Message
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Message.objects.create(
                sender=current_user,
                receiver=other_user,
                content=content
            )
            return redirect('chat_view', user_id=user_id)

    # Fetch conversation history
    messages = Message.objects.filter(
        Q(sender=current_user, receiver=other_user) | 
        Q(sender=other_user, receiver=current_user)
    ).order_by('created_at')

    context = {
        'other_user': other_user,
        'messages': messages
    }
    return render(request, 'chat.html', context)