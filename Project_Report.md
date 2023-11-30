# Final Project: Project Report

### Caleb Hendrix

## Description of Problem:

Apps have of course become ubiquitous in people’s lives. App developers are fight for users time and want to maintain active users by providing a good user experience. Bugs, both crash bugs and semantic logical bugs, can destroy user experience and cause users to uninstall the app. Proper testing of an app before release is therefore extremely important. Testing apps in rigorous ways becomes cost prohibitive when the testing techniques are done manually and the app has much functionality. There is a need for automated testing approaches. 

Google developed and released an automated testing tool that is widely used called Monkey. Monkey will make random GUI gestures on an application until a certain stopping condition is reached. Code coverage is measured by method execution logging and bug finding by the number of crashes that this testing causes. Other tools have improved on this simple random approach such as Stoat (Su et. al., 2017) and TimeMachine (Dong et. al., 2020). These tools are built on top of Monkey but include additional implementation to improve the code coverage and bug finding ability. A major issue with these existing tools is that they are only capable of finding crash bugs.

Finding semantic bugs in applications is just as necessary as finding crash bugs. The user experience can be affected in similar ways as a crash when a UI element is not behaving correctly. Many researchers recognized this need and so developed an automated fuzzing tool capable of detecting these semantic errors, Genie (Su et. al., 2021). Genie is able to accomplish the task of identifying semantic errors by generating test oracles. These test oracles are generated using the model based test generation tool DroidBot. DroidBot is able to create a UI transition graph, or UTG, from an app by mining the GUI transitional model (Li et. al., 2017). Genie uses this same principal of building up a UTG for an app, and from this model it can create test oracles.

Genie creates the test oracles by first generating seed tests for the application. These seed tests are generated randomly using methods that were adapted from the Stoat tool. The seed tests try to represent specific user scenarios such as adding a category on a to-do list or attaching a picture to a category. Genie then mutates these seed tests by adding in some extra steps in the middle of the test which ultimately loop back into the main seed test. The test oracles are the end result GUI views of the seed test and the mutant test. If there are missing elements in the mutant view that exist in the seed test view then this indicates a likely semantic bug. This is made possible by the independent views property in the applications, the idea that actions on one GUI element should not affect the state of other elements. 

Genie is very good at being able to catch both semantic and crash bugs, on par with other testing frameworks such as Monkey and Stoat. One of the shortcomings of the tool that the researchers admit is the randomness of the seed test generation. It became my goal in this project to look into a new way of generating the seed tests for an application, preferably a method that was not random. I began to look into other methods of test generation and became interested in the TimeMachine tool. The time travel testing that this tool detailed was shown to outperform both Stoat and Monkey in code coverage and crash bug finding (Dong et. al., 2020). The current seed test generation method in Genie was based on Stoat and so implementing a method based on TimeMachine became my goal.

I implemented a new systematic seed test generation strategy inspired by the approach of TimeMachine. In my seed generation method, I explore the UTG and identify interesting GUI states. As I explore I check if I have reached a state where I am not making progress, where I am stuck. If I become stuck then I go back to the last most interesting previous state and begin searching again down a different route. These methods implement the core ideas behind time travel testing and enable a systematic creation of seed tests.

## Experiment Results:

The Genie tool was evaluated using open source apps found on F-droid. Most of these apps were widely used, had hundreds of thousands of downloads, and were in functional categories that allowed for many simple interactions. Known bugs in these apps were gathered from public issue trackers such as GitHub in order to determine if the tool was capable of finding known bugs. In the same way, I identified applications on F-droid that were open source and I gathered any known bugs associated with these applications. I tested two apps, one was of a similar category as the apps that Genie used for evaluation. This was a financial planning app called Simple Accounting. I then wanted to choose an app that was not in the category that Genie had covered, so I choose a simple Minesweeper app.

I wanted to determine the Genie tool’s base performance testing these apps that I selected. I wanted to confirm that the tool could test these apps and spot any known bugs. I was curious if the tool could test the Minesweeper app well because games are more complex interaction-wise than the apps that Genie was evaluated against. For the Simple Accounting app I identified a few known bugs from the public issue tracker on GitHub:

