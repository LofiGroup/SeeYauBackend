def like_to_response_model(like):
    return {
        "id": like.pk,
        "by_who": like.who.pk,
        "when": like.when,
        "is_liked": like.is_liked
    }