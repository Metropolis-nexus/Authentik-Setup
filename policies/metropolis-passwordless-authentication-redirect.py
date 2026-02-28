if request.context["pending_user"].attributes.get("passwordless_auth", "No") == "No":
  return True

if ak_user_has_authenticator(context['pending_user'], 'webauthn'):
  return False
  
return True