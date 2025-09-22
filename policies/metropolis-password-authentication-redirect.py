if request.context["pending_user"].attributes["passwordless-auth"] == "Yes":
  return False
return True