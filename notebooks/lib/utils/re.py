import re
def get_trailing_number(search_text):
	search_obj = re.search(r"([0-9]+)$", search_text)
	if not search_obj:
		return 0
	else:
		return int(search_obj.group(1))