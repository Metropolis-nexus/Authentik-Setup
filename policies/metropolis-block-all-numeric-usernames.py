import re
if not re.match('^[0-9]+$', request.context["prompt_data"]["username"]):
  return True
ak_message("All numeric usernames are not allowed.")
return False