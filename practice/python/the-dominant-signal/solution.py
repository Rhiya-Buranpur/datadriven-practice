def most_frequent(items: list) -> list:
  if not items:
    return []

  # Count frequencies
  freq = {}
  for item in items:
    freq[item] = freq.get(item, 0) + 1

  # Find the maximum frequency
  max_count = max(freq.values())

  # Collect all items with the maximum frequency, sorted ascending
  result = sorted([key for key, count in freq.items() if count == max_count])

  return result
