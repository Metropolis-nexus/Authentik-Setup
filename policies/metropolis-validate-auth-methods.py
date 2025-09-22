standard = request.context["prompt_data"]["attributes"]["standard-auth"]

passwordless = request.context["prompt_data"]["attributes"]["passwordless-auth"]

if standard=="Yes" or passwordless=="Yes":
  return True

ak_message("You must enable at least one authentication method.")
return False