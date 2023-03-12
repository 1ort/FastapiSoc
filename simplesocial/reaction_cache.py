reaction_count_cache = {}
reaction_cache = {}


def cached_reactions_count(func):
    def wrapper(post_obj):
        post_id = post_obj.id
        cached = reaction_count_cache.get(post_id)
        if not cached:
            cached = func(post_obj)
            reaction_count_cache[post_id] = cached
        return cached
    return wrapper


def update_reaction_cache(func):
    def wrapper(*args, **kwargs):
        reaction_obj = func(*args, **kwargs)
        if reaction_obj is None:
            return reaction_obj
        from_id = reaction_obj.from_id
        post_id = reaction_obj.post_id
        try:
            # To recalculate the number of reactions
            del reaction_count_cache[post_id]
        except KeyError:
            pass
        reaction_cache[(from_id, post_id)] = reaction_obj
        return reaction_obj
    return wrapper


def delete_from_cache(func):
    def wrapper(db_obj, reaction_obj):
        from_id = reaction_obj.from_id
        post_id = reaction_obj.post_id
        try:
            # To recalculate the number of reactions
            del reaction_count_cache[post_id]
        except KeyError:
            pass
        try:
            del reaction_cache[(from_id, post_id)]
        except KeyError:
            pass
        return func(db_obj, reaction_obj)
    return wrapper


def get_from_cache(func):
    def wrapper(db_obj, post_obj, user_obj):
        from_id = user_obj.id
        post_id = post_obj.id
        reaction_obj = reaction_cache.get((from_id, post_id))
        if reaction_obj is None:
            reaction_obj = func(db_obj, post_obj, user_obj)
            reaction_cache[(from_id, post_id)] = reaction_obj
        return reaction_obj
    return wrapper
