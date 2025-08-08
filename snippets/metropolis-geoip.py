# GeoIP block
# The UK block is temporary. We are waiting for lawsuits against Ofcom. OSA is most likely unenforcable in the US and also violates the first admendment.

if (context["geoip"]["country"] == "GB"):
  ak_message("United Kingdom IP addresses are not allowed.")
  return False
return True