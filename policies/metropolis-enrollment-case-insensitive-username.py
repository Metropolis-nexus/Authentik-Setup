# Source: https://github.com/goauthentik/authentik/issues/5844#issuecomment-1590005763

if ak_user_by(username__iexact=context['prompt_data']['username']) is None:
  return True
else:
  ak_message("Username is already taken.")
  return False