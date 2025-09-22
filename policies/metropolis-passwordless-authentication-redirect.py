if request.context["pending_user"].attributes["standard-auth"] == "No" and ak_user_has_authenticator(context['pending_user'], 'webauthn'):
  return True
return False