# Advanced-SE-Project
Project for the Advanced Software Engineering course at the University of Cincinnati. I will be testing the Genie tool to automatically detect bugs in a new application and then make a change to the algorithm to compare bug-finding effect.

## Deliverables
The deliverables for the project can be found in the main directory. The project report is names Project_Report.md and the slides are Advanced SE Project.pdf. As for the implementation of the systematic seed generation algorithm, 
look in Genie/droidbot/systematic_policy.py. I wrote everything in this python class to implement this seed test generation.

If you with to use the Genie tool with this new systematic generation method then use the command line option as follows: -seed-generation-strategy systematic

This option is used when genertating seed tests but I would also suggest using it when generation mutant tests.

For example when generating seed tests only: python3 -m droidbot.start -d emulator-5554 -a apps_for_test/de.rampro.activitydiary_118.apk -policy fuzzing_gen_seeds -count 100000 -max_seed_test_suite_size 20 -max_random_seed_test_length 15 -max_independent_trace_length 8 -max_mutants_per_insertion_position 300 -grant_perm -is_emulator -interval 1 -coverage -seed-generation-strategy systematic -o ./tmp-diary [-script script_samples/user_script.json]

For a complete guide to setting up and running the Genie tool, see DEVLEOPER.md
