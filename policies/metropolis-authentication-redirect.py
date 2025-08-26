if ak_user_has_authenticator(context['pending_user'], 'webauthn'):
  return False
return True