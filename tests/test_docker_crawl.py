import subprocess
import pytest
import sqlite3
from .fixtures import *

def test_docker_crawl(tmp_path, process):
    """
    Test that a crawl with a depth of 1 is successful and archives the correct number of pages.
    """
    # Add a seed URL and crawl
    subprocess.run(["archivebox", "add", "http://127.0.0.1:8080/static/example.com.html", "--depth=1"], capture_output=True)

    # Check that the crawl was successful
    conn = sqliteite3.connect("index.sqlite3")
    c = conn.cursor()
    urls = c.execute("SELECT url from core_snapshot").fetchall()
    conn.commit()
    conn.close()

    urls = list(map(lambda x: x[0], urls))
    assert "http://127.0.0.1:8080/static/example.com.html" in urls
    assert "http://127.0.0.1:8080/static/iana.org.html" in urls
    assert len(urls) == 2
