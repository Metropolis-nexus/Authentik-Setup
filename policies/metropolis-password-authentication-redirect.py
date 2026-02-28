if request.context["pending_user"].attributes.get("passwordless_auth", "No") == "Yes":
  return False
return True