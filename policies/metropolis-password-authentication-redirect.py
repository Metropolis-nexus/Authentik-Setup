if request.context["pending_user"].attributes["passwordless_auth"] == "Yes":
  return False
return True