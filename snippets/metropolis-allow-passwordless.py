# Check if the user enabled passwordless login

if request.context["pending_user"].attributes["passwordless"] == "Yes":
  return True
ak_message("Passwordless login not enabled in account settings.")
return False