# Redirect to a different flow if the user signs up with an email address

if request.context["prompt_data"]["email"] == "":
   return False
return True