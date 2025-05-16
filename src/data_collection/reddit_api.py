from src.utils.paths import get_project_root
import os
import yaml
import praw


def get_reddit_instance(config_filename="config.yaml"):
    """
    Initialise and return a read-only Reddit API client using credentials from a YAML config file.

    Parameters:
        config_filename (str): Filename of the YAML config file (default: "config.yaml")

    Returns:
        praw.Reddit: An authenticated, read-only Reddit instance.

    Raises:
        FileNotFoundError: If the config file is not found.
        KeyError: If expected keys are missing in the YAML.
        praw.exceptions.PRAWException: If Reddit API client cannot be initialised.
    """
    # Resolve full path to config
    project_root = get_project_root()
    config_path = project_root / config_filename

    if not config_path.exists():
        raise FileNotFoundError(f"[ERROR] Config file not found at {config_path}")

    # Load Reddit API credentials from YAML config
    try:
        with open(config_path, 'r') as f:
            reddit_login = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ValueError(f"[ERROR Failed to parse YAML config {e}")
    
    try:
        reddit_config = reddit_login['reddit']
        client_id=reddit_config['client_id']
        client_secret=reddit_config['client_secret']
        user_agent=reddit_config['user_agent']
    except KeyError as e:
        raise KeyError(f"[ERROR] Missing required key in config: {e}")

    # Create Reddit instance
    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        # Sanity check: confirm instance is read-only
        assert reddit.read_only, "[ERROR] Reddit instance is not read-only. Check credentials."
    except Exception as e:
        raise RuntimeError(f"[ERROR] Failed to initialise Reddit instance {e}")


    return reddit
