from authentik.core.models import User

email = request.context["prompt_data"]["email"]
if email!="" and User.objects.filter(email=email).exists():
  ak_message("Email address already in use")
  return False
return True