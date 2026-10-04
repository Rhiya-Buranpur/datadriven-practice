def high_water_marks(readings):
  result = []
  current_max = float('-inf')
    
  for reading in readings:
    current_max = max(current_max, reading)
    result.append(current_max)
    
  return result
