from authentik.core.models import User

current_email = request.user.email
new_email = request.context["prompt_data"]["email"]

if new_email == "":
    return True

if new_email == current_email:
    return True

if User.objects.filter(email=new_email).exists():
  ak_message("Email address already in use")
  return False
  
return True