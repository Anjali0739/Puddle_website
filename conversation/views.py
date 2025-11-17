from django.shortcuts import render, get_object_or_404, redirect
from .forms import ConversationMessageForm
from item.models import Item
from .models import Conversation
# Create your views here.
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:
        # Prevent users from starting conversations with themselves
        return render(request, "dashboard/index.html")
    
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        pass

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = None

            if conversations:
                conversation = conversations[0]
            else:
                conversation = Conversation.objects.create(item=item)
                conversation.members.add(request.user)
                conversation.members.add(item.created_by)
                conversation.save()
            
            message = form.save(commit=False)
            message.conversation = conversation
            message.created_by = request.user
            message.save()

            return redirect('item:detail', pk=item.pk)
        
    else:
        form = ConversationMessageForm()
    
    return render(request, 'conversation/new.html', {
        'form': form,})