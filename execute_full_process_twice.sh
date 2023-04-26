echo "===== EXECUTING execute_full_process_twice.sh ====="
cat execute_full_process_twice.sh
echo "===== EXECUTING python clear_results.py ====="
python clear_results.py
echo "===== EXECUTING python fullprocess.py (FOR THE FIRST TIME) ====="
python fullprocess.py
echo "===== EXECUTING ./use_configuration_2.sh ====="
./use_configuration_2.sh
echo "===== EXECUTING python fullprocess.py (FOR THE SECOND TIME) ====="
python fullprocess.py
