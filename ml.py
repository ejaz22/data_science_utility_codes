

# transform data
def transform_data(data,t_type=0,m='min'):
    '''
    A t_type to transform data in Gaussian which is not Gaussian in nature using different techniques
    param:
        data: input data in the form of numpy array or pandas series
        t_type: transformation type 
                options:   int {
                                0: Square Root
                                1: Normalization
                                2: Sigmoid
                                3: Cube Root
                                4: Normalized Cube Root
                                5: Log
                                6: Log Max Root
                                7: Normalized Log
                                8: Normalized Log Max Root
                                9: Hyperbolic Tangent
                                10: 
                            }
    out:
        transformed data 
    '''

    def normalize_(data):
        upper = data.max()
        lower = data.min()
        return (column - lower)/(upper-lower)
    
    def sigmoid_(data):
        e = np.exp(1)
        return 1/(1+e**(-data))

    def log_(data):
        if data.min()>0:
            return np.log(data)
        else:
            return np.log(data+1)
    
    
    if t_type==0:
        return np.sqrt(data)

    if t_type==1:
        return normalize_(data) # normalize
    
    elif t_type==2:
        return sigmoid_(data) # sigmoid
    
    elif t_type==3:
        return data**(1/3) # cube root

    elif t_type==4:
        return normalize_(data**(1/3)) # normalized cube root

    elif t_type==5:
        return log_(data) # log

    elif t_type==6:
        return data**(np.log(data.max())) # log-max-root 

    elif t_type==7:
        return normalize_(log_(data)) # normalized log

    elif t_type==8:
        return normalize_(data**(np.log(data.max()))) # normalized log-max-root

    elif t_type==9:
        return np.tanh(data) # hyperbolic tangent
    
    elif t_type==10:
        return data.rank(method=m).apply(lambda x: (x-1)/len(data)-1)

    else:
        print('No Suitable t_type Specified. Returning Data')
        return(data) 
    

print(transform_data([1,2,3],t_type=2))

# print False Postive and False Negative samples
def print_fp_fn_samples(test_y, test_y_pred, test_txt):

    i_lst_fp = [i for i in xrange(len(test_y)) if test_y[i] == 0 and test_y_pred[i] == 1]
    i_lst_fn = [i for i in xrange(len(test_y)) if test_y[i] == 1 and test_y_pred[i] == 0]
    print '\nfalse positive'
    for i in i_lst_fp[:20]:
        print i, test_y[i], ':', test_txt[i]
    print 'false negative'
    for i in i_lst_fn[:20]:
        print i, test_y[i], ':', test_txt[i]
        
        
# perform TSNE
def perform_tsne(X, y, perplexity=100, learning_rate=200, n_components=2):
    tsne = TSNE(n_components=n_components, init='random',
                         random_state=None, perplexity=perplexity, verbose=1)
    result = tsne.fit_transform(X)
    result = pd.DataFrame(result)
    result = result.join(y)
    result.columns = ['x0', 'x1', 'y']
    sns.lmplot('x0', 'x1', result, fit_reg=False, hue='y', palette={0:"#2662c1", 1:"#c9001e"},
              scatter_kws={'alpha': .5})
    plt.title('t-SNE plot')
    plt.plot()


# get feature importance
def get_rf_feat_importances(X,y):
    rf = RandomForestClassifier(n_estimators=20, random_state = 42)
    rf.fit(X, y)
    df = pd.DataFrame(
        {'feature': X.columns, 'importance':rf.feature_importances_})
    df = df.sort_values(by=['importance'], ascending=False)
    return df


from sklearn.model_selection import learning_curve
from sklearn.model_selection import ShuffleSplit


# plot learning curve
def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
                    n_jobs=1, train_sizes=np.linspace(.1, 1.0, 5)):
"""
Generate a simple plot of the test and training learning curve.

Parameters
----------
estimator : object type that implements the "fit" and "predict" methods
    An object of that type which is cloned for each validation.

title : string
    Title for the chart.

X : array-like, shape (n_samples, n_features)
    Training vector, where n_samples is the number of samples and
    n_features is the number of features.

y : array-like, shape (n_samples) or (n_samples, n_features), optional
    Target relative to X for classification or regression;
    None for unsupervised learning.

ylim : tuple, shape (ymin, ymax), optional
    Defines minimum and maximum yvalues plotted.

cv : int, cross-validation generator or an iterable, optional
    Determines the cross-validation splitting strategy.
    Possible inputs for cv are:
      - None, to use the default 3-fold cross-validation,
      - integer, to specify the number of folds.
      - An object to be used as a cross-validation generator.
      - An iterable yielding train/test splits.

    For integer/None inputs, if ``y`` is binary or multiclass,
    :param train_sizes:
    :class:`StratifiedKFold` used. If the estimator is not a classifier
    or if ``y`` is neither binary nor multiclass, :class:`KFold` is used.

    Refer :ref:`User Guide <cross_validation>` for the various
    cross-validators that can be used here.

 n_jobs : integer, optional
    Number of jobs to run in parallel (default 1).
"""
plt.figure()
plt.title(title)
if ylim is not None:
    plt.ylim(*ylim)
plt.xlabel("Training examples")
plt.ylabel("Score")
train_sizes, train_scores, test_scores = learning_curve(
    estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
train_scores_mean = np.mean(train_scores, axis=1)
train_scores_std = np.std(train_scores, axis=1)
test_scores_mean = np.mean(test_scores, axis=1)
test_scores_std = np.std(test_scores, axis=1)
plt.grid()

plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                 train_scores_mean + train_scores_std, alpha=0.1,
                 color="r")
plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                 test_scores_mean + test_scores_std, alpha=0.1, color="g")
plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
         label="Training score")
plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
         label="Cross-validation score")

plt.legend(loc="best")
return plt
