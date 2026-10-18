if ' ' in request.context["prompt_data"]["username"]:
  ak_message("Username cannot have spaces.")
  return False
elif '@' in request.context["prompt_data"]["username"]:
  ak_message("Username cannot contain '@'.")
  return False
elif request.context["prompt_data"]["username"].startswith("."):
  ak_message("Username cannot start with a period.")
  return False
return True