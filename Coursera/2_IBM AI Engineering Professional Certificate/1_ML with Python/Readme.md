- Course Link: [Course Link](https://www.coursera.org/learn/machine-learning-with-python)

- M1 Summary:

    - Artificial intelligence (AI) simulates human cognition, while machine learning (ML) uses algorithms and requires feature engineering to learn from data.

    - Machine learning includes different types of models: supervised learning, which uses labeled data to make predictions; unsupervised learning, which finds patterns in unlabeled data; and semi-supervised learning, which trains on a small subset of labeled data.

    - Key factors for choosing a machine learning technique include the type of problem to be solved, the available data, available resources, and the desired outcome.

    - Machine learning techniques include anomaly detection for identifying unusual cases like fraud, classification for categorizing new data, regression for predicting continuous values, and clustering for grouping similar data points without labels.

    - Machine learning tools support pipelines with modules for data preprocessing, model building, evaluation, optimization, and deployment.

    - R is commonly used in machine learning for statistical analysis and data exploration, while Python offers a vast array of libraries for different machine learning tasks. Other programming languages used in ML include Julia, Scala, Java, and JavaScript, each suited to specific applications like high-performance computing and web-based ML models.

    - Data visualization tools such as Matplotlib and Seaborn create customizable plots, ggplot2 enables building graphics in layers, and Tableau provides interactive data dashboards.

    - Python libraries commonly used in machine learning include NumPy for numerical computations, Pandas for data analysis and preparation, SciPy for scientific computing, and Scikit-learn for building traditional machine learning models.

    - Deep learning frameworks such as TensorFlow, Keras, Theano, and PyTorch support the design, training, and testing of neural networks used in areas like computer vision and natural language processing.

    - Computer vision tools enable applications like object detection, image classification, and facial recognition, while natural language processing (NLP) tools like NLTK, TextBlob, and Stanza facilitate text processing, sentiment analysis, and language parsing.

    - Generative AI tools use artificial intelligence to create new content, including text, images, music, and other media, based on input data or prompts.

    - Scikit-learn provides a range of functions, including classification, regression, clustering, data preprocessing, model evaluation, and exporting models for production use.

    - The machine learning ecosystem includes a network of tools, frameworks, libraries, platforms, and processes that collectively support the development and management of machine learning models.

- M2 Summary:

    - Regression models relationships between a continuous target variable and explanatory features, covering simple and multiple regression types.

    - Simple regression uses a single independent variable to estimate a dependent variable, while multiple regression involves more than one independent variable.

    - Regression is widely applicable, from forecasting sales and estimating maintenance costs to predicting rainfall and disease spread.

    - In simple linear regression, a best-fit line minimizes errors, measured by Mean Squared Error (MSE); this approach is known as Ordinary Least Squares (OLS).

    - OLS regression is easy to interpret but sensitive to outliers, which can impact accuracy.

    - Multiple linear regression extends simple linear regression by using multiple variables to predict outcomes and analyze variable relationships.

    - Adding too many variables can lead to overfitting, so careful variable selection is necessary to build a balanced model.

    - Nonlinear regression models complex relationships using polynomial, exponential, or logarithmic functions when data does not fit a straight line.

    - Polynomial regression can fit data but may overfit by capturing random noise rather than the underlying patterns.  

    - Logistic regression is a probability predictor and binary classifier, suitable for binary targets and assessing feature impact.

    - Logistic regression minimizes errors using log-loss and optimizes with gradient descent or stochastic gradient descent for efficiency.

    - Gradient descent is an iterative process to minimize the cost function, which is crucial for training logistic regression models.

- Module 3 Summary:

    - Classification is a supervised machine learning method used to predict labels on new data with applications in churn prediction, customer segmentation, loan default prediction, and multiclass drug prescriptions.

    - Binary classifiers can be extended to multiclass classification using one-versus-all or one-versus-one strategies.

    - A decision tree classifies data by testing features at each node, branching based on test results, and assigning classes at leaf nodes.

    - Decision tree training involves selecting features that best split the data and pruning the tree to avoid overfitting.

    - Information gain and Gini impurity are used to measure the quality of splits in decision trees.

    - Regression trees are similar to decision trees but predict continuous values by recursively splitting data to maximize information gain.

    - Mean Squared Error (MSE) is used to measure split quality in regression trees.

    - K-Nearest Neighbors (k-NN) is a supervised algorithm used for classification and regression by assigning labels based on the closest labeled data points.

    - To optimize k-NN, test various k values and measure accuracy, considering class distribution and feature relevance.

    - Support Vector Machines (SVM) build classifiers by finding a hyperplane that maximizes the margin between two classes, effective in high-dimensional spaces but sensitive to noise and large datasets.

    - The bias-variance tradeoff affects model accuracy, and methods such as bagging, boosting, and random forests help manage bias and variance to improve model performance.

    - Random forests use bagging to train multiple decision trees on bootstrapped data, improving accuracy by reducing variance.

- Module 4 Summary:

    - Clustering is a machine learning technique used to group data based on similarity, with applications in customer segmentation and anomaly detection.

    - K-means clustering partitions data into clusters based on the distance between data points and centroids but struggles with imbalanced or non-convex clusters.

    - Heuristic methods such as silhouette analysis, the elbow method, and the Davies-Bouldin Index help assess k-means performance.

    - DBSCAN is a density-based algorithm that creates clusters based on density and works well with natural, irregular patterns.

    - HDBSCAN is a variant of DBSCAN that does not require parameters and uses cluster stability to find clusters.

    - Hierarchical clustering can be divisive (top-down) or agglomerative (bottom-up) and produces a dendrogram to visualize the cluster hierarchy.

    - Dimension reduction simplifies data structure, improves clustering outcomes, and is useful in tasks such as face recognition (using eigenfaces).

    - Clustering and dimension reduction work together to improve model performance by reducing noise and simplifying feature selection.

    - PCA, a linear dimensionality reduction method, minimizes information loss while reducing dimensionality and noise in data.

    - t-SNE and UMAP are other dimensionality reduction techniques that map high-dimensional data into lower-dimensional spaces for visualization and analysis.

- Module 5 Summary:

    - Supervised learning evaluation assesses a model's ability to predict outcomes for unseen data, often using a train/test split to estimate performance.

    - Key metrics for classification evaluation include accuracy, confusion matrix, precision, recall, and the F1 score, which balances precision and recall.

    - R- egression model evaluation metrics include MAE, MSE, RMSE, R-squared, and explained variance to measure prediction accuracy.

    - Unsupervised learning models are evaluated for pattern quality and consistency using metrics like Silhouette Score, Davies-Bouldin Index, and Adjusted Rand Index.

    - Dimensionality reduction evaluation involves Explained Variance Ratio, Reconstruction Error, and Neighborhood Preservation to assess data structure retention.

    - Model validation, including dividing data into training, validation, and test sets, helps prevent overfitting by tuning hyperparameters carefully.

    - Cross-validation methods, especially K-fold and stratified cross-validation, support robust model validation without overfitting to test data.

    - Regularization techniques, such as ridge (L2) and lasso (L1) regression, help prevent overfitting by adding penalty terms to linear regression models.

    - Data leakage occurs when training data includes information unavailable in real-world data, which is preventable by separating data properly and mindful feature selection.

    - Common modelling pitfalls include misinterpreting feature importance, ignoring class imbalance, and making causal inferences without sufficient evidence.”  

    - Feature importance assessments should consider redundancy, scale sensitivity, and avoid misinterpretation, as well as inappropriate assumptions about causation.

- Module 6 Summary:

    - Final Exam...