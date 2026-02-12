if (context["geoip"]["country"] == "GB"):
  ak_message("United Kingdom IP addresses are not allowed.")
  return False
elif (context["geoip"]["country"] == "AU"):
  ak_message("Australian IP addresses are not allowed.")
  return False
return True
