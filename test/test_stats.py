import pytest
import sqlite3
import time
from http_monitor.stats.stats import Stats

class TestStats:
    @pytest.fixture
    def db(self, tmpdir):
        dbconn = sqlite3.connect(tmpdir.dirname + "test_stats.db") 
        dbcursor = dbconn.cursor()
        dbcursor.execute("DROP TABLE IF EXISTS Hit")
        dbcursor.execute("CREATE TABLE IF NOT EXISTS Hit (host text, logname text, authuser text, date integer, request_type text, domain text, section text, trail text, version text, status text, bites integer)")
        return (dbconn, dbcursor)

    @pytest.fixture 
    def stats(self, db):
        return Stats(*db) 

    def test_get_total_traffic_with_no_traffic(self, db, stats):
        dbconn, dbcursor = db
        assert stats.get_total_traffic()[0] == 0
        dbconn.close()

    def test_get_total_traffic_with_changing_traffic(self, db, stats):
        dbconn, dbcursor = db
        for _ in range(20):
            # Make sure times are well into the threshold, there is a weird bug if using the current time
            dbcursor.execute("INSERT INTO Hit VALUES (?,?,?,?,?,?,?,?,?,?,?)", 
                ["host", "loguser", "authuser", time.time()-5, "GET", "domain", "section", "", "HTTP/1.1", "200", 0])
        dbconn.commit()
        assert stats.get_total_traffic()[0] == 20
        dbconn.close()
