if not ' ' in request.context["prompt_data"]["username"]:
  return True
ak_message("Username cannot have spaces.")
return False