session_memories = {}

def get_memory_for_user(email):
    """
    Retrieve the last memory session list for a given user email.
    Creates a new session if one doesn't exist.
    """
    if email not in session_memories:
        session_memories[email] = []
    return session_memories[email]

def add_to_memory(email, user_query, bot_response):
    """
    Append the latest interaction to the user's memory.
    """
    formatted = f"User: {user_query}\nBot: {bot_response}"
    session_memories[email].append(formatted)
    print(session_memories)

def build_context(email, latest_query, max_turns=3):
    memory = get_memory_for_user(email)
    user_turns = [m.split("User:")[-1].strip() for m in memory if "User:" in m]
    last_user_turns = user_turns[-max_turns:] if len(user_turns) >= max_turns else user_turns
    context = "\n".join([f"User: {q}" for q in last_user_turns] + [f"User: {latest_query}"])
    return context


