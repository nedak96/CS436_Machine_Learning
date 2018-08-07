Python program that uses Naive Bayes or logistic regression to determine whether a file is spam or ham.  It includes the option to use a stop word filter and a simple feature selector that just removes words based on frequency.

To run: python hamOrSpam.py <algorithm: nb/lr> <stop word filter: yes/no> <feature selector: yes/no>

Naive Bayes Results:
0.943514644351
0.945606694561

Logistic Regression Results:
0.851464435146
0.880753138075

Naive Bayes with Feature Selector:
0.943514644351
0.935146443515

Logistic Regression with Feature Selector:
0.851464435146
0.878661087866
