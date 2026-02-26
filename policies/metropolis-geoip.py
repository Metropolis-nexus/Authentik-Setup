if (context["geoip"]["country"] == "GB"):
  ak_message("United Kingdom IP addresses are not allowed.")
  return False
return True
