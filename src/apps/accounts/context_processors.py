from apps.accounts.models import Profile


def user_profile_context(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None
    else:
        profile = None

    return {
        'navbar_profile': profile
    }
