from http_monitor import main
main.main(database = "sample.db", 
    log = "sample_logs/sample.log", 
    interval = 10, 
    threshold_time = 120, 
    threshold_amount = 20)
