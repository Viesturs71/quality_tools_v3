import logging
import subprocess

logger = logging.getLogger(__name__)

def git_checkout(ref: str, cwd: str | None = None) -> bool:
    """
    Checkout a specific Git reference (branch, tag, commit)

    Args:
        ref: The Git reference to checkout
        cwd: Working directory, uses current directory if not specified

    Returns:
        bool: True if checkout successful, False otherwise
    """
    try:
        subprocess.run(
            ['git', 'checkout', ref],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        logger.info(f"Successfully checked out {ref}")
        return True

    except subprocess.CalledProcessError as e:
        logger.error(f"Git checkout failed: {e.stderr}")
        return False
