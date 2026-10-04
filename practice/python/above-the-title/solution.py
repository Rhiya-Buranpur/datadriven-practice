from collections import defaultdict


def actor_genre_box_office(
  movies: list[dict],
  actors: list[dict],
  mapping: list[dict],
  genre: str,
  min_rating: float,
) -> dict:
  # Step 1: Index qualifying movies by movie_id -> box_office
  #         (only movies matching genre AND rating >= min_rating)

  qualifying_movies: dict[int, int] = {
    m["movie_id"]: m["box_office"]
    for m in movies
    if m["genre"] == genre and m["rating"] >= min_rating
  }

  # Short-circuit: no qualifying films means no actors qualify

  if not qualifying_movies:
    return {}
  # Step 2: Index actor names by actor_id for O(1) lookup

  actor_names: dict[int, str] = {a["actor_id"]: a["name"] for a in actors}

  # Step 3: Accumulate box_office per actor across qualifying films

  totals: dict[int, int] = defaultdict(int)
  for row in mapping:
    movie_id = row["movie_id"]
    if movie_id in qualifying_movies:
      totals[row["actor_id"]] += qualifying_movies[movie_id]
  # Step 4: Map actor_id -> name, dropping any unknown actor_ids

  result: dict[str, int] = {
    actor_names[actor_id]: total
    for actor_id, total in totals.items()
    if actor_id in actor_names
  }

  return result
