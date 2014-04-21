import pytest
import sqlite3
import time
from http_monitor.stats import stats

class TestStats:
    @pytest.fixture
    def db(self, tmpdir, request):
        dbconn = sqlite3.connect(tmpdir.dirname + "test_stats.db") 
        request.addfinalizer(lambda : dbconn.close())
        dbcursor = dbconn.cursor()
        dbcursor.execute("DROP TABLE IF EXISTS Hit")
        dbcursor.execute("CREATE TABLE IF NOT EXISTS Hit (host text, logname text, authuser text, date integer, request_type text, domain text, section text, trail text, version text, status text, bites integer)")
        return (dbconn, dbcursor)

    @pytest.fixture 
    def my_stats(self, db):
        dbconn, dbcursor = db
        return stats.Stats(dbconn, dbcursor, 120, 20) 

    def test_get_total_traffic_with_no_traffic(self, db, my_stats):
        dbconn, dbcursor = db
        assert my_stats.get_total_traffic()[0] == 0

    def test_get_total_traffic_with_changing_traffic(self, db, my_stats):
        dbconn, dbcursor = db
        for _ in range(20):
            # Make sure times are well into the threshold, there is a weird bug if using the current time
            dbcursor.execute("INSERT INTO Hit VALUES (?,?,?,?,?,?,?,?,?,?,?)", 
                ["host", "loguser", "authuser", time.time()-5, "GET", "domain", "section", "", "HTTP/1.1", "200", 0])
        dbconn.commit()
        assert my_stats.get_total_traffic()[0] == 20

    def test_new_alert_and_recover(self, db, my_stats):
        dbconn, dbcursor = db
        threshold = 20
        for _ in range(threshold + 1):
            dbcursor.execute("INSERT INTO Hit VALUES (?,?,?,?,?,?,?,?,?,?,?)", 
                ["host", "loguser", "authuser", time.time()-5, "GET", "domain", "section", "", "HTTP/1.1", "200", 0])
        dbconn.commit()
        alerts = my_stats.get_alerts()
        assert len(alerts) == 1
        assert alerts[0][0] == threshold+1
        dbcursor.execute("UPDATE Hit SET date = 0")
        dbconn.commit()
        alerts = my_stats.get_alerts()
        assert len(alerts) == 1
        assert alerts[0][2] != 0
