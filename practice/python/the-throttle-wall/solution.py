def run_rate_limiter(operations):
  max_requests = 0
  window_ms = 0
  # Per-client dict mapping client_id -> list of accepted timestamps,
  # used as a queue with an index pointer for O(1) amortized dequeue.

  accepted = {}
  head = {}  # client_id -> index of the oldest live element in accepted[cid]
  results = []

  for op in operations:
    if op[0] == "init":
      _, max_requests, window_ms = op
      results.append(None)
    elif op[0] == "is_allowed":
      _, client_id, timestamp = op

      q = accepted.get(client_id)
      if q is None:
        q = []
        accepted[client_id] = q
        head[client_id] = 0
      h = head[client_id]
      cutoff = timestamp - window_ms

      # Evict aged-out accepted calls by advancing the head pointer.

      while h < len(q) and q[h] <= cutoff:
        h += 1
      head[client_id] = h

      if len(q) - h < max_requests:
        q.append(timestamp)
        results.append(True)
      else:
        results.append(False)
  return results
