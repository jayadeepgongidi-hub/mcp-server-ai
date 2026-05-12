from mcp.server.fastmcp import FastMCP

# Create an MCP server for managing a simple in-memory to-do list
mcp = FastMCP("AI To-Do List")

# In-memory storage for to-do items
todo_list = []

@mcp.tool()
def add_todo(item: str) -> str:
    """
    Add a new to-do item to the in-memory list.

    Args:
        item (str): The task to be added to the list.

    Returns:
        str: Confirmation message indicating the task was added.
    """
    todo_list.append(item)
    return f"Added to-do: '{item}'"

@mcp.tool()
def list_todos() -> str:
    """
    Retrieve the full list of current to-do items.

    Returns:
        str: Formatted string of all to-do items.
    """
    if not todo_list:
        return "Your to-do list is empty."
    return "\n".join(f"{idx+1}. {task}" for idx, task in enumerate(todo_list))

@mcp.tool()
def update_todo(index: int, new_item: str) -> str:
    """
    Update a to-do item by its index (1-based).

    Args:
        index (int): 1-based index of the item to update.
        new_item (str): The new content for the task.

    Returns:
        str: Confirmation or error message.
    """
    if 0 < index <= len(todo_list):
        old_item = todo_list[index - 1]
        todo_list[index - 1] = new_item
        return f"Updated to-do {index}: '{old_item}' -> '{new_item}'"
    return "Invalid index."

@mcp.tool()
def delete_todo(index: int) -> str:
    """
    Delete a to-do item by its index (1-based).

    Args:
        index (int): 1-based index of the task to remove.

    Returns:
        str: Confirmation or error message.
    """
    if 0 < index <= len(todo_list):
        removed = todo_list.pop(index - 1)
        return f"Deleted to-do {index}: '{removed}'"
    return "Invalid index."

@mcp.resource("todos://latest")
def get_latest_todo() -> str:
    """
    Get the most recently added to-do item.

    Returns:
        str: The latest task or a default message if list is empty.
    """
    return todo_list[-1] if todo_list else "No to-dos yet."

@mcp.prompt()
def todo_summary_prompt() -> str:
    """
    Generate a prompt asking the AI to summarize the current to-do list.

    Returns:
        str: AI-ready prompt string, or a default message if list is empty.
    """
    if not todo_list:
        return "There are no to-do items."
    return f"Summarize the following to-do items: {', '.join(todo_list)}"