if not ak_is_group_member(request.context["pending_user"], name="metropolis-banned"):
  return True
ak_message("Account banned.")
return False