1. Wrong behavior recorded - https://github.com/EmmanuelMess/Simple-Accounting/issues/136

2. Credit and Debit column swap - https://github.com/EmmanuelMess/Simple-Accounting/issues/108

3. Some crash behavior - https://github.com/EmmanuelMess/Simple-Accounting/issues/42

I wanted to determine if the Genie tool could actually find these known bugs during testing of the Simple Accounting app. For the Minesweeper app, I simply wanted to see the results of testing and see if the Genie tool could find any bugs at all.
My testing procedure included a baseline test of each of the 2 apps that I selected. This meant that I first tested each of the apps using the default settings of the Genie tool. These included default command line arguments for seed and mutant generation and testing time. This was to ensure accurate comparison to the tool performance as described in the paper. A second round of testing was then done where the only change in the testing strategy was the use of my new systematic seed generation approach. This was to ensure an accurate comparison between the approach that the Genie tool used, random generation, to my new approach which is systematic. The results of these two testing rounds are presented below.


## Simple Accounting:

Initial Baseline: There were 113,171 mutants created and executed using the baseline command line arguments for the initial test of this app. Of these executed mutants, 10,186 were analyzed for semantic or crash errors. The baseline test of the Genie tool was not able to identify any crash bugs. There were two identified semantic bugs reported by the tool. These results can be viewed in the file merged_results_2023-1116-211058_seed-test-2.csv in the output directory tmp-simpleaccounting

Systematic approach: There were only 32,994 mutants generated for this test run and 4,249 that were evaluated for errors. In this test run there were no crashing or semantic errors reported in the evaluated mutant test. These results can be viewed in the file merged_results_2023-1119-102744_seed-test-2.csv in the output directory tmp-simpleaccounting-systematic.

## Minesweeper:

Initial Baseline: The initial run of testing of the minesweeper app did not produce any mutant tests which indicated and crash or semantic errors. The results can be viewed in the tmp-minesweeper output directory. 

Systematic approach: There were 32,126 mutants produced for the testing of the minesweeper app using the systematic seed generation approach. 4,146 of these were evaluated for crash and semantic errors. The systematic approach also did not find any crash or semantic bugs in the testing. These results can be seen in merged_results_2023-1119-165052_seed-test-2.csv in the tmp-minesweeper-systematic output directory.

## Discussion:
Overall, the Genie tool was not very effective at identifying the crash and semantic bugs for the apps that were tested. The identified bugs for simple accounting that were retrieved from github were not identified by the Genie tool nor was the reported crashing bug. Genie was also not able to test the Minesweeper app very well as it never finished a game, this was expected though as the Genie tool is not equipped to handle games. Genie’s inability to find these bugs seems to be due to the model based testing method. Sometimes a UTG is constructed that will not allow the Genie tool to find a certain bug or perhaps the seed tests generated simply do not cover functionality that a bug is in. These are also limitations of model based testing approaches generally. The Systematic method created here may be better suited if the UTG exploration is made longer and the length of each individual seed test was also increased. These changes may help the systematic seed generation strategy that I developed to be more effective.

## References:

Dong, Z., Böhme, M., Cojocaru, L., & Roychoudhury, A. (2020b). Time-travel testing of Android apps. IEEE/ACM 42nd International Conference on Software Engineering. https://doi.org/10.1145/3377811.3380402
Li, Y., Yang, Z., Guo, Y., & Chen, X. (2017). DroidBot: a lightweight UI-Guided test input generator for android. IEEE/ACM 39th IEEE International Conference on Software Engineering Companion. https://doi.org/10.1109/icse-c.2017.8
Su, T., Meng, G., Chen, Y., Wu, K., Yang, W., Yao, Y., Pu, G., Liu, Y., & Su, Z. (2017). Guided, stochastic model-based GUI testing of Android apps. Association for Computing Machinery. https://doi.org/10.1145/3106237.3106298
Su, T., Yan, Y., Wang, J., Sun, J., Xiong, Y., Pu, G., Wang, K., & Su, Z. (2021). Fully automated functional fuzzing of Android apps for detecting non-crashing logic bugs. Proceedings of the ACM on Programming Languages, 5(OOPSLA), 1–31. https://doi.org/10.1145/3485533
