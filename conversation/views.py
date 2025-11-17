from django.shortcuts import render, get_object_or_404, redirect
from .forms import ConversationMessageForm
from item.models import Item
from .models import Conversation
# Create your views here.



def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    conversations = Conversation.objects.filter(item=item)

    # If logged in user already has conversation reused
    if request.user.is_authenticated:
        user_convo = conversations.filter(members=request.user)
        if user_convo.exists():
            return redirect('conversation:detail', pk=user_convo.first().pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            # Create or get conversation
            conversation = conversations.first()
            if not conversation:
                conversation = Conversation.objects.create(item=item)

                # Add only item owner
                conversation.members.add(item.created_by)

                # Add logged-in user, NOT anonymous users
                if request.user.is_authenticated:
                    conversation.members.add(request.user)

            # Save message
            message = form.save(commit=False)
            message.conversation = conversation

            # Assign user or anonymous name
            if request.user.is_authenticated:
                message.created_by = request.user
                message.anonymous_name = ""
            else:
                message.created_by = None
                message.anonymous_name = "Anonymous"

            message.save()
            return redirect('item:detail', pk=conversation.pk)

    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/new.html', {
        'form': form,
        'item': item,
    })