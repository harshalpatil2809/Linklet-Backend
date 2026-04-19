from .models import Follow

def check_mutual_follow(user1, user2):
    forward_follow = Follow.objects.filter(follower=user1, following=user2).exists()
    backward_follow = Follow.objects.filter(follower=user2, following=user1).exists()
    
    return forward_follow and backward_follow