from ninja import Router

router = Router()


@router.get(path="/")
def get_users(request):
    users = User.objects.all()
    return users
