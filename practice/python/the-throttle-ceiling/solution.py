from collections import deque


class RateLimiter:
  def __init__(self, max_requests: int, window_seconds: float):
    self.max_requests = max_requests
    self.window_seconds = window_seconds
    # Monotonic deque of accepted timestamps (arrivals are non-decreasing)

    self._accepted: deque[float] = deque()

  def is_allowed(self, timestamp: float) -> bool:
    # Evict accepted calls that have fallen out of the window.
    # Boundary is exclusive: a call at exactly (timestamp - window) is OUT.

    cutoff = timestamp - self.window_seconds
    while self._accepted and self._accepted[0] <= cutoff:
      self._accepted.popleft()
    if len(self._accepted) < self.max_requests:
      self._accepted.append(timestamp)
      return True
    return False


def run_rate_limiter(calls, max_requests, window_seconds):
  limiter = RateLimiter(max_requests, window_seconds)
  return [limiter.is_allowed(t) for t in calls]
