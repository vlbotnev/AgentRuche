def get_calls_by_manager(manager_name: str) -> list:
    """A tool that finds calls in the database for a specific manager."""
    print(f"Tool executed: getting calls for {manager_name}")
    return [{"id": "mock_call_123", "manager": manager_name}]
