if ak_is_group_member(request.context["pending_user"], name="authentik Service Accounts"):
  ak_message("Service accounts cannot login here. How did you even get this far?!")
  return False
  
return True