


def get_help(inpt_json):
    return inpt_json["help_router"]["help_message"]


def get_languages(inpt_json):
    return inpt_json["help_router"]["languages"]


def get_single(inpt_json):
    return inpt_json["help_router"]["single"]


def get_batch(inpt_json):
    return inpt_json["help_router"]["batch"]