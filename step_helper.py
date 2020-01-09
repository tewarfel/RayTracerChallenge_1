
def ensure_context_has_tuple(context):
    try:
        if (context.tuple is None):
            context.tuple = {}
    except:
        context.tuple = {}


def ensure_context_has_dict(context):
    try:
        if (context.dict is None):
            context.dict = {}
    except:
        context.dict = {}
